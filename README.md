# Marvel Rivals Builder API

Django + DRF backend for the Marvel Rivals Builder project.  
Stores heroes, teams, votes, and comments and exposes real-time comment streaming via WebSockets using Django Channels.

## Tech Stack
- Django 5.2
- Django REST Framework
- Django Channels + `channels-redis`
- SQLite (dev) / Postgres (prod)
- Redis (required for production WebSockets)

## Getting Started
> Requires Python 3.11+
```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate      # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Environment Variables (`.env`)
| Variable | Description |
| --- | --- |
| `DJANGO_SECRET_KEY` | Strong secret used for crypto/signing |
| `DJANGO_DEBUG` | Enable/disable debug mode (`False` in production) |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of backend hosts |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | HTTPS origins allowed to submit forms/requests |
| `DJANGO_SECURE_SSL_REDIRECT` | Force HTTPS in production (`True`) |
| `REDIS_URL` | `redis://` connection string when using `channels-redis` |
| `DATABASE_URL` (optional) | Standard Django DATABASE_URL string for Postgres |

## Useful Commands
| Purpose | Command |
| --- | --- |
| Apply migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Load heroes from script | `python add_heroes.py` |
| Run tests | `python manage.py test` |
| Collect static files | `python manage.py collectstatic` |

> Note: `SECURE_SSL_REDIRECT` should be enabled only when running behind a proxy that sets `X-Forwarded-Proto` (e.g. Render).


## WebSockets
Comment broadcasting uses Django Channels. Local dev can rely on the in-memory channel layer, but production must set `REDIS_URL` and run the app via an ASGI server (e.g., Daphne or Uvicorn).

## Deployment Checklist
1. Install dependencies via `pip install -r requirements.txt`.
2. Configure environment variables from `.env.example` (Render/Heroku dashboard).
3. Provision Redis and set `REDIS_URL`.
4. Use an ASGI server start command such as:
   ```
   daphne -b 0.0.0.0 -p $PORT marvel_rivals.asgi:application
   ```
5. Run migrations (`python manage.py migrate`).
6. Configure media storage (e.g., S3) for avatars/hero images if needed.


This repository contains the backend API for the Marvel Rivals Builder project. It was built as a production-style backend and portfolio showcase.  
Live frontend consuming this API: [rivals.blurryshady.dev](https://rivals.blurryshady.dev).
