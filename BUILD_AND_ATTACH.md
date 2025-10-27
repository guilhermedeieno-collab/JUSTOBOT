# 🔨 Como Fazer Build e Anexar à Release

## Por Que Não Tem o App?

A release atual só tem o código-fonte (source code). Para ter a aplicação `.dmg` instalável, precisamos fazer o **build** da aplicação Electron.

## Opção 1: Build Local (Se Você Tem um Mac)

### Passo 1: Preparar o Ambiente

```bash
# Clone o repositório (se ainda não tiver)
git clone https://github.com/guilhermedeieno-collab/JUSTOBOT.git
cd JUSTOBOT

# Ou atualize se já tem
git pull origin claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC
```

### Passo 2: Instalar Dependências

```bash
# Backend Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend Desktop
cd desktop
npm install
```

### Passo 3: Fazer o Build

```bash
# Ainda no diretório desktop/
npm run build:mac
```

Isso vai gerar (leva 5-10 minutos):
```
desktop/release/
├── JustoBot-1.0.0-mac-universal.dmg   ← Para Intel e M1/M2/M3
├── JustoBot-1.0.0-mac-universal.zip
├── JustoBot-1.0.0-mac-x64.dmg         ← Só Intel
└── JustoBot-1.0.0-mac-arm64.dmg       ← Só Apple Silicon
```

### Passo 4: Anexar à Release no GitHub

**Via Interface Web:**

1. Vá em: https://github.com/guilhermedeieno-collab/JUSTOBOT/releases/tag/v1.0.0
2. Clique em **"Edit release"** (ícone de lápis)
3. Arraste os arquivos `.dmg` e `.zip` para a área de anexos
4. Clique em **"Update release"**

**Via GitHub CLI:**

```bash
gh release upload v1.0.0 \
  desktop/release/JustoBot-1.0.0-mac-universal.dmg \
  desktop/release/JustoBot-1.0.0-mac-universal.zip \
  desktop/release/JustoBot-1.0.0-mac-x64.dmg \
  desktop/release/JustoBot-1.0.0-mac-arm64.dmg
```

---

## Opção 2: Publicar Só o Código (Mais Rápido)

Se não puder fazer build agora, você pode:

### 1. Editar a Release

Adicione este aviso no topo da descrição da release:

```markdown
## 📦 Download

⚠️ **Nota**: Esta release contém o código-fonte completo.

Para usar o JustoBot:

**Opção A: Rodar Localmente (Recomendado)**
\`\`\`bash
# Clone e configure
git clone https://github.com/guilhermedeieno-collab/JUSTOBOT.git
cd JUSTOBOT
./scripts/setup.sh

# Para a API
uvicorn app.main:app --reload

# Para a aplicação desktop
cd desktop
npm install
npm run dev
\`\`\`

**Opção B: Docker**
\`\`\`bash
docker-compose up -d
\`\`\`

**Opção C: Build Você Mesmo**
Veja [BUILD_INSTRUCTIONS.md](desktop/BUILD_INSTRUCTIONS.md)

---
```

### 2. Marcar como Pre-release

Na edição da release:
- ✅ Marque **"This is a pre-release"**
- Adicione a nota acima
- Faça build e publique uma v1.0.1 com os binários depois

---

## Opção 3: GitHub Actions (Automático - Avançado)

Crie `.github/workflows/build.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: macos-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: |
          cd desktop
          npm install

      - name: Build
        run: |
          cd desktop
          npm run build:mac

      - name: Upload to Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            desktop/release/*.dmg
            desktop/release/*.zip
```

Então:
```bash
git add .github/workflows/build.yml
git commit -m "ci: adiciona build automático"
git push
git tag v1.0.1
git push origin v1.0.1
```

---

## 🎯 Recomendação

**Para agora:**
1. Edite a release atual
2. Adicione o aviso sobre código-fonte
3. Marque como "pre-release"

**Depois:**
1. Faça build localmente (ou configure GitHub Actions)
2. Crie uma nova tag v1.0.1 com os binários
3. Marque como release estável

---

## ✅ Checklist

- [ ] Release v1.0.0 criada com código-fonte
- [ ] Aviso adicionado sobre ausência de binários
- [ ] Marcada como pre-release (opcional)
- [ ] Build local feito (ou planejado)
- [ ] Arquivos .dmg/.zip anexados
- [ ] Homebrew formula atualizada (após anexar)

---

## 🚀 Resultado Final

Quando anexar os builds, os usuários verão:

**Assets**
- Source code (zip)
- Source code (tar.gz)
- JustoBot-1.0.0-mac-universal.dmg ← **Novo!**
- JustoBot-1.0.0-mac-universal.zip ← **Novo!**
- JustoBot-1.0.0-mac-x64.dmg
- JustoBot-1.0.0-mac-arm64.dmg

E poderão instalar via:
```bash
brew tap guilhermedeieno-collab/justobot
brew install --cask justobot
```

---

**Precisa de ajuda com o build? Me avise e te guio!** 🛠️
