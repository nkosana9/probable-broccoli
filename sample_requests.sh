#!/bin/bash

# Test Data Ingestion Script
# Sends multiple test batches with various transaction types for categorization

BASE_URL="http://localhost:8080"
TOKEN=$1

echo "🚀 Starting test data ingestion..."
echo ""

# Test 1: Basic ingestion with various merchants
echo "📦 Test 1: Ingesting batch with various transaction categories..."
curl -X POST "$BASE_URL/accounts/bulk-ingestion" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "accounts": [
      {
        "account_id": "acc_001",
        "name": "John Doe",
        "type": "checking"
      },
      {
        "account_id": "acc_002",
        "name": "Jane Smith",
        "type": "savings"
      }
    ],
    "transactions": [
      {
        "transaction_id": "txn_001",
        "account_id": "acc_001",
        "amount": -50.75,
        "currency": "ZAR",
        "date": "2026-01-01T12:34:56Z",
        "merchant_name": "Amazon",
        "description": "Amazon - Books and Electronics"
      },
      {
        "transaction_id": "txn_002",
        "account_id": "acc_001",
        "amount": -14.99,
        "currency": "ZAR",
        "date": "2026-01-02T10:15:00Z",
        "merchant_name": "Netflix",
        "description": "Monthly streaming subscription"
      },
      {
        "transaction_id": "txn_003",
        "account_id": "acc_001",
        "amount": -45.00,
        "currency": "ZAR",
        "date": "2026-01-03T08:30:00Z",
        "merchant_name": "Udemy",
        "description": "Online course subscription"
      },
      {
        "transaction_id": "txn_004",
        "account_id": "acc_001",
        "amount": 3500.00,
        "currency": "ZAR",
        "date": "2026-01-05T09:00:00Z",
        "merchant_name": "Stripe",
        "description": "Monthly salary deposit"
      },
      {
        "transaction_id": "txn_005",
        "account_id": "acc_001",
        "amount": -32.50,
        "currency": "ZAR",
        "date": "2026-01-06T15:20:00Z",
        "merchant_name": "Uber",
        "description": "Ride to downtown"
      },
      {
        "transaction_id": "txn_006",
        "account_id": "acc_002",
        "amount": -89.99,
        "currency": "ZAR",
        "date": "2026-01-04T11:45:00Z",
        "merchant_name": "Takealot",
        "description": "Household items"
      },
      {
        "transaction_id": "txn_007",
        "account_id": "acc_002",
        "amount": 1200.00,
        "currency": "ZAR",
        "date": "2026-01-05T10:00:00Z",
        "merchant_name": "PayPal",
        "description": "Freelance income"
      },
      {
        "transaction_id": "txn_008",
        "account_id": "acc_002",
        "amount": -25.00,
        "currency": "ZAR",
        "date": "2026-01-07T14:30:00Z",
        "merchant_name": "Disney",
        "description": "Disney+ renewal"
      }
    ]
  }' 2>/dev/null | jq '.'
echo ""
echo "✅ Batch 1 sent!"
echo ""

# Test 2: Additional transactions for account_001
echo "📦 Test 2: Ingesting additional transactions for existing account..."
curl -X POST "$BASE_URL/accounts/bulk-ingestion" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \  
  -d '{
    "accounts": [],
    "transactions": [
      {
        "transaction_id": "txn_009",
        "account_id": "acc_001",
        "amount": -16.99,
        "currency": "ZAR",
        "date": "2026-01-08T19:00:00Z",
        "merchant_name": "Spotify",
        "description": "Music streaming subscription"
      },
      {
        "transaction_id": "txn_010",
        "account_id": "acc_001",
        "amount": -120.00,
        "currency": "ZAR",
        "date": "2026-01-09T13:15:00Z",
        "merchant_name": "DataCamp",
        "description": "Data science course"
      },
      {
        "transaction_id": "txn_011",
        "account_id": "acc_001",
        "amount": -18.50,
        "currency": "ZAR",
        "date": "2026-01-10T09:30:00Z",
        "merchant_name": "Bolt",
        "description": "Ride-sharing service"
      },
      {
        "transaction_id": "txn_012",
        "account_id": "acc_001",
        "amount": -250.00,
        "currency": "ZAR",
        "date": "2026-01-11T16:45:00Z",
        "merchant_name": "Bash",
        "description": "Clothing purchase"
      },
      {
        "transaction_id": "txn_013",
        "account_id": "acc_001",
        "amount": -250.00,
        "currency": "ZAR",
        "date": "2026-01-11T16:45:00Z",
        "merchant_name": "EFT",
        "description": "Transcation with unknown merchant/description"
      }
    ]
  }' 2>/dev/null | jq '.'
echo ""
echo "✅ Batch 2 sent!"
echo ""

# Test 3: Query account summary
echo "📊 Test 3: Fetching account summary for acc_001..."
curl -s -X GET "$BASE_URL/accounts/acc_001/summary?start_date=2026-01-01&end_date=2026-01-30" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq '.'
echo ""

echo "🎉 Test data ingestion completed!"