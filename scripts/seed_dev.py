"""Seed a local database with starter categories and an admin account.

Usage: SEED_ADMIN_PASSWORD='...' python scripts/seed_dev.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app  # noqa: E402
from models import db  # noqa: E402
from models.category import Category  # noqa: E402
from models.user import User  # noqa: E402

app = create_app()
password = os.getenv("SEED_ADMIN_PASSWORD")
if not password:
    raise SystemExit("Set SEED_ADMIN_PASSWORD before running the seed script.")

with app.app_context():
    for name in ("Breakfast", "Lunch", "Dinner", "Dessert"):
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))

    admin_email = os.getenv("SEED_ADMIN_EMAIL", "admin@example.com").lower()
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(username=os.getenv("SEED_ADMIN_USERNAME", "admin"), email=admin_email, role="admin")
        admin.set_password(password)
        admin.confirmed = True
        db.session.add(admin)
    db.session.commit()
    print("Development seed completed.")
