from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
