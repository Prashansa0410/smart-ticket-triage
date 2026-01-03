@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3}
)
def run_ml_task(self, ticket_id: int, text: str):
    db = SessionLocal()
    try:
        result = classify(text)

        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return

        ticket.category = result["category"]
        ticket.priority = result["priority"]
        ticket.confidence = result.get("confidence")

        ticket.assigned_team = assign_team(
            ticket.category,
            ticket.confidence
        )

        db.commit()   # 

    finally:
        db.close()    # 
