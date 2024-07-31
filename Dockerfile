FROM python:3.12-alpine

LABEL authors="Berestianyi Ivan"

RUN apk add --no-cache build-base libjpeg-turbo-dev zlib-dev libffi-dev && \
    pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY . /app

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]