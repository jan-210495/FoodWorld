# FoodWorld

Recipe discovery and management application built with Flask, SQLAlchemy, Flask-Login, and optional Gemini/Pexels integrations.

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the configuration template:

   ```bash
   cp .env.example .env
   ```

4. Replace the placeholders in `.env` with local development values.
5. Start the application:

   ```bash
   python app.py
   ```

`.env` and `appconfig.env` are intentionally ignored by Git. Do not commit database passwords, Flask secret keys, or third-party API keys.

## Configuration

The application requires:

- `SECRET_KEY` — a long, random value used to sign sessions.
- `DATABASE_URL` — a SQLAlchemy database URL, or the component variables `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

The AI features use these optional variables:

- `GEMINI_API_KEY`
- `PEXELS_API_KEY`

When optional API keys are absent or an external provider is unavailable, the application uses its fallback behavior. Production deployments should provide the required values through the platform's secret/environment configuration rather than a file in the repository.

## Production

Use a production WSGI server and keep `APP_ENV=production`:

```bash
gunicorn app:app
```

Never run Flask's development server or debug mode in production.

## Security note

If a credential has ever been committed to this repository, treat it as compromised: revoke or rotate it with the relevant provider and remove it from repository history using an approved Git history-rewrite process.
