import os


# Set defaults for local Windows testing before config.py loads settings.
# setdefault keeps Docker Compose's own values (database / 5432) untouched
# when running inside the api container.
os.environ.setdefault("DATABASE_HOSTNAME", "127.0.0.1")
os.environ.setdefault("DATABASE_PORT", "5433")
