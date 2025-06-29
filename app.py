from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager
from models import db
from models.user import User
from resources.user_routes import user_bp
from resources.recipe_routes import recipe_bp
from config import Config
import os

# -------------------------------------------------------
# Load environment variables
# -------------------------------------------------------

load_dotenv('appconfig.env')

print("✅ SQLALCHEMY_DATABASE_URI =", Config.SQLALCHEMY_DATABASE_URI)

# -------------------------------------------------------
# Create Flask app
# -------------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv("SECRET_KEY", "def-secret")

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
login_manager.login_view = 'user_bp.login_page'  # redirects to login if not logged in
login_manager.init_app(app)


# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------------------------------------
# Register Blueprints
# -------------------------------------------------------

app.register_blueprint(user_bp)
app.register_blueprint(recipe_bp)

# -------------------------------------------------------
# Root Redirect
# -------------------------------------------------------


@app.route("/")
def home_redirect():
    return redirect(url_for("user_bp.home"))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
