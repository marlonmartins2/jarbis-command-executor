import os

import spacy

from dotenv import load_dotenv

load_dotenv()


# Application settings
APP_NAME: str = os.getenv('APP_NAME')
APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION')
CORS_ORIGINS: list = os.getenv('CORS_ORIGINS')
DEBUG: bool = os.getenv('DEBUG')


# Database settings
MONGO_URL: str = os.getenv("MONGO_URL")
MONGO_SSL: bool = os.getenv("MONGO_SSL")
PATH_CERT: str = os.getenv("PATH_CERT")
DATABASE_ENVIRONMENT: str = os.getenv("DATABASE_ENVIRONMENT")


# # External Services settings
WEATHER_API_KEY: str = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL: str = os.getenv('WEATHER_API_URL')

SPACY = spacy.load("pt_core_news_sm")
