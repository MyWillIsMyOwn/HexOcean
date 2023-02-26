# Base image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    gcc \
    libc-dev \
    linux-headers \
    postgresql-dev \
    && apk add --no-cache \
    postgresql-client \
    curl



# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the code into the container
COPY . /code/
WORKDIR /code/HexOcean


# Expose the port
EXPOSE 8000

