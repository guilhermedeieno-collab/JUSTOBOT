# Contribuindo para o JUSTOBOT

Obrigado por considerar contribuir para o JUSTOBOT!

## Como Contribuir

### 1. Fork e Clone

```bash
git clone https://github.com/seu-usuario/JUSTOBOT.git
cd JUSTOBOT
```

### 2. Crie um Branch

```bash
git checkout -b feature/minha-feature
# ou
git checkout -b fix/meu-bug
```

### 3. Configure o Ambiente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Faça suas Alterações

- Escreva código limpo e bem documentado
- Siga as convenções do projeto
- Adicione testes para novas funcionalidades
- Atualize a documentação se necessário

### 5. Execute os Testes

```bash
pytest
```

### 6. Formate o Código

```bash
black app/ tests/
flake8 app/ tests/
```

### 7. Commit

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
```

**Convenção de Commits:**
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes
- `chore:` manutenção

### 8. Push e Pull Request

```bash
git push origin feature/minha-feature
```

Abra um Pull Request no GitHub.

## Adicionando um Novo Tribunal

### 1. Estrutura

Crie diretório:
```
app/tribunals/novo_tribunal/
├── __init__.py
├── client.py
└── parser.py
```

### 2. Implemente o Cliente

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

    async def search_by_name(self, name: str) -> SearchResult:
        # Implementação
        pass

    async def search_by_case_number(self, case_number: str) -> SearchResult:
        # Implementação
        pass

    async def get_case_details(self, case_number: str) -> Optional[Case]:
        # Implementação
        pass
```

### 3. Crie Parser (se necessário)

```python
# app/tribunals/novo_tribunal/parser.py
class NovoTribunalParser:
    async def parse_search_results(self, html: str, tribunal: str):
        # Parse específico
        pass
```

### 4. Adicione Testes

```python
# tests/tribunals/test_novo_tribunal.py
import pytest
from app.tribunals.novo_tribunal.client import NovoTribunalClient

class TestNovoTribunal:
    @pytest.fixture
    def client(self):
        return NovoTribunalClient()

    def test_tribunal_code(self, client):
        assert client._get_tribunal_code() == "NOVO"
```

### 5. Atualize Documentação

- Adicione o tribunal no README.md
- Documente peculiaridades na API
- Adicione exemplos

## Diretrizes de Código

### Python

- Python 3.11+
- Type hints sempre que possível
- Docstrings em formato Google
- Máximo 100 caracteres por linha
- Use async/await para I/O

### Exemplo de Docstring

```python
async def search_by_cpf(self, cpf: str) -> SearchResult:
    """
    Busca processos por CPF

    Args:
        cpf: CPF a ser pesquisado (apenas números)

    Returns:
        SearchResult com processos encontrados

    Raises:
        ValueError: Se CPF inválido
    """
    pass
```

### Testes

- Cobertura mínima: 80%
- Testes unitários para lógica de negócio
- Testes de integração para APIs
- Use fixtures do pytest
- Mocks para chamadas externas

## Estrutura de Pull Request

**Título:** Descrição curta e clara

**Descrição:**
- O que foi mudado
- Por que foi mudado
- Como testar
- Screenshots (se aplicável)

**Checklist:**
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Código formatado (black, flake8)
- [ ] Testes passando
- [ ] Sem conflitos com main

## Code Review

PRs serão revisados por:
- Qualidade do código
- Cobertura de testes
- Documentação
- Performance
- Segurança

## Reportar Bugs

Abra uma issue com:
- Descrição clara
- Passos para reproduzir
- Comportamento esperado vs atual
- Versão do Python
- Logs relevantes

## Sugerir Funcionalidades

Abra uma issue de feature request com:
- Descrição da funcionalidade
- Casos de uso
- Exemplos de como seria usada
- Mockups (se aplicável)

## Código de Conduta

- Seja respeitoso
- Aceite críticas construtivas
- Foque no que é melhor para o projeto
- Seja colaborativo

## Dúvidas?

Abra uma issue ou entre em contato!

Obrigado pela contribuição! 🚀
