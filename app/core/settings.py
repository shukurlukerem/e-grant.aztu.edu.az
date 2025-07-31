from pydantic import BaseSettings

class Settings(BaseSettings):
    SMTP_SERVER: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()