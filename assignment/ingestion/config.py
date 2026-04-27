import os


class BaseConfig:
    AUTH_TOKEN: str = os.getenv("AUTH_TOKEN", "")
    DEBUG: bool = os.getenv("DEBUG", "").lower() in ("true", "1")
    SQLALCHEMY_DATABASE_URI: str = os.environ["DATABASE_URL"]
    CELERY_BROKER_URL: str = os.environ["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND: str = os.environ["CELERY_RESULT_BACKEND"]


def get_config() -> BaseConfig:
    """Factory function to get the appropriate configuration class based on environment variables."""
    return BaseConfig()
