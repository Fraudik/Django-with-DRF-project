FROM python:3.9-slim-bullseye AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# builder-base is used to build dependencies
FROM python-base AS builder-base
RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        libpq-dev \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry wtih respect to $POETRY_VERSION and $POETRY_HOME
ENV POETRY_VERSION=1.5.1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry

# Copy Python requirements to cache them and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-root

# 'production' stage uses the clean 'python-base' stage and copyies in only our runtime deps from 'builder-base'
FROM python-base AS production

COPY --from=builder-base $VENV_PATH $VENV_PATH

# Create user with the name poetry
RUN groupadd -g 1500 poetry && \
    useradd -m -u 1500 -g poetry poetry
RUN apt-get update && apt-get install -y libpq-dev
COPY --chown=poetry:poetry ./ /
USER poetry

WORKDIR /app

RUN . /opt/pysetup/.venv/bin/activate
