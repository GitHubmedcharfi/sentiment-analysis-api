FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_app.txt .
RUN pip install --no-cache-dir -r requirements_app.txt

# Copy ML models
COPY ml_models/ml_models/model.pkl ./ml_models/ml_models/
COPY ml_models/ml_models/tokenizer.pkl ./ml_models/ml_models/  

COPY app ./app
COPY init_db.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]