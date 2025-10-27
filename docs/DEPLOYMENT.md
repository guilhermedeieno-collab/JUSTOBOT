# Guia de Deploy - JUSTOBOT

## Deploy Local (Desenvolvimento)

### 1. Pré-requisitos

- Python 3.11+
- PostgreSQL 14+
- Redis (opcional)

### 2. Setup

```bash
# Clone o repositório
git clone <repo-url>
cd JUSTOBOT

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis
cp .env.example .env
# Edite .env com suas configurações
```

### 3. Inicie o servidor

```bash
# Modo desenvolvimento
uvicorn app.main:app --reload

# Ou use make
make dev
```

## Deploy com Docker

### 1. Build e Start

```bash
# Build das imagens
docker-compose build

# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f api
```

### 2. Verificar Health

```bash
curl http://localhost:8000/health
```

### 3. Parar serviços

```bash
docker-compose down

# Com volumes
docker-compose down -v
```

## Deploy em Produção

### AWS (EC2 + RDS + ElastiCache)

#### 1. Configurar RDS (PostgreSQL)

```bash
# Criar instância RDS
aws rds create-db-instance \
  --db-instance-identifier justobot-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username justobot \
  --master-user-password <senha> \
  --allocated-storage 20
```

#### 2. Configurar ElastiCache (Redis)

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id justobot-cache \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

#### 3. Deploy EC2

```bash
# Criar instância EC2
# Instalar Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start

# Clone e build
git clone <repo-url>
cd JUSTOBOT

# Configurar .env com endpoints AWS
# RDS endpoint para DATABASE_URL
# ElastiCache endpoint para REDIS_URL

# Deploy
docker-compose up -d
```

#### 4. Configurar NGINX

```nginx
server {
    listen 80;
    server_name api.justobot.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Google Cloud (Cloud Run)

#### 1. Build da imagem

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/justobot
```

#### 2. Deploy

```bash
gcloud run deploy justobot \
  --image gcr.io/PROJECT_ID/justobot \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL=<url>,REDIS_URL=<url>
```

### Azure (App Service)

```bash
# Login
az login

# Criar resource group
az group create --name justobot-rg --location eastus

# Criar App Service
az webapp create \
  --resource-group justobot-rg \
  --plan justobot-plan \
  --name justobot-api \
  --runtime "PYTHON:3.11"

# Deploy
az webapp up --name justobot-api
```

### Heroku

```bash
# Login
heroku login

# Criar app
heroku create justobot-api

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Adicionar Redis
heroku addons:create heroku-redis:hobby-dev

# Deploy
git push heroku main

# Configurar variáveis
heroku config:set ENVIRONMENT=production
```

## Configurações de Produção

### Variáveis de Ambiente

```bash
# .env.production
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<gerar-chave-segura>

DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
REDIS_ENABLED=True

# Segurança
CORS_ORIGINS=https://seu-dominio.com

# Performance
BULK_MAX_CONCURRENT_REQUESTS=10
BULK_BATCH_SIZE=100

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Gerar SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(32))
```

## Monitoramento

### 1. Logs

```bash
# Docker
docker-compose logs -f api

# Kubernetes
kubectl logs -f deployment/justobot

# Produção - usar serviços como:
# - CloudWatch (AWS)
# - Stackdriver (GCP)
# - Application Insights (Azure)
```

### 2. Métricas

Integrar com:
- Prometheus + Grafana
- DataDog
- New Relic

### 3. Health Checks

```bash
# Endpoint de health
curl https://api.justobot.com/health

# Status code 200 = OK
```

## Backup

### Banco de Dados

```bash
# PostgreSQL backup
pg_dump -U justobot -h localhost justobot > backup.sql

# Restore
psql -U justobot -h localhost justobot < backup.sql
```

### Automatizar com cron

```bash
# Crontab
0 2 * * * pg_dump -U justobot justobot > /backups/justobot_$(date +\%Y\%m\%d).sql
```

## Scaling

### Horizontal (Múltiplas Instâncias)

```bash
# Docker Compose
docker-compose up -d --scale api=3

# Kubernetes
kubectl scale deployment justobot --replicas=3
```

### Vertical (Mais Recursos)

Aumentar recursos da instância/container:
- CPU
- Memória
- Conexões do banco

## SSL/HTTPS

### Let's Encrypt

```bash
# Certbot
sudo certbot --nginx -d api.justobot.com
```

### CloudFlare

Usar proxy do CloudFlare com SSL automático.

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Deploy script
```

## Troubleshooting

### Verificar logs

```bash
docker-compose logs api --tail=100
```

### Reiniciar serviço

```bash
docker-compose restart api
```

### Verificar conectividade

```bash
# Banco de dados
docker-compose exec db psql -U justobot

# Redis
docker-compose exec redis redis-cli ping
```
