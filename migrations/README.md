# FoodWorld database migrations

The application uses Flask-Migrate/Alembic. Apply schema changes with:

```bash
flask --app wsgi:app db upgrade
```

Create a new migration after changing models with:

```bash
flask --app wsgi:app db migrate -m "describe the change"
flask --app wsgi:app db upgrade
```

The first migration adds the saved-recipe relationship. Existing recipe and user tables are assumed to have been created by the original application and are not recreated by this migration.

Never run migrations against production before reviewing the generated SQL and taking a database backup.
