"""Recipe database model."""

import json
from datetime import datetime, timezone

from models import db


class Recipe(db.Model):
    __tablename__ = "recipes"
    __table_args__ = (
        db.Index("ix_recipes_category_id", "category_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    # New records store a JSON list in this existing Text column. Legacy
    # comma/newline-separated records are still readable through the property.
    ingredients = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    instructions = db.Column(db.Text, nullable=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True,
    )

    category = db.relationship("Category", back_populates="recipes")
    favorites = db.relationship(
        "Favorite",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )

    @property
    def ingredient_items(self):
        """Return ingredients as a list, including legacy stored records."""
        if not self.ingredients:
            return []
        try:
            parsed = json.loads(self.ingredients)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except (TypeError, json.JSONDecodeError):
            pass

        return [
            item.strip()
            for item in self.ingredients.replace("\r", "").replace("\n", ",").split(",")
            if item.strip()
        ]

    @property
    def ingredient_text(self):
        return "\n".join(self.ingredient_items)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredient_items,
            "instructions": self.instructions,
            "photo": self.photo,
            "category": self.category.name if self.category else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
