FROM python:3.11.4-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install

COPY booking_app .
