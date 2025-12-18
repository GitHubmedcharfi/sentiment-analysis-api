from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.db_models import Base, Feedback
from app.config import DATABASE_URL

# Create engine with SQLite specific connect_args
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

# Create all tables (only once)
Base.metadata.create_all(bind=engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD: save feedback
def save_feedback(db: Session, text: str, sentiment: str, score: float):
    fb = Feedback(text=text, sentiment=sentiment, score=score)
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

# Get feedback by ID
def get_feedback(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

# Get all feedbacks
def get_all_feedbacks(db: Session):
    return db.query(Feedback).all()

# Get feedbacks by sentiment
def get_feedbacks_by_sentiment(db: Session, sentiment: str):
    return db.query(Feedback).filter(Feedback.sentiment == sentiment).all()

# Delete feedback by ID
def delete_feedback(db: Session, feedback_id: int):
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if fb:
        db.delete(fb)
        db.commit()
        return True
    return False

# Delete all feedbacks
def delete_all_feedbacks(db: Session):
    db.query(Feedback).delete()
    db.commit()
