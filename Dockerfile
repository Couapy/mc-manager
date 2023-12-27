FROM python:3.11.5-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && apk add --no-cache tzdata
ENV TZ=Europe/Paris

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry==1.6.1 \
  && poetry config virtualenvs.create false \
  && apk add --no-cache libpq-dev \
  && apk add --no-cache --virtual .build-deps \
    build-base  \
  && poetry install --no-interaction --no-ansi \
  && apk add --no-cache \
    openjdk17 \
  && apk del .build-deps

COPY . ./

RUN python manage.py collectstatic --noinput

EXPOSE 80
CMD ["daphne", "project.asgi:application", "-b", "0.0.0.0", "-p", "80"]
