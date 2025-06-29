# user_routes.py

# ------------------------------
# Imports
# ------------------------------

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from models.user import User
from models import db
from datetime import datetime
from models.category import Category

# ------------------------------
# Blueprint Definition
# ------------------------------

# Define a blueprint for all user-related routes
user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

# ------------------------------
# Public Home Page
# ------------------------------


@user_bp.route('/')
def home():
    """
    Displays the public home page.
    Loads a preview of categories to display on the homepage.
    """
    categories = Category.query.limit(6).all()
    return render_template("index.html", categories=categories)


# ------------------------------
# Alternate Test Home (Optional)
# ------------------------------


@user_bp.route('/canva')
def home_canva():
    """
    Displays an alternate home page template for testing purposes.
    """
    categories = Category.query.limit(6).all()
    return render_template("index_canva.html", categories=categories)


# ------------------------------
# Login Page (GET)
# ------------------------------


@user_bp.route('/login', methods=['GET'])
def login_page():
    """
    Displays the login page with the login form.
    """
    return render_template("log_in.html")


# ------------------------------
# Register Page (GET)
# ------------------------------


@user_bp.route('/register', methods=['GET'])
def register_page():
    """
    Displays the user registration page.
    """
    return render_template("sign_up.html")


# ------------------------------
# Register User (POST)
# ------------------------------


@user_bp.route('/register', methods=['POST'])
def register():
    """
    Handles user registration:
    - Accepts form or JSON data.
    - Checks if user already exists.
    - Creates a new user and saves to DB.
    - Redirects to home after successful registration.
    """

    # Retrieve data from form or JSON
    data = request.form if not request.is_json else request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check required fields
    if not username or not email or not password:
        return "Missing required fields", 400

    # Check if user already exists
    existing = User.query.filter((User.email == email)
                                 | (User.username == username)).first()

    if existing:
        return "User already exists", 409

    # Create and save the new user
    user = User(username=username, email=email, role='customer')
    user.set_password(password)
    user.confirmed = True
    user.confirmed_on = datetime.utcnow()

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('user_bp.home'))


# ------------------------------
# Login User (POST)
# ------------------------------


@user_bp.route('/login', methods=['POST'])
def login():
    """
    Handles user login:
    - Validates email and password.
    - Logs in the user using Flask-Login.
    - Redirects admins to the admin dashboard.
    - Redirects customers to the user dashboard.
    """

    data = request.form if not request.is_json else request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)

        if user.role == 'admin':
            return redirect(url_for('user_bp.admin_home'))
        else:
            return redirect(url_for('user_bp.user_home'))

    return "Invalid credentials", 401


# ------------------------------
# Admin Home Page
# ------------------------------


@user_bp.route('/admin/home')
@login_required
def admin_home():
    """
    Displays the admin homepage.
    Redirects non-admin users back to the public home page.
    """

    if current_user.role != 'admin':
        return redirect(url_for('user_bp.home'))

    return render_template("admin_home.html")


# ------------------------------
# User Home (Dashboard)
# ------------------------------


@user_bp.route('/home')
@login_required
def user_home():
    """
    Displays the user dashboard page after login.
    Requires the user to be logged in.
    """

    return render_template("user_home.html", username=current_user.username)


# ------------------------------
# Logout
# ------------------------------


@user_bp.route('/logout')
@login_required
def logout():
    """
    Logs the user out using Flask-Login.
    Redirects to the public home page.
    """

    logout_user()
    return redirect(url_for('user_bp.home'))
