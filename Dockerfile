# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install bash
RUN apt-get update && apt-get install -y bash

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copy project
COPY . /app/

WORKDIR /app

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "strategyapp.wsgi:application"]