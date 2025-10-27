# Instruções de Build - JustoBot Desktop

## Pré-requisitos

- Node.js 18+
- Python 3.11+
- macOS 11+ (para build macOS)
- Xcode Command Line Tools

## Setup do Ambiente

```bash
# Instalar Xcode Command Line Tools
xcode-select --install

# Instalar Node.js (via Homebrew)
brew install node

# Instalar Python 3.11+
brew install python@3.11
```

## Build Passo a Passo

### 1. Preparar Backend Python

```bash
# Na raiz do projeto
cd JUSTOBOT

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Preparar Frontend Desktop

```bash
# Entrar no diretório desktop
cd desktop

# Instalar dependências Node
npm install

# Verificar instalação
npm list
```

### 3. Build da Aplicação

```bash
# Ainda no diretório desktop/

# Build do React
npm run build

# Build do Electron para macOS
npm run build:mac
```

Isto irá gerar:
- `release/JustoBot-1.0.0-mac-universal.dmg`
- `release/JustoBot-1.0.0-mac-universal.zip`
- `release/JustoBot-1.0.0-mac-x64.dmg` (Intel)
- `release/JustoBot-1.0.0-mac-arm64.dmg` (Apple Silicon)

### 4. Testar o Build

```bash
# Abrir o .app gerado
open release/mac/JustoBot.app
```

## Build para Distribuição

### Assinatura de Código (Opcional mas Recomendado)

```bash
# Obter certificado de desenvolvedor Apple
# https://developer.apple.com/account/

# Configurar variáveis de ambiente
export APPLE_ID="seu-email@example.com"
export APPLE_ID_PASSWORD="senha-app-specific"
export CSC_LINK="caminho/para/certificado.p12"
export CSC_KEY_PASSWORD="senha-do-certificado"

# Build com assinatura
npm run build:mac
```

### Notarização (Para distribuição fora da App Store)

```bash
# Notarizar o app
npx electron-notarize --bundle-id com.justobot.app \
  --app-path release/mac/JustoBot.app \
  --apple-id $APPLE_ID \
  --apple-id-password $APPLE_ID_PASSWORD
```

## Estrutura de Arquivos Gerados

```
desktop/release/
├── mac/
│   └── JustoBot.app           # Aplicação
├── JustoBot-1.0.0-mac-universal.dmg
├── JustoBot-1.0.0-mac-universal.zip
├── JustoBot-1.0.0-mac-x64.dmg
└── JustoBot-1.0.0-mac-arm64.dmg
```

## Troubleshooting

### Erro: "electron-builder não encontrado"

```bash
npm install electron-builder --save-dev
```

### Erro: "Python não encontrado"

Certifique-se que o venv está na raiz do projeto:

```bash
cd ..  # Voltar para raiz
python3 -m venv venv
```

### Erro de permissão no macOS

```bash
chmod +x scripts/*.sh
```

### Erro: "Cannot find module"

```bash
rm -rf node_modules package-lock.json
npm install
```

## Build Rápido (Script)

Use o script fornecido:

```bash
cd desktop
chmod +x scripts/build-mac.sh
./scripts/build-mac.sh
```

## Validação do Build

Antes de distribuir, teste:

1. ✅ Aplicação abre sem erros
2. ✅ Servidor Python inicia automaticamente
3. ✅ Interface carrega completamente
4. ✅ Todas as páginas funcionam
5. ✅ Consultas retornam resultados
6. ✅ Upload de planilhas funciona
7. ✅ Credenciais salvam corretamente

## Upload para GitHub Releases

1. Gerar os builds
2. Ir para GitHub → Releases → New Release
3. Tag: `v1.0.0`
4. Title: `JustoBot v1.0.0`
5. Anexar arquivos:
   - `JustoBot-1.0.0-mac-universal.dmg`
   - `JustoBot-1.0.0-mac-universal.zip`
6. Publicar release

## Atualização da Formula Homebrew

Após publicar o release:

1. Calcular SHA256:
```bash
shasum -a 256 JustoBot-1.0.0-mac-universal.zip
```

2. Atualizar `homebrew/justobot.rb` com o SHA256

3. Commit e push da formula

## Recursos

- [Electron Builder Docs](https://www.electron.build/)
- [Code Signing Guide](https://www.electron.build/code-signing)
- [Notarization Guide](https://kilianvalkhof.com/2019/electron/notarizing-your-electron-application/)

---

Para dúvidas, abra uma issue em:
https://github.com/guilhermedeieno-collab/JUSTOBOT/issues
