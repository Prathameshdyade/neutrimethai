Alembic — quick usage (NutriMithai)
=================================

This project includes an Alembic setup under `alembic/` configured to read `DATABASE_URL` from `app.core.config.settings`.

Prerequisites
- Install dependencies (adds `alembic`):

```bash
pip install alembic
# or keep in requirements.txt and run:
pip install -r requirements.txt
```

- Ensure your environment has `DATABASE_URL` set (eg in a `.env` file):

```bash
export DATABASE_URL="postgresql://user:pass@localhost/nutrimithai"
# on Windows (PowerShell)
$env:DATABASE_URL = 'postgresql://user:pass@localhost/nutrimithai'
```

Common commands
- Create a new autogenered migration (edit produced file before applying):

```bash
alembic revision --autogenerate -m "describe changes"
```

- Apply migrations to the database:

```bash
alembic upgrade head
```

- (One-time) stamp the DB if it already has the schema:

```bash
alembic stamp head
```

Notes
- `alembic/env.py` is already set to load `settings.DATABASE_URL` from `app.core.config`.
- When using `--autogenerate`, inspect the generated migration for correctness before running `upgrade`.
- For SQLite, set `DATABASE_URL` to a `sqlite:///` path; some ALTER operations are limited on SQLite.

Troubleshooting
- If Alembic can't import the app, ensure the repo root is on `PYTHONPATH` and the virtualenv is activated.
- If migrations report unexpected changes, make sure all models are imported (or run `python -c "import app.models.product"`).

If you want, I can run `alembic upgrade head` here (requires a reachable DB from this environment). 
