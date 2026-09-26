"""Shared settings for every deployment environment."""

from pathlib import Path
from urllib.parse import unquote, urlsplit

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class EnvironmentSettings(BaseSettings):
    """Environment variables loaded from the process or the local .env file."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: str = "django-insecure-local-development-only-change-me"
    debug: bool = True
    database_url: str = "postgresql://postgres:postgres@localhost:5432/social_media"
    redis_url: str = "redis://localhost:6379/0"
    allowed_hosts: str = "localhost,127.0.0.1"


environment = EnvironmentSettings()

SECRET_KEY = environment.secret_key
DEBUG = environment.debug
ALLOWED_HOSTS = [host.strip() for host in environment.allowed_hosts.split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.users.apps.UsersConfig",
    "apps.posts.apps.PostsConfig",
    "apps.comments.apps.CommentsConfig",
    "apps.likes.apps.LikesConfig",
    "apps.follows.apps.FollowsConfig",
    "apps.feed.apps.FeedConfig",
    "apps.notifications.apps.NotificationsConfig",
    "apps.messaging.apps.MessagingConfig",
    "apps.search.apps.SearchConfig",
    "apps.media.apps.MediaConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

_database_url = urlsplit(environment.database_url)
if _database_url.scheme not in {"postgres", "postgresql"}:
    raise ValueError("DATABASE_URL must use the postgres:// or postgresql:// scheme")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(_database_url.path.lstrip("/")),
        "USER": unquote(_database_url.username or ""),
        "PASSWORD": unquote(_database_url.password or ""),
        "HOST": _database_url.hostname or "localhost",
        "PORT": _database_url.port or 5432,
        "CONN_MAX_AGE": 60,
    }
}

AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
