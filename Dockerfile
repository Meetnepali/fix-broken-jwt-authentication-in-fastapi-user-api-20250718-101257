FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV JWT_SECRET=super-secret-key
ENV JWT_ALGORITHM=HS256

CMD ["/bin/bash", "-c", "source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000"]
