from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    # Register blueprints
    from resources.recipe_routes import recipe_blueprint
    from resources.user_routes import user_blueprint

    app.register_blueprint(recipe_blueprint, url_prefix="/recipe")
    app.register_blueprint(user_blueprint, url_prefix="/user")

    return app
