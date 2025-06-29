# models/category.py

from models import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    photo = db.Column(db.String(255))

    # Relationship to recipes
    recipes = db.relationship("Recipe", back_populates="category")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "photo": self.photo}
