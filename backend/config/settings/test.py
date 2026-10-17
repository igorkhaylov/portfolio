"""Test settings — runnable with NO external services.

Used by pytest via `DJANGO_SETTINGS_MODULE = "config.settings.test"` (pyproject.toml).
Everything heavy (Postgres, real email, disk storage) is swapped for
in-memory/local backends so the suite runs anywhere, including before you have created
your initial migrations (pytest is configured with --no-migrations).
"""

import os

# Ensure base.py's ENVIRONMENT validation/branching sees a valid value.
os.environ.setdefault("ENVIRONMENT", "test")

from .base import *
from .third_party import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Quieter logs during tests.
LOG_LEVEL = "WARNING"
LOGGING["root"]["level"] = "WARNING"
