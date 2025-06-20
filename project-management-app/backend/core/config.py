from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Project Management Platform"
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    SECRET_KEY: str = "your-super-secret-key-for-jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # Add other settings as needed

    class Config:
        env_file = ".env"

settings = Settings()
