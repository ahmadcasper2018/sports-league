# Use the official Python base image with slim-buster
FROM python:3.11-slim-buster

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

COPY ./wait-for.sh /usr/bin
COPY ./entrypoint.sh /usr/bin
# Copy the entire project directory to the container
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/bin/entrypoint.sh"]

