FROM python:3.12.2-slim as base

ENV \
  PYTHONFAULTHANDLER=TRUE \
  PYTHONUNBUFFERED=TRUE \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
COPY README.md "$PYSETUP_PATH/README.md"

FROM base as builder

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl

# install poetry
ARG POETRY_VERSION="1.7.1"
RUN curl -sSL https://install.python-poetry.org | python -

# standard python project
WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock ./
RUN poetry install -vvv --no-root --only main

FROM base as final

# permit http service
WORKDIR /app
ENV PORT 8000
EXPOSE $PORT

# copy dependencies from builder layer
COPY --from=builder $VENV_PATH $VENV_PATH

# copy files
COPY src ./


CMD gunicorn app.wsgi --bind 0.0.0.0:${PORT}

HEALTHCHECK CMD python3 -c "from http import client; c=client.HTTPConnection('localhost', ${PORT}, timeout=2); c.request('GET', '/admin'); r=c.getresponse(); print(r.read()); exit(r.status != 200)"
