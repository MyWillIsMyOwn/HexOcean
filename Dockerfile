FROM python:3.11-alpine

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN \
apk add --no-cache python3 postgresql-libs && \
apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
libmagic && \
pip install -r requirements.txt 
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]