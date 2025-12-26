import os

# MySQL credentials (read from environment variables)
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "rootpassword")  # default password if not set
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")  # <-- Use container name for Docker
MYSQL_DB = os.getenv("MYSQL_DB", "sentiment_db")

# SQLAlchemy database URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
