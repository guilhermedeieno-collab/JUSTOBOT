"""
Configurações centrais da aplicação
"""
from functools import lru_cache
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas de variáveis de ambiente"""

    # Application
    APP_NAME: str = "JUSTOBOT"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://justobot:password@localhost:5432/justobot"
    )
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis (optional)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False

    # Security
    SECRET_KEY: str = Field(default="change-this-secret-key-in-production")
    API_KEY_HEADER: str = "X-API-Key"
    CORS_ORIGINS: list[str] = ["*"]

    # TJSP Configuration
    TJSP_BASE_URL: str = "https://esaj.tjsp.jus.br"
    TJSP_TIMEOUT: int = 30
    TJSP_MAX_RETRIES: int = 3
    TJSP_RATE_LIMIT: int = 10

    # Bulk Processing
    BULK_MAX_CONCURRENT_REQUESTS: int = 5
    BULK_BATCH_SIZE: int = 100
    BULK_TIMEOUT: int = 300

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Processa CORS origins de string ou lista"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância singleton das configurações"""
    return Settings()


# Instância global de configurações
settings = get_settings()
