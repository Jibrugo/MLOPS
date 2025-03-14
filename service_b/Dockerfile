FROM python:3.11-slim

RUN pip install fastapi uvicorn databases[asyncpg]

COPY main.py /app/main.py
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
