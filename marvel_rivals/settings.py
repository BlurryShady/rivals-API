from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# -------------------------
# Base
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

import cloudinary 
# -------------------------
# Security
# -------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-only-change-me")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in {"1", "true", "yes"}

# -------------------------
# Hosts / CSRF
# -------------------------
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

# Render adds this automatically.
if render_host := os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(render_host)

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "http://localhost:8000,http://127.0.0.1:8000,https://rivals.blurryshady.dev",
    ).split(",")
    if origin.strip()
]

# -------------------------
# Logging / DRF throttles
# -------------------------
LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO")
USER_THROTTLE_RATE = os.environ.get("DRF_USER_THROTTLE", "300/day")
ANON_THROTTLE_RATE = os.environ.get("DRF_ANON_THROTTLE", "60/hour")
LOGIN_THROTTLE_RATE = os.environ.get("DRF_LOGIN_THROTTLE", "10/minute")
REGISTER_THROTTLE_RATE = os.environ.get("DRF_REGISTER_THROTTLE", "5/hour")

# -------------------------
# Applications
# -------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # Third party
    "rest_framework",
    "corsheaders",
    "channels",
    "rest_framework.authtoken",

    # Local apps
    "heroes",
    "teams",
    "accounts",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",

    # Request ID middleware
    "marvel_rivals.middleware.RequestIDMiddleware",

    # WhiteNoise for static on Render
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "marvel_rivals.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "marvel_rivals.wsgi.application"
ASGI_APPLICATION = "marvel_rivals.asgi.application"

# -------------------------
# Channels / Redis
# -------------------------
REDIS_URL = os.environ.get("REDIS_URL")

USE_REDIS_CHANNEL_LAYER = os.environ.get("USE_REDIS_CHANNEL_LAYER", "0").lower() in {"1", "true", "yes"}

if REDIS_URL and USE_REDIS_CHANNEL_LAYER:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
# -------------------------
# Database (Neon via DATABASE_URL)
# -------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
if CLOUDINARY_URL:
    cloudinary.config(cloudinary_url=CLOUDINARY_URL, secure=True)

# -------------------------
# Password validation
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------
# Internationalization
# -------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------
# Static files
# -------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

# -------------------------
# Cloudinary (media) + Django 5.2 storage config
# -------------------------

STORAGES = {
    # MEDIA (uploads): Cloudinary
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # STATIC: WhiteNoise compressed manifest
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Local-only media path (useful in dev). In prod, media is served by Cloudinary via STORAGES["default"].
if DEBUG:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# -------------------------
# Security headers (Render-friendly)
# -------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = (not DEBUG) and (
    os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "True").lower() in {"1", "true", "yes"}
)

# -------------------------
# CORS
# -------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://rivals.blurryshady.dev",
]

# -------------------------
# DRF
# -------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": USER_THROTTLE_RATE,
        "anon": ANON_THROTTLE_RATE,
        "auth-login": LOGIN_THROTTLE_RATE,
        "auth-register": REGISTER_THROTTLE_RATE,
    },
}

# -------------------------
# Default primary key
# -------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------
# Logging
# -------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] %(levelname)s %(request_id)s %(name)s:%(lineno)d %(message)s",
        },
    },
    "filters": {
        "request_id": {"()": "marvel_rivals.middleware.RequestIDFilter"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "filters": ["request_id"],
        },
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "accounts": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "teams": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "heroes": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
    },
}
