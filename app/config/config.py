from pydantic_settings import BaseSettings
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # Lokasi file ini
ENV_PATH = os.path.join(BASE_PATH, '..', '.env') 

class Settings(BaseSettings):
    FIREBASE_CREDENTIALS_PATH: str  # nama field di class Settings harus sama persis dengan nama variabel di .env (case-insensitive)
    class Config:
        env_file = ENV_PATH

settings = Settings()