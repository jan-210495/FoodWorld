from app import app
from models import db
from models.category import Category

with app.app_context():
    cats = Category.query.all()
    for c in cats:
        print(c.id, c.name, c.photo)
