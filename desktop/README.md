# JustoBot Desktop

Aplicação desktop para macOS do JustoBot - Sistema de Consulta de Processos Judiciais.

## Características

- 🎨 **Interface Moderna** - Galileo Glass UI com glassmorphism
- ⚡ **Alta Performance** - Electron + React + Vite
- 🔐 **Seguro** - Sistema de credenciais local com electron-store
- 🚀 **Rápido** - Backend Python FastAPI integrado
- 📊 **Completo** - Dashboard, Consultas, Processamento em Lote

## Instalação

### Via Homebrew (Recomendado)

```bash
# Adicionar tap
brew tap guilhermedeieno-collab/justobot

# Instalar
brew install --cask justobot
```

### Manual

1. Baixe o arquivo `.dmg` ou `.zip` das [Releases](https://github.com/guilhermedeieno-collab/JUSTOBOT/releases)
2. Abra o arquivo e arraste JustoBot para Applications
3. Execute JustoBot

## Desenvolvimento

### Requisitos

- Node.js 18+
- Python 3.11+
- macOS 11+ (para build)

### Setup

```bash
cd desktop

# Instalar dependências
npm install

# Desenvolvimento
npm run dev
```

### Build

```bash
# Build para macOS
npm run build:mac

# Ou use o script
chmod +x scripts/build-mac.sh
./scripts/build-mac.sh
```

## Estrutura

```
desktop/
├── electron/          # Código Electron
│   ├── main.js       # Processo principal
│   └── preload.js    # Preload script
├── src/              # Código React
│   ├── pages/        # Páginas da aplicação
│   ├── components/   # Componentes reutilizáveis
│   └── store/        # Estado global (Zustand)
├── assets/           # Assets (logos, ícones)
└── build/            # Configurações de build
```

## Funcionalidades

### 1. Dashboard
- Visão geral das estatísticas
- Tribunais disponíveis
- Jobs recentes

### 2. Consultas
- Busca por CPF
- Busca por Nome
- Busca por Número de Processo
- Resultados detalhados

### 3. Processamento em Lote
- Upload de planilhas (Excel/CSV)
- Acompanhamento em tempo real
- Download de resultados
- Histórico de jobs

### 4. Configurações
- Gerenciamento de credenciais de API
- Configurações do servidor
- Informações do sistema

## Tecnologias

- **Electron** - Framework desktop
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animações
- **Zustand** - State management
- **Axios** - HTTP client
- **FastAPI** - Backend Python

## Segurança

- Credenciais armazenadas localmente com criptografia
- Comunicação segura entre processos
- Servidor backend local (127.0.0.1)
- Sandboxing do Electron

## Troubleshooting

### Servidor Python não inicia

```bash
# Verifique se o Python está instalado
python3 --version

# Verifique o venv
ls -la ../venv

# Reinstale dependências
cd ..
pip install -r requirements.txt
```

### Erros de permissão no macOS

```bash
# Remova da quarentena
xattr -cr /Applications/JustoBot.app
```

## Licença

MIT License - veja [LICENSE](../LICENSE) para detalhes

## Suporte

- Issues: https://github.com/guilhermedeieno-collab/JUSTOBOT/issues
- Documentação: https://github.com/guilhermedeieno-collab/JUSTOBOT/tree/main/docs
