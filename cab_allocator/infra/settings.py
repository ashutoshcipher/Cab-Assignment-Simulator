"""Application configuration via environment variables."""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Runtime configuration for the simulator."""

    max_eta_km: float = 5.0

settings = Settings()
