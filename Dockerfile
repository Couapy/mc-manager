FROM python:3.9.4-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt update && apt install default-jre -y

# Initialize projet
COPY . .
RUN mkdir var
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput
# RUN python manage.py updatemclist
