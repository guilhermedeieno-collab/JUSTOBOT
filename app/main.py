"""
Aplicação principal FastAPI
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import cases, bulk

# Importa tribunais para registrá-los automaticamente
from app.tribunals.tjsp import client as tjsp_client  # noqa

# Configuração de logging
setup_logging()

# Criação da aplicação
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    JUSTOBOT - Sistema de Consulta de Processos Judiciais

    API para consulta automatizada de processos em tribunais brasileiros.

    ## Funcionalidades

    * **Consultas individuais** - Busca por CPF, nome ou número do processo
    * **Processamento em lote** - Upload de planilhas para busca em massa
    * **Múltiplos tribunais** - Arquitetura extensível para adicionar novos tribunais

    ## Tribunais Disponíveis

    * TJSP - Tribunal de Justiça de São Paulo
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de todas as requisições"""
    start_time = time.time()

    # Processa requisição
    response = await call_next(request)

    # Calcula tempo
    process_time = time.time() - start_time

    # Log
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"duration={process_time:.3f}s"
    )

    # Adiciona header de tempo
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global de exceções"""
    logger.error(f"Erro não tratado: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "Erro interno do servidor"
        }
    )


# Rotas
app.include_router(cases.router, prefix=settings.API_PREFIX)
app.include_router(bulk.router, prefix=settings.API_PREFIX)


@app.get("/", tags=["root"])
async def root():
    """Endpoint raiz"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "docs": "/docs",
        "api": settings.API_PREFIX
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar a aplicação"""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} iniciado")
    logger.info(f"Ambiente: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Executado ao encerrar a aplicação"""
    logger.info(f"{settings.APP_NAME} encerrado")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
