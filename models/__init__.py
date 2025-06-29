# models/__init__.py

# Importing SQLAlchemy to be used as the ORM (Object Relational Mapper)
from flask_sqlalchemy import SQLAlchemy

# Initialize a single SQLAlchemy instance to be shared across all models
db = SQLAlchemy()
