# JustoBot v1.0.0 - Release Notes

## 🎉 Primeira Release Oficial!

Estamos orgulhosos em apresentar a primeira versão do **JustoBot** - Sistema de Consulta de Processos Judiciais!

## ✨ Novidades

### 🖥️ Aplicação Desktop para macOS

Uma aplicação nativa completa com interface moderna e intuitiva:

- **Interface Moderna**: Design Galileo Glass UI com efeitos glassmorphism
- **Dashboard Interativo**: Visão geral com estatísticas e métricas em tempo real
- **Consultas Individuais**: Busque processos por CPF, Nome ou Número do Processo
- **Processamento em Lote**: Upload de planilhas Excel/CSV com drag & drop
- **Sistema de Credenciais**: Gerenciamento seguro de API keys
- **Backend Integrado**: FastAPI roda automaticamente ao abrir o app

### 🌐 API REST Completa

- **FastAPI**: Documentação automática em `/docs`
- **Endpoints Completos**: Consultas, Bulk, Status, Download
- **Processamento Assíncrono**: Alta performance com asyncio
- **Rate Limiting**: Proteção contra sobrecarga
- **Docker Ready**: docker-compose.yml incluído

### 🏛️ Tribunais Suportados

- **TJSP**: Tribunal de Justiça de São Paulo ✅
- Mais tribunais em breve (TJRJ, STJ, STF)

## 📦 Como Instalar

### macOS (Aplicação Desktop)

**Via Homebrew (Recomendado):**

```bash
brew tap guilhermedeieno-collab/justobot
brew install --cask justobot
```

**Download Direto:**

Baixe um dos arquivos abaixo:
- `JustoBot-1.0.0-mac-universal.dmg` - Para Intel e Apple Silicon
- `JustoBot-1.0.0-mac-universal.zip` - Versão compactada

### API REST

```bash
# Clone o repositório
git clone https://github.com/guilhermedeieno-collab/JUSTOBOT.git
cd JUSTOBOT

# Setup rápido
./scripts/setup.sh

# Ou com Docker
docker-compose up -d
```

## 🎯 Funcionalidades

### Dashboard
- 📊 Estatísticas de consultas
- 📈 Taxa de sucesso
- 🏛️ Tribunais disponíveis
- 📝 Jobs recentes

### Consultas
- 🔍 Busca por CPF
- 👤 Busca por Nome
- 📄 Busca por Número de Processo
- 📋 Visualização detalhada de partes e movimentações

### Processamento em Lote
- 📤 Upload de planilhas (Excel/CSV)
- ⏱️ Acompanhamento em tempo real
- 📊 Barra de progresso
- 📥 Download de resultados
- 📜 Histórico completo

### Configurações
- 🔐 Gerenciamento de credenciais
- 👁️ Mostrar/ocultar senhas
- 🖥️ Status do servidor
- ℹ️ Informações do sistema

## 🛠️ Stack Tecnológica

### Desktop
- Electron 28.0
- React 18.2
- Vite 5.0
- Tailwind CSS 3.4
- Framer Motion 11.0
- Zustand 4.5

### Backend
- Python 3.11+
- FastAPI 0.109.0
- SQLAlchemy 2.0
- Pandas 2.1
- httpx 0.26

## 📚 Documentação

- [README Principal](https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/README.md)
- [Guia de Instalação Desktop](https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/docs/DESKTOP_INSTALL.md)
- [Arquitetura](https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/docs/ARCHITECTURE.md)
- [Guia da API](https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/docs/API_GUIDE.md)
- [Deploy](https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/docs/DEPLOYMENT.md)

## 🐛 Problemas Conhecidos

Nenhum problema conhecido nesta versão inicial.

## 🔮 Próximas Versões

### v1.1.0 (Planejado)
- [ ] Suporte a TJRJ
- [ ] Modo escuro/claro
- [ ] Notificações de conclusão de jobs
- [ ] Exportação em PDF

### v1.2.0 (Planejado)
- [ ] Suporte a Windows
- [ ] Suporte a Linux
- [ ] Dashboard analytics avançado
- [ ] Integração com calendário

### v2.0.0 (Futuro)
- [ ] Suporte a STJ e STF
- [ ] API GraphQL
- [ ] Sincronização em nuvem
- [ ] Mobile app (iOS/Android)

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Veja [CONTRIBUTING.md](https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/CONTRIBUTING.md)

## 📄 Licença

MIT License - Veja [LICENSE](https://github.com/guilhermedeieno-collab/JUSTOBOT/blob/main/LICENSE)

## 👥 Autores

- JustoBot Team
- Desenvolvido com Claude Code

## 🙏 Agradecimentos

- FastAPI pela excelente framework
- Electron pela plataforma desktop
- Comunidade open source

---

**Download:** [GitHub Releases](https://github.com/guilhermedeieno-collab/JUSTOBOT/releases/tag/v1.0.0)

**Instalação via Homebrew:**
```bash
brew tap guilhermedeieno-collab/justobot
brew install --cask justobot
```

**Suporte:** [GitHub Issues](https://github.com/guilhermedeieno-collab/JUSTOBOT/issues)

---

🎊 **Obrigado por usar o JustoBot!**
