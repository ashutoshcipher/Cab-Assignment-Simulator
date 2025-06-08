from pydantic import BaseSettings

class Settings(BaseSettings):
    max_eta_km: float = 5.0

settings = Settings()
