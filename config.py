"""Application configuration loaded from the process environment.

Secrets must be provided through the environment or a local, ignored ``.env``
file. No credential defaults are provided here.
"""

from pathlib import Path
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Loading a local .env file is convenient for development. In production,
# environment variables supplied by the process/deployment platform take
# precedence because load_dotenv does not override existing values by default.
load_dotenv(ENV_FILE)


def _database_uri():
    """Return the configured database URI without exposing credentials."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Keep component-based configuration available for local development,
    # while correctly escaping usernames and passwords in the URI.
    required = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    }
    if not all(required.values()):
        return None

    try:
        port = int(os.getenv("DB_PORT", "3306"))
    except ValueError:
        return None

    return (
        "mysql+pymysql://"
        f"{quote_plus(required['DB_USER'])}:{quote_plus(required['DB_PASSWORD'])}"
        f"@{required['DB_HOST']}:{port}/{required['DB_NAME']}"
    )


class Config:
    """Base application configuration."""

    # Default to production-safe behavior when the environment is unspecified.
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

    DEBUG = APP_ENV == "development"
    SESSION_COOKIE_SECURE = APP_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    @classmethod
    def validate(cls):
        """Fail early with an actionable message when startup config is missing."""
        missing = []
        if not cls.SECRET_KEY:
            missing.append("SECRET_KEY")
        if not cls.SQLALCHEMY_DATABASE_URI:
            missing.append(
                "DATABASE_URL (or DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, and DB_PORT)"
            )

        if missing:
            missing_values = ", ".join(missing)
            raise RuntimeError(
                "Missing required configuration: "
                f"{missing_values}. Set these as environment variables or in "
                f"{ENV_FILE.name} (which must not be committed)."
            )
