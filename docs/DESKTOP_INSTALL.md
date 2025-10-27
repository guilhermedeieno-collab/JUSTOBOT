# Instalação do JustoBot Desktop para macOS

## Visão Geral

O JustoBot Desktop é uma aplicação nativa para macOS que integra o backend FastAPI com uma interface moderna em Electron + React.

## Métodos de Instalação

### 1. Via Homebrew (Recomendado) 🍺

O método mais fácil para instalar e manter atualizado.

```bash
# Adicionar o repositório (tap)
brew tap guilhermedeieno-collab/justobot

# Instalar JustoBot
brew install --cask justobot
```

### 2. Download Direto

1. Acesse as [Releases](https://github.com/guilhermedeieno-collab/JUSTOBOT/releases)
2. Baixe o arquivo apropriado:
   - **Intel Mac**: `JustoBot-1.0.0-mac-x64.dmg`
   - **Apple Silicon (M1/M2/M3)**: `JustoBot-1.0.0-mac-arm64.dmg`
   - **Universal**: `JustoBot-1.0.0-mac-universal.dmg` (funciona em ambos)

3. Abra o arquivo `.dmg`
4. Arraste o ícone do JustoBot para a pasta Applications
5. Abra o JustoBot pela primeira vez:
   - Abra o Finder
   - Vá para Applications
   - Clique com botão direito em JustoBot
   - Selecione "Abrir"
   - Confirme que deseja abrir (requerido apenas na primeira vez)

### 3. Build do Código Fonte

Para desenvolvedores que desejam construir a partir do código fonte:

```bash
# Clone o repositório
git clone https://github.com/guilhermedeieno-collab/JUSTOBOT.git
cd JUSTOBOT

# Execute o script de build
chmod +x desktop/scripts/build-mac.sh
./desktop/scripts/build-mac.sh
```

O arquivo `.dmg` será criado em `desktop/release/`.

## Requisitos do Sistema

- **macOS**: 11.0 (Big Sur) ou superior
- **Memória**: 4 GB RAM mínimo, 8 GB recomendado
- **Espaço em Disco**: 500 MB livres
- **Arquitetura**: Intel (x64) ou Apple Silicon (arm64)

## Primeira Execução

### 1. Inicialização Automática

Quando você abre o JustoBot pela primeira vez:

1. ✅ O servidor backend Python inicia automaticamente
2. ✅ A interface carrega em alguns segundos
3. ✅ Os tribunais disponíveis são carregados

### 2. Configurar Credenciais (Opcional)

Se você possui credenciais de API dos tribunais:

1. Clique em **Configurações** na barra lateral
2. Vá para a seção **Credenciais de API**
3. Clique em **Adicionar Nova Credencial**
4. Preencha:
   - **Tribunal**: Ex: TJSP, TJRJ
   - **API Key**: Sua chave de API
   - **API Secret** (opcional): Segredo da API
   - **Notas** (opcional): Descrição
5. Clique em **Adicionar Credencial**

### 3. Realizar Primeira Consulta

1. Clique em **Consultas** na barra lateral
2. Selecione o tipo de busca (CPF, Nome, ou Nº Processo)
3. Digite os dados
4. Clique em **Buscar Processos**

## Recursos da Aplicação

### Dashboard
- Visão geral das estatísticas
- Lista de tribunais disponíveis
- Histórico de jobs recentes

### Consultas Individuais
- ✅ Busca por CPF
- ✅ Busca por Nome
- ✅ Busca por Número de Processo
- ✅ Visualização detalhada dos resultados
- ✅ Informações de partes e movimentações

### Processamento em Lote
- ✅ Upload de planilhas Excel (.xlsx, .xls)
- ✅ Upload de arquivos CSV
- ✅ Acompanhamento em tempo real
- ✅ Barra de progresso
- ✅ Estatísticas de sucesso/falha
- ✅ Download dos resultados em Excel
- ✅ Histórico de jobs

### Configurações
- ✅ Gerenciamento de credenciais
- ✅ Visualização segura (mostrar/ocultar)
- ✅ Status do servidor
- ✅ Informações do sistema

## Formato das Planilhas

Para processamento em lote, suas planilhas devem ter:

### Para busca por CPF:
```
| cpf         |
|-------------|
| 12345678900 |
| 98765432100 |
```

### Para busca por Nome:
```
| nome          |
|---------------|
| João da Silva |
| Maria Santos  |
```

### Para busca por Processo:
```
| processo                      |
|-------------------------------|
| 1000001-01.2024.8.26.0100    |
| 1000002-02.2024.8.26.0200    |
```

## Arquitetura

```
JustoBot Desktop
│
├── Electron (Frontend)
│   ├── React UI (Galileo Glass)
│   ├── Zustand (Estado)
│   └── Axios (HTTP Client)
│
└── FastAPI (Backend)
    ├── Python 3.11+
    ├── Uvicorn Server
    └── APIs dos Tribunais
```

## Segurança

### Credenciais
- Armazenadas localmente com `electron-store`
- Criptografadas no disco
- Nunca enviadas para servidores externos
- Protegidas por permissões do macOS

### Servidor
- Roda apenas localmente (127.0.0.1)
- Não aceita conexões externas
- Isolado do sistema

### Dados
- Processamento local
- Sem telemetria
- Resultados salvos localmente

## Troubleshooting

### Problema: "JustoBot não pode ser aberto porque o desenvolvedor não pode ser verificado"

**Solução**:
```bash
# Remover da quarentena
xattr -cr /Applications/JustoBot.app

# Ou abra com botão direito + "Abrir"
```

### Problema: Servidor Python não inicia

**Solução 1 - Verificar Python**:
```bash
python3 --version  # Deve ser 3.11+
```

**Solução 2 - Reinstalar dependências**:
```bash
cd /Applications/JustoBot.app/Contents/Resources
./scripts/setup_venv.sh
```

### Problema: Erro ao fazer upload de planilha

**Verificar**:
- ✅ Arquivo é .xlsx, .xls ou .csv
- ✅ Tem a coluna correta (cpf, nome, ou processo)
- ✅ Arquivo não está corrompido
- ✅ Tamanho menor que 10 MB

### Problema: Credenciais não salvam

**Solução**:
```bash
# Verificar permissões
ls -la ~/Library/Application\ Support/JustoBot

# Se não existir, criar
mkdir -p ~/Library/Application\ Support/JustoBot
```

## Atualização

### Via Homebrew:
```bash
brew upgrade --cask justobot
```

### Manual:
1. Baixe a nova versão
2. Substitua a aplicação antiga em Applications
3. Suas configurações e credenciais serão mantidas

## Desinstalação

### Via Homebrew:
```bash
# Desinstalar aplicação
brew uninstall --cask justobot

# Remover dados (opcional)
brew uninstall --zap justobot
```

### Manual:
```bash
# Remover aplicação
rm -rf /Applications/JustoBot.app

# Remover dados (opcional)
rm -rf ~/Library/Application\ Support/JustoBot
rm -rf ~/Library/Preferences/com.justobot.app.plist
rm -rf ~/Library/Logs/JustoBot
```

## Suporte

- **Issues**: [GitHub Issues](https://github.com/guilhermedeieno-collab/JUSTOBOT/issues)
- **Discussões**: [GitHub Discussions](https://github.com/guilhermedeieno-collab/JUSTOBOT/discussions)
- **Documentação**: [/docs](https://github.com/guilhermedeieno-collab/JUSTOBOT/tree/main/docs)

## Roadmap

- [ ] Windows Support
- [ ] Linux Support
- [ ] Modo escuro/claro
- [ ] Notificações de jobs
- [ ] Exportação em PDF
- [ ] Integração com calendário
- [ ] Sincronização em nuvem (opcional)

---

**Desenvolvido com ❤️ usando Electron + React + FastAPI**
