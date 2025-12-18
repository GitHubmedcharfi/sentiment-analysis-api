from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000))
    sentiment = Column(String(10))
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
