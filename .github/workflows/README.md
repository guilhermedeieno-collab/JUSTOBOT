# GitHub Actions Workflows

## Workflows Configurados

### 1. Build and Release (`build-release.yml`)

**Quando roda:** Automaticamente quando você cria uma nova tag (ex: `v1.0.1`, `v1.1.0`)

**O que faz:**
1. ✅ Checkout do código
2. ✅ Instala Node.js e Python
3. ✅ Instala todas as dependências
4. ✅ Faz build do React
5. ✅ Faz build do Electron para macOS (Intel + Apple Silicon)
6. ✅ Anexa automaticamente os arquivos `.dmg` e `.zip` à release
7. ✅ Publica a release no GitHub

**Arquivos gerados:**
- `JustoBot-{version}-mac-universal.dmg`
- `JustoBot-{version}-mac-universal.zip`
- `JustoBot-{version}-mac-x64.dmg`
- `JustoBot-{version}-mac-arm64.dmg`

**Como usar:**
```bash
# Criar e push uma nova tag
git tag v1.0.1
git push origin v1.0.1

# Ou via GitHub CLI
gh release create v1.0.1 --generate-notes
```

Aguarde ~10 minutos e os arquivos aparecerão automaticamente na release!

---

### 2. Test Build (`test-build.yml`)

**Quando roda:** Em todo push e pull request

**O que faz:**
1. ✅ Testa se as dependências instalam corretamente
2. ✅ Valida que o código compila
3. ✅ Roda testes (se existirem)

**Não cria builds** - apenas valida o código.

---

## Como Criar uma Nova Release com Build Automático

### Método 1: Via Git (Terminal)

```bash
# Certifique-se que está na branch correta
git checkout main  # ou sua branch principal

# Crie a tag
git tag -a v1.0.1 -m "Release v1.0.1 com builds automáticos"

# Push da tag
git push origin v1.0.1
```

**Resultado:**
- GitHub Actions detecta a tag
- Faz build automaticamente
- Anexa os arquivos à release
- Você recebe notificação quando terminar

### Método 2: Via GitHub CLI

```bash
# Criar release e tag ao mesmo tempo
gh release create v1.0.1 \
  --title "JustoBot v1.0.1" \
  --notes "Build automático via GitHub Actions"
```

### Método 3: Via Interface Web

1. Vá em: https://github.com/seu-usuario/JUSTOBOT/releases/new
2. Preencha:
   - Tag: `v1.0.1`
   - Title: `JustoBot v1.0.1`
   - Description: Suas release notes
3. Clique **"Publish release"**

GitHub Actions vai adicionar os builds automaticamente em alguns minutos!

---

## Monitorar o Build

Enquanto o build está rodando:

1. Vá em: https://github.com/seu-usuario/JUSTOBOT/actions
2. Clique no workflow "Build and Release Desktop App"
3. Veja o progresso em tempo real
4. Quando terminar (✅), os arquivos estarão na release

---

## Troubleshooting

### Build falhou?

Verifique os logs:
1. Actions → Clique no workflow que falhou
2. Veja qual step falhou
3. Leia os logs de erro

**Problemas comuns:**

**1. Permissões:**
- Vá em Settings → Actions → General
- Marque "Read and write permissions"
- Salve

**2. Node/Python não encontrado:**
- Commit e tente novamente (workflows já tem setup correto)

**3. Falta de espaço:**
- Normal no GitHub Actions, ele vai tentar novamente

### Como testar sem criar release?

Push em qualquer branch vai rodar o `test-build.yml` que valida tudo sem criar release.

---

## Estatísticas

- **Tempo médio de build:** 8-12 minutos
- **Runners usados:** macOS-latest (grátis para repos públicos)
- **Artefatos mantidos:** 5 dias (downloads via Actions)
- **Build automático:** ✅ Sim, completamente automático

---

## Próximas Melhorias Possíveis

- [ ] Build para Windows
- [ ] Build para Linux
- [ ] Notarização automática (requer certificado Apple)
- [ ] Upload automático para Homebrew
- [ ] Changelog automático

---

**🎉 Agora você nunca mais precisa fazer build manualmente!**

Apenas crie uma tag e aguarde. GitHub Actions faz o resto.
