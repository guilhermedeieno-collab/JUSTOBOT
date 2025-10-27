# Guia para Criar Release no GitHub

## Passo a Passo para Release v1.0.0

### 1. Criar a Tag Localmente

```bash
# Na sua máquina local
git checkout claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC
git pull origin claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC

# Criar tag
git tag -a v1.0.0 -m "JustoBot v1.0.0 - Primeira Release Oficial"

# Push da tag
git push origin v1.0.0
```

### 2. Criar Release no GitHub

1. Vá para: https://github.com/guilhermedeieno-collab/JUSTOBOT/releases/new

2. Preencha os campos:
   - **Tag**: `v1.0.0` (selecione a tag criada ou crie uma nova)
   - **Target**: `claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC`
   - **Release title**: `JustoBot v1.0.0 - Primeira Release Oficial`

3. Copie e cole o conteúdo de `RELEASE_NOTES.md` na descrição

### 3. Adicionar Arquivos (Opcional)

**Nota**: Como esta é uma aplicação Electron que precisa ser buildada, você pode:

**Opção A: Fazer Build e Anexar**

```bash
cd desktop
npm install
npm run build:mac

# Anexar os arquivos gerados:
# - release/JustoBot-1.0.0-mac-universal.dmg
# - release/JustoBot-1.0.0-mac-universal.zip
```

**Opção B: Release Somente do Código**

Marque como "Pre-release" e adicione uma nota:
```
⚠️ Esta versão contém o código-fonte completo.
Para instruções de build, veja desktop/BUILD_INSTRUCTIONS.md

Ou aguarde pela próxima release com binários pre-compilados.
```

### 4. Publicar

- Marque "Set as the latest release" se for a versão principal
- Clique em "Publish release"

## Template Completo para Descrição do Release

```markdown
# JustoBot v1.0.0 🎉

Primeira versão oficial do JustoBot - Sistema de Consulta de Processos Judiciais!

## ✨ Destaques

### 🖥️ Aplicação Desktop para macOS
- Interface moderna com Galileo Glass UI
- Dashboard interativo com estatísticas
- Consultas individuais e processamento em lote
- Sistema de credenciais integrado
- Backend FastAPI automático

### 🌐 API REST Completa
- FastAPI com documentação automática
- Processamento assíncrono de alta performance
- Docker ready
- Rate limiting e retry automático

### 🏛️ Tribunais Suportados
- ✅ TJSP - Tribunal de Justiça de São Paulo

## 📦 Instalação

### macOS (Aplicação Desktop)

**Via Homebrew:**
\`\`\`bash
brew tap guilhermedeieno-collab/justobot
brew install --cask justobot
\`\`\`

**Build do Código:**
\`\`\`bash
git clone https://github.com/guilhermedeieno-collab/JUSTOBOT.git
cd JUSTOBOT/desktop
npm install
npm run build:mac
\`\`\`

### API REST

**Docker:**
\`\`\`bash
git clone https://github.com/guilhermedeieno-collab/JUSTOBOT.git
cd JUSTOBOT
docker-compose up -d
\`\`\`

**Manual:**
\`\`\`bash
./scripts/setup.sh
uvicorn app.main:app --reload
\`\`\`

## 📚 Documentação

- [README Principal](README.md)
- [Instalação Desktop](docs/DESKTOP_INSTALL.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Guia da API](docs/API_GUIDE.md)
- [Instruções de Build](desktop/BUILD_INSTRUCTIONS.md)

## 🎯 Funcionalidades Principais

### Dashboard
- 📊 Estatísticas em tempo real
- 🏛️ Tribunais disponíveis
- 📝 Histórico de jobs

### Consultas
- 🔍 Busca por CPF
- 👤 Busca por Nome
- 📄 Busca por Número de Processo

### Processamento em Lote
- 📤 Upload de planilhas (Excel/CSV)
- ⏱️ Acompanhamento em tempo real
- 📥 Download de resultados

### Configurações
- 🔐 Gerenciamento de credenciais de API
- 👁️ Visualização segura de senhas
- 🖥️ Status do servidor

## 🛠️ Stack Tecnológica

**Desktop:**
- Electron 28.0
- React 18.2
- Vite 5.0
- Tailwind CSS 3.4
- Framer Motion 11.0

**Backend:**
- Python 3.11+
- FastAPI 0.109.0
- SQLAlchemy 2.0
- Pandas 2.1

## 🔮 Roadmap

### v1.1.0
- Suporte a TJRJ
- Modo escuro/claro
- Notificações de jobs

### v1.2.0
- Windows e Linux support
- Dashboard analytics
- Exportação PDF

## 🐛 Problemas Conhecidos

Nenhum problema conhecido nesta versão.

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE)

---

**Desenvolvido com ❤️ usando Electron + React + FastAPI**

🎊 Obrigado por usar o JustoBot!
```

## Checklist de Release

- [ ] Tag v1.0.0 criada e pushed
- [ ] Release criada no GitHub
- [ ] Release notes copiadas
- [ ] Arquivos anexados (se aplicável)
- [ ] Release publicada
- [ ] Homebrew formula atualizada (se builds anexados)
- [ ] Documentação verificada
- [ ] Links testados

## Comandos Úteis

### Ver releases existentes
```bash
gh release list
```

### Criar release via CLI
```bash
gh release create v1.0.0 \
  --title "JustoBot v1.0.0 - Primeira Release Oficial" \
  --notes-file RELEASE_NOTES.md \
  --target claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC
```

### Adicionar arquivo à release
```bash
gh release upload v1.0.0 desktop/release/*.dmg desktop/release/*.zip
```

## Após Publicar

1. ✅ Verificar que a release aparece em /releases
2. ✅ Testar links de download
3. ✅ Verificar Homebrew formula (se aplicável)
4. ✅ Anunciar no README principal
5. ✅ Compartilhar nas redes sociais/comunidades

## Troubleshooting

### Erro ao push da tag
```bash
# Deletar tag local
git tag -d v1.0.0

# Criar novamente
git tag -a v1.0.0 -m "Release message"

# Force push
git push origin v1.0.0 --force
```

### Release não aparece
- Verifique se a tag foi criada corretamente
- Certifique-se que o branch target existe
- Aguarde alguns segundos para sincronização

---

Para mais informações sobre releases no GitHub:
https://docs.github.com/en/repositories/releasing-projects-on-github
