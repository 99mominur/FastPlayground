from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # fastapi settings
    SECRET_KEY: str = "its_a_secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: str = 5432
    DB_NAME: str = "fastapi"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    class Config:
        env_file = ".env"


settings = Settings()
