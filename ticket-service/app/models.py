from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Float
from sqlalchemy import Column, String

Base = declarative_base()


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    status = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=True)
    assigned_team = Column(String(50), nullable=True)
    

    created_at = Column(DateTime, default=datetime.utcnow)
