import os

from config import secret

__all__ = (
    'TestConfig',
    'DevelopmentConfig',
    'StagingConfig',
    'ProductionConfig',
)


class Config(object):
    ENV = 'DEFAULT'
    NAME = 'FLASK-SQLALCHEMY'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = os.path.join(PROJECT_ROOT, 'app', 'static')
    TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'app', 'templates')
    UPLOAD_DIR = os.path.join(STATIC_DIR, 'upload')
    SECRET = secret.SECRET
    SQLALCHEMY_DATABASE_URI = secret.SQLALCHEMY_DATABASE_URL
    SQLALCHEMY_ECHO = False
    API_SCHEME = 'http'
    API_HOST = '127.0.0.1'
    API_PORT = 5000
    CORS = dict(
        resources={'/*': {'origins': "*"}},
        supports_credentials=True,
        expose_headers="Set-Cookie",
    )
    DEFAULT_ACCESS_TOKEN_EXPIRATION_TIME = 60 * 60 * 24 * 7


class TestConfig(Config):
    ENV = 'TEST'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = secret.TEST_SQLALCHEMY_DATABASE_URL


class DevelopmentConfig(Config):
    ENV = 'DEVELOPMENT'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class StagingConfig(Config):
    ENV = 'STAGING'
    DEBUG = False


class ProductionConfig(Config):
    ENV = 'PRODUCTION'
    DEBUG = False
