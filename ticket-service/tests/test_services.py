from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Ticket
from app.schemas import TicketCreate
from app.services import create_ticket


# Create in-memory database for testing
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def test_create_ticket_sets_default_values():
    db = SessionLocal()

    ticket_data = TicketCreate(
        title="Payment failed",
        description="Money debited but not credited"
    )

    ticket = create_ticket(db, ticket_data)

    assert ticket.id is not None
    assert ticket.status == "OPEN"
    assert ticket.category == "UNKNOWN"
    assert ticket.priority == "UNKNOWN"

    db.close()
