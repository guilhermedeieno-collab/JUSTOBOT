#!/bin/bash

# Setup do ambiente Python dentro da aplicação

APP_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
VENV_PATH="$APP_PATH/Resources/venv"

echo "Setting up Python virtual environment..."

# Cria venv se não existir
if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
fi

# Ativa venv
source "$VENV_PATH/bin/activate"

# Instala dependências
pip install -q --upgrade pip
pip install -q -r "$APP_PATH/Resources/requirements.txt"

echo "✓ Python environment ready"
