# 🚀 Como Fazer o Release AGORA

## Opção Mais Rápida (3 minutos)

### 1. Acesse o GitHub

Abra: https://github.com/guilhermedeieno-collab/JUSTOBOT/releases/new

### 2. Preencha o Formulário

```
Tag version:        v1.0.0
Target:            claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC
Release title:     JustoBot v1.0.0 - Primeira Release Oficial
```

### 3. Copie e Cole a Descrição

Abra o arquivo `RELEASE_NOTES.md` e copie TODO o conteúdo na caixa de descrição.

### 4. Publique

Clique em **"Publish release"**

## ✅ PRONTO!

Seu release está publicado em:
```
https://github.com/guilhermedeieno-collab/JUSTOBOT/releases
```

---

## Opção com GitHub CLI (mais rápido ainda)

No seu terminal:

```bash
# 1. Pull do código
git pull origin claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC

# 2. Criar e push tag
git tag v1.0.0
git push origin v1.0.0

# 3. Criar release
gh release create v1.0.0 \
  --title "JustoBot v1.0.0 - Primeira Release Oficial" \
  --notes-file RELEASE_NOTES.md \
  --target claude/legal-case-tracker-app-011CUY6owhHGMm5uV4bCurzC
```

---

## ⚠️ Quer Incluir Builds?

**Pule esta parte por enquanto** e publique apenas o código-fonte.

Para adicionar builds depois:

1. No seu Mac, rode:
```bash
cd desktop
npm install
npm run build:mac
```

2. Anexe os arquivos na release:
```bash
gh release upload v1.0.0 release/*.dmg release/*.zip
```

---

## 📱 Após Publicar

✅ Compartilhe o link: https://github.com/guilhermedeieno-collab/JUSTOBOT/releases/tag/v1.0.0

✅ Atualize o README se necessário

✅ Tweet/post sobre o lançamento!

---

**É isso! Simples assim.** 🎉
