"""
Configuração de logging
"""
import sys
from loguru import logger
from app.core.config import settings


def setup_logging():
    """Configura o sistema de logging"""
    logger.remove()  # Remove handler padrão

    # Configuração baseada no ambiente
    if settings.LOG_FORMAT == "json":
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level=settings.LOG_LEVEL,
            serialize=True
        )
    else:
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=settings.LOG_LEVEL,
            colorize=True
        )

    # Log em arquivo para produção
    if settings.ENVIRONMENT == "production":
        logger.add(
            "logs/app_{time:YYYY-MM-DD}.log",
            rotation="00:00",
            retention="30 days",
            level="INFO",
            serialize=True
        )

    return logger
