# Multi-stage build para otimizar tamanho da imagem

FROM python:3.11-slim as builder

# Variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Imagem final
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Criar usuário não-root
RUN useradd -m -u 1000 justobot && \
    mkdir -p /app /app/logs && \
    chown -R justobot:justobot /app

# Copiar dependências do builder
COPY --from=builder /root/.local /home/justobot/.local

# Configurar PATH
ENV PATH=/home/justobot/.local/bin:$PATH

# Definir diretório de trabalho
WORKDIR /app

# Copiar código da aplicação
COPY --chown=justobot:justobot . .

# Mudar para usuário não-root
USER justobot

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
