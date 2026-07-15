# FoodWorld

FoodWorld is a Flask recipe discovery application with:

- Recipe browsing, category filtering, and text search.
- Admin recipe and category management.
- Password-hashed authentication with role-based access.
- Saved recipes for signed-in users.
- Optional structured AI recommendations and ingredient substitution.
- MySQL in production and an isolated SQLite database for tests.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Replace the placeholders in `.env` with local values. Never restore the old credential file and never commit `.env`.

Start the development server:

```bash
APP_ENV=development python app.py
```

## Configuration

Required:

- `SECRET_KEY` — a long random value used to sign sessions.
- `DATABASE_URL` — a SQLAlchemy URL, or `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

Optional:

- `GEMINI_API_KEY` — enables AI recipe generation and substitutions.
- `PEXELS_API_KEY` — enables recipe images from Pexels.
- `CORS_ORIGINS` — comma-separated allow-list for a separately hosted trusted frontend. Same-origin server-rendered requests do not need CORS.
- `RATELIMIT_STORAGE_URI` — use Redis or another shared store for multi-process production deployments; the default in-memory store is for development only.

Generate a local secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Database migrations

The application uses Flask-Migrate/Alembic:

```bash
flask --app wsgi:app db upgrade
```

After model changes:

```bash
flask --app wsgi:app db migrate -m "describe the change"
flask --app wsgi:app db upgrade
```

Review generated migrations and back up production before upgrading. The current migration adds the saved-recipe relationship; the original tables are assumed to already exist.

## Tests and quality checks

```bash
pytest
ruff check .
python -m compileall -q .
```

The test suite uses an in-memory SQLite database and does not require production credentials or network AI services.

## Production

Use the WSGI entrypoint with debug disabled:

```bash
APP_ENV=production gunicorn wsgi:app
```

The `Procfile` uses the same entrypoint. Supply secrets through the deployment platform rather than a file in the repository.

## Security

- State-changing forms use CSRF protection.
- AI responses are validated as JSON and rendered through escaped templates; arbitrary model HTML is not trusted.
- AI and image endpoints are rate-limited.
- External image requests have timeouts and local fallbacks.
- Uploaded files are not accepted; recipes currently use validated HTTP(S) image URLs.
- If a credential was ever committed, revoke or rotate it and remove it from repository history using an approved history-rewrite process.
