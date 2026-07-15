"""Shared Flask extensions initialized by the application factory."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from models import db

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "user_bp.login_page"
login_manager.login_message_category = "error"
limiter = Limiter(key_func=get_remote_address, default_limits=[])
migrate = Migrate()

__all__ = ["csrf", "db", "limiter", "login_manager", "migrate"]
