import logging
import random
import time
from ingestion.extensions import celery, db
from ingestion.models import Transaction
from ingestion.enums import Category

_logger = logging.getLogger(__name__)

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
    transactions = Transaction.query.filter_by(batch_id=batch_id).all()
    for transaction in transactions:
        if transaction.ingestion_status == Transaction.IngestionStatus.PENDING:
            _logger.info("Processing transaction: %s", transaction.transaction_id)
            transaction.ingestion_status = Transaction.IngestionStatus.PROCESSING
            db.session.commit()
            time.sleep(random.uniform(0.5, 1))  # Simulate random processing latency
            try:
                transaction.category = _categorise_transaction(transaction.description)
            except Exception as e:
                _logger.exception("Error categorising transaction %s: %s", transaction.transaction_id, e)
                transaction.ingestion_status = Transaction.IngestionStatus.FAILED
                db.session.commit()
                continue
            transaction.ingestion_status = Transaction.IngestionStatus.COMPLETED
            db.session.commit()
            _logger.info("Categorised transaction %s as %s", transaction.transaction_id, transaction.category)
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

    raise ValueError("Unable to determine category from description")
