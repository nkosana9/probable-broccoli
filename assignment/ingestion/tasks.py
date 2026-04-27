import logging
import random
import time

from ingestion.enums import Category, IngestionStatus
from ingestion.extensions import celery, db
from ingestion.models import Transaction

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Simple ruleset for categorising transactions based on keywords in the description
_CATEGORIES_ENGINE = {
    Category.EDUCATION: ["coursera", "datacamp", "udemy"],
    Category.ENTERTAINMENT: ["disney", "netflix", "spotify"],
    Category.INCOME: ["eft", "paypal", "stripe"],
    Category.SHOPPING: ["amazon", "bash", "takealot"],
    Category.TRANSPORT: ["bolt", "indrive", "uber"],
}


@celery.task()
def process_transactions(batch_id: str):
    """
    A background task to categorise transactions in a given batch.
    Only processes transactions with 'pending' status.
    """
    with celery.flask_app.app_context():
        transactions: list[Transaction] = Transaction.query.filter_by(batch_id=batch_id).all()
        for transaction in transactions:
            if transaction.ingestion_status == IngestionStatus.PENDING:
                _logger.debug("Processing transaction: %s", transaction.transaction_id)
                transaction.ingestion_status = IngestionStatus.PROCESSING
                db.session.commit()
                time.sleep(random.uniform(0.5, 1))  # Simulate random processing latency
                try:
                    transaction.category = _categorise_transaction(
                        f"{transaction.merchant_name + transaction.description}"
                    )
                except Exception as e:
                    _logger.exception("Error categorising transaction %s: %s", transaction.transaction_id, e)
                    transaction.ingestion_status = IngestionStatus.FAILED
                    db.session.commit()
                    continue
                transaction.ingestion_status = IngestionStatus.COMPLETED
                db.session.commit()
                _logger.debug("Categorised transaction %s as %s", transaction.transaction_id, transaction.category)
            else:
                _logger.warning(
                    "Skipping transaction %s with status %s", transaction.transaction_id, transaction.ingestion_status
                )


def _categorise_transaction(description: str) -> str:
    """A simple categorisation logic based on keywords in the transaction description."""
    description_lower = description.lower()

    for category, keywords in _CATEGORIES_ENGINE.items():
        if any(keyword in description_lower for keyword in keywords):
            return category.value

    raise ValueError(f"Unable to determine category from description {description}")
