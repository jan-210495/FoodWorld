from flask import url_for
from app import app

with app.app_context():
    for rule in app.url_map.iter_rules():
        print(rule)