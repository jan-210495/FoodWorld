"""FoodWorld application factory and WSGI configuration."""

import os

from flask import Flask, redirect, render_template, url_for
from flask_cors import CORS
from flask_wtf.csrf import CSRFError

from config import Config
from extensions import csrf, db, limiter, login_manager, migrate
from models.user import User


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app(config_object=None):
    """Create and configure a FoodWorld Flask application."""
    config_object = config_object or Config

    app = Flask(__name__)
    app.config.from_object(config_object)
    if config_object is Config:
        Config.validate(app.config)

    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # The application is server-rendered, so CORS is disabled unless an
    # explicit allow-list is supplied for a separate trusted frontend.
    if app.config.get("CORS_ORIGINS"):
        CORS(app, origins=app.config["CORS_ORIGINS"])

    login_manager.init_app(app)

    from resources.recipe_routes import recipe_bp
    from resources.user_routes import user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(recipe_bp)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return render_template(
            "error.html",
            title="Request expired",
            message="Please refresh the page and submit the form again.",
        ), 400

    @app.errorhandler(403)
    def handle_forbidden(error):
        return render_template(
            "error.html",
            title="Access denied",
            message="You do not have permission to view this page.",
        ), 403

    @app.errorhandler(404)
    def handle_not_found(error):
        return render_template(
            "error.html",
            title="Page not found",
            message="We could not find the page you requested.",
        ), 404

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        if app.config.get("APP_ENV") == "production":
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response

    @app.route("/")
    def home_redirect():
        return redirect(url_for("user_bp.home"))

    return app


if __name__ == "__main__":
    application = create_app()
    port = int(os.environ.get("PORT", 3000))
    application.run(
        host="0.0.0.0",
        port=port,
        debug=application.config["DEBUG"],
    )
