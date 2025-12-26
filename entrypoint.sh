#!/bin/sh
set -e

echo "Waiting for MySQL..."

MAX_RETRIES=30
RETRY_COUNT=0

until python - <<EOF
import pymysql, os, sys
try:
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        connect_timeout=5
    )
    conn.close()
    print("Successfully connected to MySQL!", flush=True)
    sys.exit(0)
except Exception as e:
    print(f"Connection failed: {e}", flush=True)
    sys.exit(1)
EOF
do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "Failed to connect to MySQL after $MAX_RETRIES attempts"
    exit 1
  fi
  echo "Retry $RETRY_COUNT/$MAX_RETRIES..."
  sleep 2
done

echo "MySQL is ready. Initializing database..."

python init_db.py

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000