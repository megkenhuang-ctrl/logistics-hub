FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY . /app

# Ensure database is initialized
RUN python init_db.py

# Expose default port
EXPOSE 5000

ENV PORT=5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "server.py"]
