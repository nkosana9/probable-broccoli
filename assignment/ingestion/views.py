from collections import Counter
from datetime import datetime
from uuid import uuid4

from flask import jsonify, request

from ingestion.extensions import db
from ingestion.models import Account, Transaction
from ingestion.tasks import process_transactions


def bulk_account_ingestion():
    """
    Endpoint to ingest bulk accounts and transactions data for further processing

    Expected JSON payload format:
    {
        "accounts": [
            {
                "account_id": "acc_123",
                "name": "John Doe",
                "type": "checking",
                "subtype": "personal",
                "mask": "1234"
            },
            ...
        ],
        "transactions": [
            {
                "transaction_id": "txn_456",
                "account_id": "acc_123",
                "amount": -50.75,
                "currency": "USD",
                "date": "2024-06-01T12:34:56Z",
                "merchant_name": "Amazon",
                "description": "Amazon purchase",
            },
            ...
        ]
    }
    """
    data = request.get_json()
    accounts_data = data.get("accounts", [])
    transactions_data = data.get("transactions", [])
    request_account_ids = [a["account_id"] for a in accounts_data]

    # Upsert accounts
    existing_accounts = Account.query.filter(Account.account_id.in_(request_account_ids)).all()
    existing_account_ids = set(a.account_id for a in existing_accounts)
    accounts_to_create = [Account(**a) for a in accounts_data if a["account_id"] not in existing_account_ids]
    if accounts_to_create:
        db.session.bulk_save_objects(accounts_to_create)

    # Bulk create transactions
    batch_id = str(uuid4())
    transactions_to_create = [Transaction(**t, batch_id=batch_id) for t in transactions_data]
    db.session.bulk_save_objects(transactions_to_create)
    db.session.commit()

    # Trigger async categorization task with Celery
    # from .tasks import categorise_transactions

    process_transactions.delay(batch_id)
    return jsonify({"total_transactions": len(transactions_to_create), "batch_id": batch_id}), 201


def account_summary(account_id: int):
    """
    Endpoint to get summary of transactions for a given account and date range
    """
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date", datetime.now().date().isoformat())

    # Basic validation for date parameters
    if not start_date:
        return jsonify({"error": "The start_date query parameter is required"}), 400
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError as e:
        return jsonify({"error": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"}), 400
    if start_date_dt > end_date_dt:
        return jsonify({"error": "start_date cannot be after end_date"}), 400

    if not Account.query.filter_by(account_id=account_id).first():
        return jsonify({"error": f"Account with id {account_id} not found"}), 404

    transactions = Transaction.query.filter(
        Transaction.account_id == account_id,
        Transaction.date >= start_date_dt,
        Transaction.date <= end_date_dt,
    )
    total_transactions = transactions.count()
    total_spend = sum(abs(t.amount) for t in transactions if t.amount < 0)
    total_income = sum(t.amount for t in transactions if t.amount > 0)

    # Top 5 categories
    cat_counter = Counter()
    cat_spend = {}
    for t in transactions:
        if t.category:
            cat_counter[t.category] += 1
            if t.amount < 0:
                cat_spend[t.category] = cat_spend.get(t.category, 0) + abs(t.amount)
    top_categories = [
        {
            "category": cat,
            "total_spend": cat_spend.get(cat, 0),
            "transaction_count": cat_counter[cat],
        }
        for cat in sorted(cat_spend, key=cat_spend.get, reverse=True)[:5]
    ]
    # Processing status breakdown
    status_breakdown = Counter(t.ingestion_status for t in transactions)
    processing_status = {
        "pending": status_breakdown.get("pending", 0),
        "processing": status_breakdown.get("processing", 0),
        "completed": status_breakdown.get("completed", 0),
        "failed": status_breakdown.get("failed", 0),
    }
    summary = {
        "account_id": account_id,
        "date_range": {"start": start_date_dt, "end": end_date_dt},
        "metrics": {
            "total_transactions": total_transactions,
            "total_spend": total_spend,
            "total_income": total_income,
            "net": total_income - total_spend,
        },
        "top_categories": top_categories,
        "processing_status": processing_status,
    }
    return jsonify(summary)
