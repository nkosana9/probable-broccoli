# Project Overview
This project is a Flask-based web application designed to handle the bulk ingestion of financial transactions - whic hare then categorized and reported on.  
The application provides RESTful API endpoints to ingest transactions and generate reports based on the ingested data. Once ingested, transactions are processed asynchronously using Celery, which allows for efficient handling of large volumes of data without blocking the main application.

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
Edit the `base.env` file to set your `AUTH_TOKEN` and any other environment variables as needed.

Then, run the following command in the terminal:

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

### 3. Running the sample API requests

With everything setup, you can now make API requests to your Flask app. 

A script with sample API requests is provided in `sample_requests.sh`. You can run it to test the endpoints:

```bash
chmod +x sample_requests.sh
./sample_requests.sh <YOUR_AUTH_TOKEN_HERE>
```


The endpoints may also be called manually.

For example, to ingest bulk transactions:

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
                "currency": "ZAR",
                "date": "2026-01-01T12:34:56Z",
                "merchant_name": "Amazon",
                "description": "Amazon purchase"
            }
        ]
    }'
```

To get an account summary:

```bash
curl "http://localhost:8080/api/reports/account/acc_12345/summary/?start_date=2026-01-01&end_date=2026-01-31"
```

