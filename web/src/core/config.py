from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SECRET_KEY: str
    ACTIVATION_CODE_TTL: int = 3600  # 1 час
    TOKEN_TTL: int = 30  # 30 дней
    
    ANALYTICS_SERVICE_URL: str
    ANALYTICS_API_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings() 