from flask import Flask
from flask_cors import CORS
from models.user import db as user_db
from models.recipe import db as recipe_db
from resources.user_routes import user_bp
from resources.recipe_routes import recipe_bp
import config

app = Flask(__name__)
app.config.from_object(config)

# Initialize database (same object, shared setup)
user_db.init_app(app)
recipe_db.init_app(app)

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(recipe_bp)

@app.route('/')
def home():
    return "FoodWorld API is running!"

if __name__ == '__main__':
    app.run(debug=True)
