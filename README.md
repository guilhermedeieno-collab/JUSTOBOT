# JUSTOBOT - Sistema de Consulta de Processos Judiciais

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Sobre

JUSTOBOT é uma plataforma extensível e robusta para consulta automatizada de processos judiciais através das APIs de diversos tribunais brasileiros. O sistema suporta consultas individuais e processamento em lote via planilhas Excel/CSV.

### Destaques

- **Arquitetura Modular**: Baseada em Design Patterns (Strategy, Registry, Factory)
- **Alta Performance**: Processamento assíncrono com controle de concorrência
- **Extensível**: Framework completo para adicionar novos tribunais
- **Produção-Ready**: Docker, health checks, logging estruturado
- **API RESTful**: Documentação interativa com Swagger/OpenAPI

## Funcionalidades

- Consulta de processos por CPF, nome ou número do processo
- Processamento em lote via upload de planilhas (Excel/CSV)
- Sistema de jobs com acompanhamento de progresso
- Rate limiting e retry automático
- Cache de consultas (Redis)
- Exportação de resultados em Excel
- Validação robusta de dados (CPF, CNPJ, números de processo)

## Tribunais Suportados

- [x] **TJSP** - Tribunal de Justiça de São Paulo
- [ ] **TJRJ** - Tribunal de Justiça do Rio de Janeiro (planejado)
- [ ] **STJ** - Superior Tribunal de Justiça (planejado)
- [ ] **STF** - Supremo Tribunal Federal (planejado)

> Adicionar novos tribunais é simples! Veja [CONTRIBUTING.md](CONTRIBUTING.md)

## Arquitetura

O sistema utiliza o **Strategy Pattern** para implementar diferentes tribunais de forma modular:

```
app/
├── tribunals/
│   ├── base.py          # Interface abstrata
│   ├── tjsp/            # Implementação TJSP
│   └── registry.py      # Registro de tribunais
```

Cada tribunal implementa a interface `BaseTribunal` com métodos padronizados:
- `search_by_cpf()`
- `search_by_name()`
- `search_by_case_number()`
- `get_case_details()`

## Instalação

### Requisitos
- Python 3.11+
- PostgreSQL 14+
- Redis (opcional, para cache)

### Setup Rápido

**Opção 1: Script Automático**

```bash
# Clone o repositório
git clone <repo-url>
cd JUSTOBOT

# Execute o script de setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Inicie o servidor
source venv/bin/activate
uvicorn app.main:app --reload
```

**Opção 2: Manual**

```bash
# Clone o repositório
git clone <repo-url>
cd JUSTOBOT

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Inicie o servidor
uvicorn app.main:app --reload
```

**Opção 3: Docker (Recomendado para produção)**

```bash
# Inicie todos os serviços (API + PostgreSQL + Redis)
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Parar serviços
docker-compose down
```

Acesse: http://localhost:8000/docs

## Uso da API

### Consulta Individual

```bash
# Por CPF
curl -X POST "http://localhost:8000/api/v1/cases/search" \
  -H "Content-Type: application/json" \
  -d '{
    "tribunal": "tjsp",
    "search_type": "cpf",
    "query": "12345678900"
  }'

# Por nome
curl -X POST "http://localhost:8000/api/v1/cases/search" \
  -H "Content-Type: application/json" \
  -d '{
    "tribunal": "tjsp",
    "search_type": "name",
    "query": "João da Silva"
  }'
```

### Consulta em Lote

```bash
# Upload de planilha
curl -X POST "http://localhost:8000/api/v1/bulk/upload" \
  -F "file=@processos.xlsx" \
  -F "tribunal=tjsp"

# Verificar status
curl "http://localhost:8000/api/v1/bulk/status/{job_id}"

# Download dos resultados
curl "http://localhost:8000/api/v1/bulk/download/{job_id}" -o resultados.xlsx
```

## Documentação da API

Acesse a documentação interativa em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estrutura do Projeto

```
justobot/
├── app/
│   ├── api/              # Endpoints REST
│   ├── core/             # Configurações centrais
│   ├── tribunals/        # Implementações dos tribunais
│   ├── services/         # Lógica de negócio
│   ├── models/           # Modelos do banco de dados
│   └── utils/            # Utilitários
├── tests/                # Testes
├── alembic/              # Migrações de banco
├── docker-compose.yml
└── requirements.txt
```

## Desenvolvimento

### Adicionando um Novo Tribunal

1. Crie um diretório em `app/tribunals/novo_tribunal/`
2. Implemente a interface `BaseTribunal`
3. Registre no `TribunalRegistry`

Exemplo:

```python
from app.tribunals.base import BaseTribunal

class NovoTribunalClient(BaseTribunal):
    async def search_by_cpf(self, cpf: str) -> List[Case]:
        # Implementação específica
        pass
```

### Testes

```bash
# Rodar todos os testes
pytest

# Ou use o script
./scripts/test.sh

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/tribunals/test_tjsp.py -v
```

### Exemplos de Uso

```bash
# Criar planilhas de exemplo
python examples/create_sample_spreadsheet.py

# Executar exemplos de API
python examples/example_usage.py
```

## Documentação Completa

- [Guia de Arquitetura](docs/ARCHITECTURE.md) - Padrões e estrutura do código
- [Guia da API](docs/API_GUIDE.md) - Documentação detalhada dos endpoints
- [Guia de Deploy](docs/DEPLOYMENT.md) - Como colocar em produção
- [Como Contribuir](CONTRIBUTING.md) - Guia para desenvolvedores

## Comandos Úteis (Makefile)

```bash
make install      # Instalar dependências
make dev          # Executar em modo desenvolvimento
make test         # Executar testes
make lint         # Verificar código
make format       # Formatar código
make docker-up    # Subir containers
make docker-down  # Parar containers
```

## Stack Tecnológica

- **Backend**: Python 3.11+ com FastAPI
- **HTTP Client**: httpx (async)
- **Data Processing**: Pandas, openpyxl
- **Database**: PostgreSQL + SQLAlchemy (async)
- **Cache**: Redis
- **Logging**: Loguru
- **Testing**: pytest + pytest-asyncio
- **Deployment**: Docker + docker-compose

## Performance

- Requisições assíncronas (asyncio)
- Processamento concorrente controlado
- Rate limiting por tribunal
- Cache de consultas (Redis)
- Pool de conexões otimizado

## Segurança

- Validação rigorosa de entrada
- Sanitização de dados
- Rate limiting e retry exponencial
- Logs estruturados
- Suporte para autenticação (API Key, JWT)

## Roadmap

- [ ] Adicionar TJRJ
- [ ] Adicionar STJ
- [ ] Sistema de webhooks para notificações
- [ ] Dashboard web para visualização
- [ ] Integração com sistemas de CRM
- [ ] API GraphQL
- [ ] Suporte a mais formatos de arquivo (JSON, XML)

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes

## Contribuindo

Contribuições são muito bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/JUSTOBOT/issues)
- **Documentação**: [/docs](docs/)
- **Exemplos**: [/examples](examples/)

## Autores

Desenvolvido com Python e FastAPI

---

**Aviso Legal**: Esta ferramenta é destinada apenas para consultas em fontes públicas de tribunais. Respeite os termos de uso de cada tribunal e não faça uso abusivo das APIs.
