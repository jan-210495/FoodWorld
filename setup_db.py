from flask import Flask
from models import db
from models.user import User
from models.recipe import Recipe
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
