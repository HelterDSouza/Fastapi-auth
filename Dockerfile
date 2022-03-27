FROM python:3.10.2-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./

RUN pip install poetry==1.1.13 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev


COPY . ./

CMD poetry run alembic upgrade head && \
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000