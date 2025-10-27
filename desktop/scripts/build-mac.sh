#!/bin/bash

# Script de build para macOS

set -e

echo "======================================"
echo "JustoBot - Build macOS"
echo "======================================"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado!"
    exit 1
fi

echo "✓ Node.js $(node --version) encontrado"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    exit 1
fi

echo "✓ Python $(python3 --version | cut -d' ' -f2) encontrado"

# Instalar dependências Node
echo ""
echo "Instalando dependências Node.js..."
cd desktop
npm install

# Build React
echo ""
echo "Building aplicação React..."
npm run build

# Build Electron para macOS
echo ""
echo "Building aplicação Electron para macOS..."
npm run build:mac

echo ""
echo "======================================"
echo -e "${GREEN}Build concluído com sucesso!${NC}"
echo "======================================"
echo ""
echo "Arquivos gerados em:"
echo "  desktop/release/"
echo ""
echo "Para instalar via Homebrew:"
echo "  1. Faça upload do .zip para GitHub Releases"
echo "  2. brew install --cask justobot"
echo ""
