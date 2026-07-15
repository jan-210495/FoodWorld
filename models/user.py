"""User database model and password helpers."""

from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from models import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="customer")
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
