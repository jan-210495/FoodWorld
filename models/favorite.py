"""Saved recipe relationship."""

from datetime import datetime, timezone

from models import db


class Favorite(db.Model):
    __tablename__ = "favorites"
    __table_args__ = (
        db.UniqueConstraint("user_id", "recipe_id", name="uq_favorite_user_recipe"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="favorites")
    recipe = db.relationship("Recipe", back_populates="favorites")
