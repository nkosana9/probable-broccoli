from enum import StrEnum


class Category(StrEnum):
    """Transaction categories for classification."""

    EDUCATION = "Education"
    ENTERTAINMENT = "Entertainment"
    INCOME = "Income"
    SHOPPING = "Shopping"
    TRANSPORT = "Transport"


class IngestionStatus(StrEnum):
    """Status of transaction ingestion and processing."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
