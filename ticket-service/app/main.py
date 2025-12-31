from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine
from app.models import Base
from app.schemas import TicketCreate, TicketResponse
from app.services import create_ticket
from app.services import get_ticket_by_id
from fastapi import HTTPException
from app.services import run_ml_and_update_ticket
from fastapi import FastAPI, Depends
from app.celery_worker import run_ml_task
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket_api(ticket: TicketCreate, db: Session = Depends(get_db)):
    created_ticket = create_ticket(db, ticket)

    text = f"{created_ticket.title} {created_ticket.description}"

    # Send job to Redis queue
    try:
        run_ml_task.delay(ticket.id, text)
    except Exception as e:
        print("Celery unavailable, skipping async ML:", e)


    return created_ticket



@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket
