#!/bin/bash

# Script para executar testes

set -e

echo "======================================"
echo "JUSTOBOT - Executando Testes"
echo "======================================"
echo ""

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Limpar cache
echo "Limpando cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
rm -rf htmlcov/ .coverage 2>/dev/null || true
echo "✓ Cache limpo"
echo ""

# Executar testes
echo "Executando testes..."
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

echo ""
echo "======================================"
echo "Testes concluídos!"
echo "======================================"
echo ""
echo "Relatório de cobertura HTML gerado em: htmlcov/index.html"
echo ""
