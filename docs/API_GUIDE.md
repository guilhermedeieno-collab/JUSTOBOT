# Guia da API JUSTOBOT

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticação

Atualmente a API é aberta. Para produção, implemente autenticação via:
- API Keys (header `X-API-Key`)
- JWT tokens
- OAuth2

## Endpoints

### 1. Health Check

```http
GET /health
```

**Resposta:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Listar Tribunais

```http
GET /api/v1/cases/tribunals
```

**Resposta:**
```json
{
  "tribunals": [
    {
      "code": "TJSP",
      "name": "Tribunal de Justiça de São Paulo",
      "available": true
    }
  ]
}
```

### 3. Buscar Processos

```http
POST /api/v1/cases/search
Content-Type: application/json

{
  "tribunal": "TJSP",
  "search_type": "cpf",
  "query": "12345678900"
}
```

**Parâmetros:**
- `tribunal`: Código do tribunal (TJSP, TJRJ, etc)
- `search_type`: Tipo de busca
  - `cpf`: Busca por CPF
  - `name`: Busca por nome
  - `case_number`: Busca por número do processo
- `query`: Termo de busca

**Resposta:**
```json
{
  "query": "12345678900",
  "search_type": "cpf",
  "tribunal": "TJSP",
  "total_found": 2,
  "search_date": "2024-01-15T10:30:00",
  "cases": [
    {
      "case_number": "1000001-01.2024.8.26.0100",
      "tribunal": "TJSP",
      "court": "1ª Vara Cível",
      "status": "ativo",
      "subject": "Ação de Cobrança",
      "start_date": "2024-01-15T00:00:00",
      "parties": [
        {
          "name": "João da Silva",
          "role": "autor",
          "cpf_cnpj": "12345678900"
        }
      ],
      "movements": []
    }
  ]
}
```

### 4. Detalhes de Processo

```http
POST /api/v1/cases/details
Content-Type: application/json

{
  "tribunal": "TJSP",
  "case_number": "1000001-01.2024.8.26.0100"
}
```

**Resposta:**
```json
{
  "case_number": "1000001-01.2024.8.26.0100",
  "tribunal": "TJSP",
  "court": "1ª Vara Cível",
  "status": "ativo",
  "subject": "Ação de Cobrança",
  "start_date": "2024-01-15T00:00:00",
  "parties": [...],
  "movements": [
    {
      "date": "2024-01-15T00:00:00",
      "description": "Distribuído",
      "details": null
    }
  ]
}
```

### 5. Upload de Planilha (Bulk)

```http
POST /api/v1/bulk/upload
Content-Type: multipart/form-data

file: arquivo.xlsx
tribunal: TJSP
search_type: cpf
```

**Resposta:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Job criado com sucesso. 100 itens serão processados.",
  "status_url": "/api/v1/bulk/status/550e8400-e29b-41d4-a716-446655440000"
}
```

### 6. Status do Job

```http
GET /api/v1/bulk/status/{job_id}
```

**Resposta:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "tribunal": "TJSP",
  "status": "processing",
  "total_items": 100,
  "processed_items": 45,
  "successful_items": 43,
  "failed_items": 2,
  "progress_percentage": 45.0,
  "created_at": "2024-01-15T10:00:00",
  "started_at": "2024-01-15T10:00:05",
  "completed_at": null
}
```

**Status possíveis:**
- `pending`: Aguardando processamento
- `processing`: Em processamento
- `completed`: Concluído com sucesso
- `partial`: Concluído com erros
- `failed`: Falhou completamente

### 7. Download de Resultados

```http
GET /api/v1/bulk/download/{job_id}
```

Retorna arquivo Excel com:
- Aba "Resultados": Processos encontrados
- Aba "Erros": Consultas que falharam

### 8. Listar Jobs

```http
GET /api/v1/bulk/jobs
```

**Resposta:**
```json
{
  "jobs": [...],
  "total": 5
}
```

## Códigos de Status HTTP

- `200 OK`: Sucesso
- `201 Created`: Recurso criado
- `400 Bad Request`: Erro de validação
- `404 Not Found`: Recurso não encontrado
- `422 Unprocessable Entity`: Erro de validação de dados
- `500 Internal Server Error`: Erro interno

## Rate Limiting

Para evitar sobrecarga dos tribunais:
- Limite padrão: 10 requisições/segundo por tribunal
- Retry automático em caso de throttling
- Exponential backoff

## Exemplo de Uso (Python)

```python
import requests

# Buscar por CPF
response = requests.post(
    "http://localhost:8000/api/v1/cases/search",
    json={
        "tribunal": "TJSP",
        "search_type": "cpf",
        "query": "12345678900"
    }
)

result = response.json()
print(f"Encontrados {result['total_found']} processos")

# Upload de planilha
with open("processos.xlsx", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/bulk/upload",
        files={"file": f},
        data={
            "tribunal": "TJSP",
            "search_type": "cpf"
        }
    )

job = response.json()
print(f"Job ID: {job['job_id']}")

# Verificar status
response = requests.get(
    f"http://localhost:8000/api/v1/bulk/status/{job['job_id']}"
)
status = response.json()
print(f"Progresso: {status['progress_percentage']}%")
```

## Exemplo de Planilha

Para processamento em lote, a planilha deve ter formato:

**Excel (.xlsx) ou CSV:**

| CPF         |
|-------------|
| 12345678900 |
| 98765432100 |
| 11122233344 |

Ou com nome:

| nome          |
|---------------|
| João da Silva |
| Maria Santos  |

O sistema identifica automaticamente a coluna baseada no tipo de busca.

## Documentação Interativa

Acesse a documentação Swagger em:
```
http://localhost:8000/docs
```

Ou ReDoc em:
```
http://localhost:8000/redoc
```
