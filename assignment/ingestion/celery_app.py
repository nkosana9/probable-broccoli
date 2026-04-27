from ingestion.app import create_app
from ingestion.extensions import celery

flask_app = create_app()

celery.conf.update(
    broker_url=flask_app.config["CELERY_BROKER_URL"],
    result_backend=flask_app.config.get("CELERY_RESULT_BACKEND"),
)

# Make the Flask app accessible to tasks
celery.flask_app = flask_app
