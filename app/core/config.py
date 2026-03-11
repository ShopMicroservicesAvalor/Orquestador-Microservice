# app/config/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configuration
    db_host: str
    db_name: str
    db_user: str
    db_password: str
    db_port: int

    # RabbitMQ — ADD THESE
    rabbitmq_user: str
    rabbitmq_pass: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def database_url_sync(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
