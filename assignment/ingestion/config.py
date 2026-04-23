import os


class Development:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class Production:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


def get_config():
    """Return the configuration appropriate for the current environment"""
    env = os.environ.get("FLASK_ENV", "development")
    return Production if env == "production" else Development
