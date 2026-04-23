# Docker Setup for the Project

This docker-compose setup provides a complete development environment with:
- **Redis**: Cache and message broker for Celery
- **Flask**: Web application server
- **Celery**: Task queue worker

## Prerequisites

- Docker and Docker Compose installed
- Port 8080 (Flask) and 6379 (Redis) available

## Quick Start

### 1. Build and Start Services

```bash
docker-compose up -d
```

This will:
- Build the Docker image for your Flask app
- Start Redis, Flask app, and Celery worker
- Run migrations automatically
- Start the Flask development server on `http://localhost:8080`

### 2. Verify Services

Check that all services are running:

```bash
docker-compose ps
```

### 3. Making Requests

With everything setup, you can now make API requests to your Flask app. For example, to ingest bulk transactions:

```bash
curl -X POST "http://localhost:8080/api/ingestion/accounts/bulk" \
    -H "Content-Type: application/json" \
    -d '{
        "accounts": [
            {
                "account_id": "acc_123",
                "name": "John Doe",
                "type": "checking"
            }
        ],
        "transactions": [
            {
                "transaction_id": "txn_456",
                "account_id": "acc_123",
                "amount": -50.75,
                "currency": "USD",
                "date": "2024-06-01T12:34:56Z",
                "merchant_name": "Amazon",
                "description": "Amazon purchase"
            }
        ]
    }'
```

To get an account summary:

```bash
curl "http://localhost:8080/api/reports/account/acc_12345/summary/?start_date=2025-10-01&end_date=2026-01-01"
```

