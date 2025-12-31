# Smart Ticket Triage System

An end-to-end **Smart Support Ticket Triage System** built using **FastAPI, SQLAlchemy, Machine Learning, Celery, and Redis**.  
The system automatically classifies, prioritizes, and assigns support tickets **asynchronously**, similar to real-world production systems.

---

## Problem Statement

Support teams receive a large number of tickets daily such as:
- Payment failures
- Login issues
- Technical problems

Manual triage is slow, error-prone, and does not scale well.

 This system automates ticket triage using **Machine Learning + business rules** while keeping APIs fast and scalable.

---

##  Key Features

- Create and fetch support tickets
- Automatic ticket classification (ML + rules)
- Priority assignment
- Confidence score for predictions
- Asynchronous processing using Celery + Redis
- Team assignment logic
- Clean, modular, testable architecture

---

## High-Level Architecture

Client
↓
FastAPI (Ticket Service)
↓
Database (SQLite for local dev)
↓
Redis (Message Queue)
↓
Celery Worker
↓
ML Classification + Assignment Logic
↓
Database Update


---

##  Tech Stack

| Layer | Technology |
|------|-----------|
| API | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (development) |
| Async Queue | Redis |
| Worker | Celery |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| Testing | Pytest |
| API Docs | Swagger / OpenAPI |

---

##  Machine Learning Approach

### Model
- TF-IDF Vectorization
- Logistic Regression

### Hybrid Strategy
1. Rule-based override for high-confidence keywords
2. ML fallback for ambiguous cases
3. Confidence threshold for manual review

---

##  Asynchronous Processing

To avoid blocking API requests:
- Tickets are created immediately
- ML classification runs asynchronously
- Ticket is updated in the background

This improves performance, reliability, and scalability.

---

##  Ticket Lifecycle

1. Ticket created via API
2. Ticket stored with `PENDING` classification
3. ML job pushed to Redis
4. Celery worker processes the ticket
5. Category, priority, confidence updated
6. Ticket assigned to the correct team

---

##  Assignment Logic

| Condition | Assigned Team |
|---------|---------------|
| Low confidence | MANUAL_REVIEW |
| Payments | PAYMENTS_TEAM |
| Login | IDENTITY_TEAM |
| Technical | TECH_SUPPORT |
| Default | GENERAL_SUPPORT |

---

##  Example API Flow

### Create Ticket
```http
POST /tickets

{
  "title": "Payment failed",
  "description": "Amount debited but not credited"
}

Immediate Response
{
  "status": "OPEN",
  "category": "PENDING",
  "priority": "PENDING",
  "confidence": null
}


After Async Processing
{
  "category": "Payments",
  "priority": "High",
  "confidence": 1.0,
  "assigned_team": "PAYMENTS_TEAM"
}

Testing

Unit tests for business logic

API tests using FastAPI TestClient
pytest


Project Structure
ticket-service/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   ├── ml/
│   │   └── ml_classifier.py
│   ├── celery_app.py
│   └── celery_worker.py
├── tests/
├── requirements.txt
└── README.md

Running Locally

Start Redis
redis-server

Start Celery Worker
celery -A app.celery_app worker --loglevel=info

Start FastAPI
python -m uvicorn app.main:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs

Future Improvements

Separate Assignment Service

PostgreSQL instead of SQLite

Monitoring & metrics

Dead-letter queue

Docker & Kubernetes deployment

Live Demo: https://smart-ticket-triage.onrender.com/docs