from pydantic import BaseModel
from datetime import datetime

class FeedbackRequest(BaseModel):
    text: str

class FeedbackResponse(BaseModel):
    sentiment: str
    score: float

class FeedbackDB(BaseModel):
    id: int
    text: str
    sentiment: str
    score: float
    created_at: datetime

    class Config:
        orm_mode = True
