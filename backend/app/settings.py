import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    appName: str = "GolfApp Demo"
    openapi_url: str = ''
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm = "HS256"
    access_token_expire_minutes = 30
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('APP_DB_NAME')
    db_username = os.getenv('APP_DB_USER')
    db_password = os.getenv('APP_DB_PASS')
    db_string_connection = f"postgresql://{db_username}:{db_password}@" \
                           f"{db_host}:{db_port}/{db_name}"
