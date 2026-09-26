"""Production settings with secure defaults."""

from .base import *  # noqa: F403

DEBUG = False

if SECRET_KEY == "django-insecure-local-development-only-change-me":  # noqa: F405
    raise ValueError("Set a strong SECRET_KEY in the production environment")

SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
