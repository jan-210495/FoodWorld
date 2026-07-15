"""Environment-backed application configuration."""

import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)


def _database_uri():
    """Build a SQLAlchemy URI without logging or exposing credentials."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    values = {
        "host": os.getenv("DB_HOST"),
        "name": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    if not all(values.values()):
        return None

    try:
        port = int(os.getenv("DB_PORT", "3306"))
    except ValueError:
        return None

    return (
        "mysql+pymysql://"
        f"{quote_plus(values['user'])}:{quote_plus(values['password'])}"
        f"@{values['host']}:{port}/{values['name']}"
    )


def _origins():
    return [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "").split(",")
        if origin.strip()
    ]


class Config:
    """Default configuration for local development and production."""

    APP_ENV = os.getenv("APP_ENV", os.getenv("FLASK_ENV", "production")).lower()
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    CORS_ORIGINS = _origins()
    REQUIRE_EMAIL_CONFIRMATION = False

    DEBUG = APP_ENV == "development"
    TESTING = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    SESSION_COOKIE_SECURE = APP_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_ENABLED = True
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_HEADERS_ENABLED = True

    @classmethod
    def validate(cls, settings=None):
        """Fail early with an actionable message when required config is absent."""
        values = settings or {
            "SECRET_KEY": cls.SECRET_KEY,
            "SQLALCHEMY_DATABASE_URI": cls.SQLALCHEMY_DATABASE_URI,
        }
        missing = []
        if not values.get("SECRET_KEY"):
            missing.append("SECRET_KEY")
        if not values.get("SQLALCHEMY_DATABASE_URI"):
            missing.append(
                "DATABASE_URL (or DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, and DB_PORT)"
            )

        if missing:
            raise RuntimeError(
                "Missing required configuration: "
                f"{', '.join(missing)}. Set these as environment variables or in "
                f"{ENV_FILE.name} (which must not be committed)."
            )


class TestingConfig(Config):
    """Isolated configuration used by the automated test suite."""

    TESTING = True
    DEBUG = False
    SECRET_KEY = "test-only-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    SESSION_COOKIE_SECURE = False
