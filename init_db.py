from sqlalchemy import create_engine
from app.models.db_models import Base
from app.config import DATABASE_URL

# Create a database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables defined in SQLAlchemy models
Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
