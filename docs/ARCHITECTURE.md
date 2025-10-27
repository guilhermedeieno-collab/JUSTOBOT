# Arquitetura do JUSTOBOT

## Visão Geral

O JUSTOBOT utiliza uma arquitetura modular e extensível baseada em Design Patterns para permitir a integração fácil de novos tribunais.

## Padrões de Projeto

### 1. Strategy Pattern (Tribunais)

Cada tribunal implementa a interface `BaseTribunal`, permitindo que diferentes implementações sejam intercambiáveis.

```python
from app.tribunals.base import BaseTribunal

class NovoTribunalClient(BaseTribunal):
    async def search_by_cpf(self, cpf: str) -> SearchResult:
        # Implementação específica
        pass
```

### 2. Registry Pattern

O `TribunalRegistry` gerencia todos os tribunais disponíveis usando decorators:

```python
@TribunalRegistry.register("TJSP")
class TJSPClient(BaseTribunal):
    pass
```

### 3. Service Layer

Camada de serviço (`CaseService`, `BulkService`) abstrai a lógica de negócio da API.

## Fluxo de Dados

```
API Request
    ↓
FastAPI Routes (cases.py / bulk.py)
    ↓
Service Layer (case_service.py / bulk_service.py)
    ↓
Tribunal Registry
    ↓
Specific Tribunal Client (tjsp/client.py)
    ↓
HTTP Request to Tribunal
    ↓
Parser (tjsp/parser.py)
    ↓
Response (Case/SearchResult models)
```

## Estrutura de Diretórios

```
app/
├── api/                    # Camada de apresentação
│   ├── routes/            # Endpoints REST
│   └── schemas.py         # Modelos Pydantic
├── core/                  # Configurações centrais
│   ├── config.py
│   └── logging.py
├── tribunals/             # Implementações de tribunais
│   ├── base.py           # Interface abstrata
│   ├── registry.py       # Gerenciador de tribunais
│   └── tjsp/             # Implementação TJSP
│       ├── client.py     # Cliente HTTP
│       └── parser.py     # Parser HTML
├── services/              # Lógica de negócio
│   ├── case_service.py
│   └── bulk_service.py
└── utils/                 # Utilitários
    └── validators.py
```

## Componentes Principais

### BaseTribunal (Interface)

Define o contrato que todos os tribunais devem seguir:

- `search_by_cpf(cpf: str) -> SearchResult`
- `search_by_name(name: str) -> SearchResult`
- `search_by_case_number(number: str) -> SearchResult`
- `get_case_details(number: str) -> Case`

### TribunalRegistry

Gerencia registro e instanciação de tribunais:

- Registro automático via decorator
- Singleton pattern para instâncias
- Factory method para criação

### Services

#### CaseService
- Orquestra consultas individuais
- Valida tribunais
- Abstrai chamadas aos clientes

#### BulkService
- Gerencia jobs de processamento
- Processa planilhas
- Controla concorrência
- Gera relatórios

## Extensibilidade

### Adicionando Novo Tribunal

1. Crie diretório: `app/tribunals/novo_tribunal/`

2. Implemente o cliente:

```python
# app/tribunals/novo_tribunal/client.py
from app.tribunals.base import BaseTribunal
from app.tribunals.registry import TribunalRegistry

@TribunalRegistry.register("NOVO")
class NovoTribunalClient(BaseTribunal):
    def _get_tribunal_code(self) -> str:
        return "NOVO"

    async def search_by_cpf(self, cpf: str) -> SearchResult:
        # Implementação
        pass
```

3. Crie parser se necessário:

```python
# app/tribunals/novo_tribunal/parser.py
class NovoTribunalParser:
    async def parse_search_results(self, data):
        # Parse específico
        pass
```

4. O tribunal estará automaticamente disponível na API!

## Segurança

- Rate limiting por tribunal
- Retry exponencial
- Timeout configurável
- Validação de entrada
- Sanitização de dados

## Performance

- Requisições assíncronas (asyncio)
- Pool de conexões HTTP
- Cache opcional (Redis)
- Processamento em lote concorrente
- Semaphores para controle de concorrência

## Monitoramento

- Logging estruturado (Loguru)
- Health checks
- Métricas de requisições
- Rastreamento de jobs

## Escalabilidade

A arquitetura permite:
- Deploy em múltiplas instâncias
- Cache distribuído (Redis)
- Filas de processamento
- Load balancing
