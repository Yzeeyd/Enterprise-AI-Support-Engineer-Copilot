FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/__init__.py ./app/__init__.py
COPY app/backend ./app/backend

COPY data/raw ./data/raw

RUN mkdir -p /app/runtime

EXPOSE 8000

CMD ["uvicorn","app.backend.main:app","--host","0.0.0.0","--port","8000"]