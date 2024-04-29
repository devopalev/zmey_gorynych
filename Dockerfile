FROM python:3.12-slim-bullseye as tester

ENV POETRY_VERSION=1.8.2 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/dist

RUN /bin/sh -c set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends postgresql-contrib gcc python3-dev

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /dist
COPY --chown=postgres --chmod=777 backend ./backend
COPY --chown=postgres --chmod=777 migrations ./migrations
COPY --chown=postgres --chmod=777 tests ./tests
COPY --chown=postgres --chmod=777 pyproject.toml poetry.lock yoyo.ini app.py settings.py pytest.ini ./

# Install dependencies
RUN poetry export --output requirements.txt --without-hashes --with-credentials --with main,test \
    && pip install -r requirements.txt

# Run tests
RUN su postgres -c 'pytest'

FROM tester as builder_dep

RUN poetry export --output requirements_main.txt --without-hashes --with-credentials --only main
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /dist/wheels -r requirements_main.txt

FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/dist \
    LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8

WORKDIR /dist

RUN pip install --upgrade pip
COPY --from=builder_dep /dist/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY backend ./backend
COPY migrations ./migrations
COPY app.py settings.py ./
CMD ["python", "app.py"]