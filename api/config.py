from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URI: str = "https://w3id.org/fair-enough"
    # API_URL: str = f"http://localhost:8000"


settings = Settings()
