import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY no está configurada en las variables de entorno")

    # Base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL')

    if DATABASE_URL:
        # Producción (Railway, Heroku, etc.)
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

        # Extraer la expresión condicional anidada
        if "sslmode" not in DATABASE_URL:
            ssl_separator = "?" if "?" not in DATABASE_URL else "&"
            SQLALCHEMY_DATABASE_URI = f"{DATABASE_URL}{ssl_separator}sslmode=require"
        else:
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Desarrollo local
        DB_USER = os.environ.get('DB_USER')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        DB_HOST = os.environ.get('DB_HOST')
        DB_PORT = os.environ.get('DB_PORT')
        DB_NAME = os.environ.get('DB_NAME')

        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY no está configurada en las variables de entorno")

    # Logs
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'False').lower() == 'true'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}