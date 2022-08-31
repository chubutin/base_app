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
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT'))
    db_name = os.getenv('APP_DB_NAME')
    db_username = os.getenv('APP_DB_USER')
    db_password = os.getenv('APP_DB_PASS')
    db_string_connection = f"postgresql://{db_username}:{db_password}@" \
                           f"{db_host}:{db_port}/{db_name}"
    email_host = os.getenv('EMAIL_HOST', 'app_mail')
    email_port = int(os.getenv('EMAIL_PORT', 1025))
    email_host_user = ''
    email_host_password = ''
    email_host_api_key = ''
    email_use_tls = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
    email_from = 'shamoungolf@app.com'
    email_templates_base_paths = os.getenv('EMAIL_TEMPLATES_BASE_PATH').split(',')
    base_url = os.getenv('BASE_URL', 'http://localhost:3000')
    base_activation_email_link = os.getenv('BASE_ACTIVATION_EMAIL_LINK', f'{base_url}/users/activate?activation_code=')
    email_template_name_user_activation = 'activate_account.html'


