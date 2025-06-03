from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load environment variables
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from resources.recipe_routes import recipe_blueprint
    app.register_blueprint(recipe_blueprint, url_prefix='/recipes')

    from resources.user_routes import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/users')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
