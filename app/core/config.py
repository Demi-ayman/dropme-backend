from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Drop Me Backend"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "sqlite:///./dropme.db"

    # Business rules (Task 2)
    MAX_RECYCLES_PER_DAY: int = 10

    class Config:
        env_file = ".env"


settings = Settings()