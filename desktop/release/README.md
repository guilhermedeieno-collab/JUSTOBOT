# JustoBot Desktop - Builds

## 📦 Arquivos de Instalação

Para baixar a aplicação JustoBot Desktop para macOS, acesse:

**[GitHub Releases](https://github.com/guilhermedeieno-collab/JUSTOBOT/releases)**

## Arquivos Disponíveis

### macOS

#### Universal (Recomendado)
- **JustoBot-1.0.0-mac-universal.dmg** - Instalador DMG (funciona em Intel e Apple Silicon)
- **JustoBot-1.0.0-mac-universal.zip** - Versão compactada

#### Intel (x64)
- **JustoBot-1.0.0-mac-x64.dmg** - Apenas para Macs Intel

#### Apple Silicon (arm64)
- **JustoBot-1.0.0-mac-arm64.dmg** - Apenas para Macs M1/M2/M3

## Como Instalar

### Opção 1: Via Homebrew (Mais Fácil)

```bash
brew tap guilhermedeieno-collab/justobot
brew install --cask justobot
```

### Opção 2: Download Manual

1. Baixe o arquivo `.dmg` apropriado para seu Mac
2. Abra o arquivo `.dmg`
3. Arraste JustoBot para a pasta Applications
4. Abra o JustoBot:
   - Finder → Applications → JustoBot
   - Clique com botão direito → Abrir (primeira vez)

## Verificação de Integridade

### SHA256 Checksums

```
# Universal
shasum -a 256 JustoBot-1.0.0-mac-universal.dmg

# Intel
shasum -a 256 JustoBot-1.0.0-mac-x64.dmg

# Apple Silicon
shasum -a 256 JustoBot-1.0.0-mac-arm64.dmg
```

## Requisitos do Sistema

- **macOS**: 11.0 (Big Sur) ou superior
- **Memória**: 4 GB RAM mínimo
- **Espaço**: 500 MB livres
- **Processador**: Intel ou Apple Silicon

## Build Local

Se preferir fazer build do código fonte:

```bash
git clone https://github.com/guilhermedeieno-collab/JUSTOBOT.git
cd JUSTOBOT/desktop
npm install
npm run build:mac
```

Veja [BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md) para detalhes.

## Suporte

- **Issues**: https://github.com/guilhermedeieno-collab/JUSTOBOT/issues
- **Documentação**: https://github.com/guilhermedeieno-collab/JUSTOBOT/tree/main/docs
- **Instalação**: https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/docs/DESKTOP_INSTALL.md

## Versões

- **Atual**: v1.0.0
- **Changelog**: [RELEASE_NOTES.md](../../RELEASE_NOTES.md)

---

**Nota**: Os builds são gerados automaticamente via electron-builder.
Para builds locais, siga as instruções em BUILD_INSTRUCTIONS.md
