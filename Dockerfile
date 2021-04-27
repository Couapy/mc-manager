FROM python:3.9.4-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip -q install -r requirements.txt
RUN apt-get -qq update && apt-get -yqq install default-jre
