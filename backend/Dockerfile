FROM tiangolo/uvicorn-gunicorn:python3.9 as BASE

WORKDIR /golf_app

COPY requirements.txt ./

COPY requirements-dev.txt ./


ENV PYTHONPATH=/golf_app/app

ENV APP_MODULE="app.main:app"

# ============================== SHARED BASE ============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Install OS dependencies for build purposes only
    gcc=4:10.2.* \
    python3-dev=3.9.* \
    libpq-dev=13.* && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc python3-dev && \
    apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements-dev.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./app ./app/
COPY ./email_resources ./email_resources/

EXPOSE 3000

# ============================== DEVELOPMENT/TEST ============================

FROM base AS dev

COPY ./tests ./tests/
COPY pytest.ini ./