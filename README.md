# SmartRecruit

A Django recruitment application for job postings and applications.

## Local setup

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Install the configured Bootstrap template pack and PostgreSQL driver with `pip install crispy-bootstrap5 psycopg2-binary`.
4. Create a PostgreSQL database named `recruitment_system` (default user: `postgres`, host: `localhost`, port: `5432`).
5. Set `DJANGO_SECRET_KEY` and `DB_PASSWORD` in your environment, or create an ignored `website/local_settings.py` with local settings overrides.
6. Run `python manage.py migrate`, then `python manage.py runserver`.

Uploaded CVs, local databases, credentials, and virtual environments are excluded from version control.
