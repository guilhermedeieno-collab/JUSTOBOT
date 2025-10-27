#!/bin/bash

# Script de setup rápido do JUSTOBOT

set -e

echo "======================================"
echo "JUSTOBOT - Setup"
echo "======================================"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION encontrado"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo ""
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    echo "✓ Ambiente virtual criado"
else
    echo "✓ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo ""
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo ""
echo "Atualizando pip..."
pip install --upgrade pip -q

# Instalar dependências
echo ""
echo "Instalando dependências..."
pip install -r requirements.txt -q
echo "✓ Dependências instaladas"

# Criar .env se não existir
if [ ! -f ".env" ]; then
    echo ""
    echo "Criando arquivo .env..."
    cp .env.example .env
    echo "✓ Arquivo .env criado"
    echo "⚠️  Edite o arquivo .env com suas configurações"
else
    echo "✓ Arquivo .env já existe"
fi

# Criar diretórios necessários
echo ""
echo "Criando diretórios..."
mkdir -p logs uploads temp
echo "✓ Diretórios criados"

echo ""
echo "======================================"
echo -e "${GREEN}Setup concluído com sucesso!${NC}"
echo "======================================"
echo ""
echo "Próximos passos:"
echo ""
echo "1. Ative o ambiente virtual:"
echo "   source venv/bin/activate"
echo ""
echo "2. (Opcional) Inicie os serviços com Docker:"
echo "   docker-compose up -d"
echo ""
echo "3. Ou inicie apenas a aplicação:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "4. Acesse a documentação:"
echo "   http://localhost:8000/docs"
echo ""
echo "5. Execute os exemplos:"
echo "   python examples/example_usage.py"
echo ""
