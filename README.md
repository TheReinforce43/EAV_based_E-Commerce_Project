# Ecommerce Project

A simple Django-based ecommerce starter project with Docker support.

## Features

- Django application with user app and basic models
- Dockerfile and `docker-compose.yml` for containerised development
- Nginx config in `nginx/` for production proxying
- Celery configured (see `celery.py`) for background tasks

## Requirements

- Python 3.8+
- pip
- Docker (optional, for containerized setup)

Dependencies are listed in `requirements.txt`.

## Quick start (local)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix/macOS
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Collect static files (for production):

```bash
python manage.py collectstatic
```

5. Run the development server:

```bash
python manage.py runserver
```

## Docker (optional)

Build and run using Docker Compose:

```bash
docker-compose up --build
```

This project includes a `Dockerfile` and `docker-compose.yml` for containerized development. See `nginx/default.conf` for the example Nginx configuration.

## Testing

Run tests with Django's test runner:

```bash
python manage.py test
```

## Project layout

- `ecommerce_project/` - Django project settings and WSGI/ASGI entrypoints
- `user/` - user app (models, serializers, views, tests)
- `utils/` - helper utilities
- `staticfiles/`, `media/` - static and media output
- `nginx/` - Nginx configuration
- `Dockerfile`, `docker-compose.yml` - container setup

## Notes

- Environment-specific settings (secrets, DB, allowed hosts) should be configured in environment variables or a separate settings module.
- Celery configuration lives in `ecommerce_project/celery.py`.

## Contributing

Feel free to open issues or submit pull requests.

## License

This project is unlicensed. Add a license file if you intend to open-source it.
