from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    category: str
    priority: str
    confidence: float | None
    assigned_team: str | None   # 👈 NEW

    class Config:
      from_attributes = True
