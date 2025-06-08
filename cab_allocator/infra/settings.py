from datetime import datetime
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    max_eta_day_km: float = 5.0
    max_eta_night_km: float = 8.0

    def max_eta_km_for(self, timestamp: float) -> float:
        """Return ``max_eta`` in kilometres based on the given timestamp."""
        hour = datetime.fromtimestamp(timestamp).hour
        if 22 <= hour or hour < 6:
            return self.max_eta_night_km
        return self.max_eta_day_km

settings = Settings()
