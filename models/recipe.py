# models/recipe.py

from models import db  # Import the shared SQLAlchemy instance
from datetime import datetime  # Used for automatic timestamping


# Define the Recipe model to represent recipes in the database
class Recipe(db.Model):
    __tablename__ = 'recipes'  # Table name in the MySQL database

    # Unique ID for each recipe (Primary Key)
    id = db.Column(db.Integer, primary_key=True)

    # Name/title of the recipe (must be unique and not null)
    name = db.Column(db.String(120), unique=True, nullable=False)

    # Description of the recipe (optional)
    description = db.Column(db.Text)

    # Ingredients stored as a comma-separated string (required)
    ingredients = db.Column(db.Text, nullable=False)

    # URL to an image representing the recipe (optional)
    photo = db.Column(db.Text, nullable=True)

    # Timestamp of when the recipe was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Timestamp of when the recipe was last updated (auto-updated)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Instructions for the recipe (optional)
    instructions = db.Column(db.Text, nullable=True)

    # Category of the recipe (e.g., breakfast, dinner, dessert)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id'),
                            nullable=True)
    category = db.relationship("Category", back_populates="recipes")

    # Converts the recipe object into a dictionary (for JSON or API use)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients.split(", "),
            "instructions": self.instructions,
            "photo": self.photo,
            "category": self.category.name if self.category else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
