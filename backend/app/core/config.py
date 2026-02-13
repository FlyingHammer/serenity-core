from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FX Scanner MVP"
    database_url: str = "sqlite:///./fx_scanner.db"
    data_dir: str = "backend/data"
    scheduler_interval_seconds: int = 60


settings = Settings()
