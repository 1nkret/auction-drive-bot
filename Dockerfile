FROM python:3.13-slim

RUN apt-get update &&  \
    apt-get install -y curl libpq-dev gcc && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s ~/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false &&  \
    poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["python", "main.py"]
