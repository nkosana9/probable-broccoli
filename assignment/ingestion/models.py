from datetime import datetime
from enum import StrEnum

from ingestion.extensions import db


class IngestionStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Account(db.Model):
    __tablename__ = "account"
    account_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    transactions = db.relationship("Transaction", back_populates="account", cascade="all, delete-orphan")


class Transaction(db.Model):
    __tablename__ = "transaction"
    transaction_id = db.Column(db.String(100), primary_key=True)
    account_id = db.Column(db.String(100), db.ForeignKey("account.account_id"), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    merchant_name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    batch_id = db.Column(db.String(36), nullable=False)  # UUID as string
    ingestion_status = db.Column(db.Enum(IngestionStatus, nullable=False, default=IngestionStatus.PENDING))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    account = db.relationship("Account", back_populates="transactions")
