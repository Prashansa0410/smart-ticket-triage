from sqlalchemy.orm import Session
from app.models import Ticket
from app.schemas import TicketCreate
from app.celery_worker import run_ml_task


def create_ticket(ticket: TicketCreate, db: Session):
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        status="OPEN",
        category="PENDING",
        priority="PENDING"
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    try:
        run_ml_task.delay(
            db_ticket.id,
            f"{db_ticket.title} {db_ticket.description}"
        )
    except Exception as e:
        print("Celery unavailable, skipping async ML:", e)

    return db_ticket


def get_ticket_by_id(db: Session, ticket_id: int) -> Ticket | None:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()
