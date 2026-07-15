import os

from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager

from config import Config
from models import db
from models.user import User
from resources.recipe_routes import recipe_bp
from resources.user_routes import user_bp


# -------------------------------------------------------
# Create Flask app
# -------------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)
Config.validate()

# -------------------------------------------------------
# Initialize Database
# -------------------------------------------------------

db.init_app(app)

# -------------------------------------------------------
# Enable CORS
# -------------------------------------------------------

CORS(app)

# -------------------------------------------------------
# Initialize Flask-Login
# -------------------------------------------------------

login_manager = LoginManager()
login_manager.login_view = "user_bp.login_page"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------------------------------------
# Register Blueprints
# -------------------------------------------------------

app.register_blueprint(user_bp)
app.register_blueprint(recipe_bp)


@app.route("/")
def home_redirect():
    return redirect(url_for("user_bp.home"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
