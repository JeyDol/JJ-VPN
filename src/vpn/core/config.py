from dulwich.midx import HASH_ALGORITHM_SHA256
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DATABASE_URL: str | None = None

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_URL:str
    DEBUG: bool = False

    XRAY_SERVER_ADDRESS: str = Field(..., env="XRAY_SERVER_ADDRESS")
    XRAY_SERVER_PORT: int = Field(default=443, env="XRAY_SERVER_PORT")
    XRAY_PUBLIC_KEY: str = Field(..., env="XRAY_PUBLIC_KEY")
    XRAY_SHORT_ID: str = Field(..., env="XRAY_SHORT_ID")
    XRAY_SNI: str = Field(default="www.google.com", env="XRAY_SNI")
    XRAY_FINGERPRINT: str = Field(default="chrome", env="XRAY_FINGERPRINT")

    def __init__(self, **values):
        super().__init__(**values)
        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
