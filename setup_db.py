from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.recipe import Recipe
from models.user import User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('appconfig.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    print("✅ All tables created successfully.")
