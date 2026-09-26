"""User identity and authentication models."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Project user model based on Django's built-in authentication fields."""
