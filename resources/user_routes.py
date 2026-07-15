"""Authentication and user dashboard routes."""

from datetime import datetime, timezone

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from extensions import limiter
from models import db
from models.category import Category
from models.favorite import Favorite
from models.user import User
from utils.validation import validate_auth_input

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")


def _response_error(message, status, template=None, form_data=None):
    if request.is_json:
        return jsonify({"error": message}), status
    flash(message, "error")
    return render_template(template, form_data=form_data or {}), status


@user_bp.route("/")
def home():
    categories = Category.query.order_by(Category.name.asc()).limit(6).all()
    return render_template("index.html", categories=categories)


@user_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("log_in.html", form_data={})


@user_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("sign_up.html", form_data={})


@user_bp.route("/register", methods=["POST"])
@limiter.limit("5 per hour")
def register():
    data = request.get_json(silent=True) if request.is_json else request.form
    data = data or {}
    cleaned, errors = validate_auth_input(
        data.get("username"), data.get("email"), data.get("password")
    )

    existing = User.query.filter(
        or_(
            func.lower(User.email) == cleaned["email"],
            func.lower(User.username) == cleaned["username"].lower(),
        )
    ).first()
    if existing:
        errors.append("That username or email is already registered.")

    if errors:
        message = " ".join(errors)
        return _response_error(message, 400, "sign_up.html", data)

    # Email verification is intentionally not required by the current product;
    # users are marked confirmed because no confirmation workflow is advertised.
    confirmed = not current_app.config.get("REQUIRE_EMAIL_CONFIRMATION", False)
    user = User(
        username=cleaned["username"],
        email=cleaned["email"],
        role="customer",
        confirmed=confirmed,
        confirmed_on=datetime.now(timezone.utc) if confirmed else None,
    )
    user.set_password(cleaned["password"])
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return _response_error("That username or email is already registered.", 409, "sign_up.html", data)

    if request.is_json:
        return jsonify({"message": "Registration successful."}), 201
    flash("Registration successful. You can now log in.", "success")
    return redirect(url_for("user_bp.login_page"))


@user_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.get_json(silent=True) if request.is_json else request.form
    data = data or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    remember = str(data.get("remember", "")).lower() in {"1", "true", "on", "yes"}
    user = User.query.filter(func.lower(User.email) == email).first()

    if not user or not user.check_password(password):
        return _response_error("Invalid email or password.", 401, "log_in.html", data)

    login_user(user, remember=remember)
    destination = "user_bp.admin_home" if user.role == "admin" else "user_bp.user_home"
    if request.is_json:
        return jsonify({"message": "Login successful."})
    return redirect(url_for(destination))


@user_bp.route("/admin/home")
@login_required
def admin_home():
    if current_user.role != "admin":
        return redirect(url_for("user_bp.home"))
    return render_template("admin_home.html")


@user_bp.route("/home")
@login_required
def user_home():
    favorites = Favorite.query.options(joinedload(Favorite.recipe)).filter_by(
        user_id=current_user.id
    ).order_by(Favorite.created_at.desc()).all()
    return render_template("user_home.html", username=current_user.username, favorites=favorites)


@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("user_bp.home"))
