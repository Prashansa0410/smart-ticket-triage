from sqlalchemy.orm import Session
from datetime import datetime

from app.models import Ticket
from app.schemas import TicketCreate
from app.ml.ml_classifier import classify
from app.celery_worker import run_ml_task

def create_ticket(ticket: TicketCreate, db: Session):
    # 1️⃣ Save ticket to DB
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        status="OPEN",
        category="PENDING",
        priority="PENDING"
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)   # 🔥 THIS GETS THE ID

    # 2️⃣ Send DB ticket ID to Celery
    try:
        run_ml_task.delay(
            db_ticket.id,
            f"{db_ticket.title} {db_ticket.description}"
        )
    except Exception as e:
        print("Celery unavailable, skipping async ML:", e)

    return db_ticket

def assign_team(category: str, confidence: float | None) -> str:
    """
    Decide which team should handle the ticket
    """

    if confidence is not None and confidence < 0.6:
        return "MANUAL_REVIEW"

    if category == "Payments":
        return "PAYMENTS_TEAM"

    if category == "Login":
        return "IDENTITY_TEAM"

    if category == "Technical":
        return "TECH_SUPPORT"

    return "GENERAL_SUPPORT"

def get_ticket_by_id(db: Session, ticket_id: int) -> Ticket | None:
    """
    Fetch a ticket by ID.
    Returns None if not found.
    """

    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def run_ml_and_update_ticket(db: Session, ticket_id: int, text: str):
    """
    Background task:
    - Run ML
    - Update ticket with category, priority, confidence
    """
    result = classify(text)

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return

    ticket.category = result["category"]
    ticket.priority = result["priority"]
    ticket.confidence = result.get("confidence")

    db.commit()


    
