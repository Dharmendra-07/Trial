import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

    # Flask-Security configuration
    SECURITY_PASSWORD_HASH = 'argon2'
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False  # disable email sending for local testing

class ProductionConfig(BaseConfig):
    DEBUG = False
    # You can add production database here, e.g.
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')