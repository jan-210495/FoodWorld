# models/user.py

from datetime import datetime  # For timestamping user registration/confirmation
from werkzeug.security import generate_password_hash, check_password_hash  # For secure password handling
from models import db  # Shared SQLAlchemy instance
from flask_login import UserMixin  # Optional: for user session management


# Define the User model to represent users in the database
class User(db.Model, UserMixin):  # Inherits from db.Model and UserMixin for Flask-Login integration
    __tablename__ = 'users'  # Table name in the MySQL database

    # Unique ID for each user (Primary Key)
    id = db.Column(db.Integer, primary_key=True)

    # Username must be unique and not null
    username = db.Column(db.String(50), unique=True, nullable=False)

    # Email must also be unique and not null
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Secure password hash (actual passwords are not stored)
    password_hash = db.Column(db.String(128), nullable=False)

    # User role: either 'admin' or 'customer', defaults to 'customer'
    role = db.Column(db.String(20), default='customer')

    # Whether the user has confirmed their email (optional feature)
    confirmed = db.Column(db.Boolean, default=False)

    # Date and time of confirmation (nullable)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    # Date and time of registration (auto-set to current time)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Sets the password by hashing it securely
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Checks if a given password matches the stored hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
