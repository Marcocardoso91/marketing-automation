# MCP Orchestrator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Servidor MCP híbrido para orquestração de múltiplos agentes de IA com fallback inteligente**

O MCP Orchestrator é um servidor [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) que integra múltiplos provedores de IA (APIs, CLIs e LLMs locais) com fallback automático, permitindo alta disponibilidade e otimização de custos.

## 🚀 Características

- **Múltiplos Agentes**: Claude API/CLI, Gemini API/CLI, OpenAI, Mistral, Cohere, Perplexity
- **LLMs Locais**: Ollama, LM Studio (gratuitos e privados)
- **Fallback Inteligente**: Alternância automática entre agentes em caso de falha
- **Otimização de Custos**: Priorização de agentes gratuitos (CLIs, LLMs locais)
- **Alta Disponibilidade**: Múltiplas opções de fallback garantem resposta sempre
- **Arquitetura Extensível**: Fácil adição de novos agentes e ferramentas
- **Logging Estruturado**: Logs detalhados para monitoramento e debugging
- **Configuração Flexível**: Suporte a variáveis de ambiente e arquivos de config

## 📋 Pré-requisitos

- Python 3.10+
- (Opcional) Docker para LLMs locais
- (Opcional) CLIs do Claude e Gemini instalados
- (Opcional) Ollama ou LM Studio para LLMs locais

## 🛠️ Instalação

### Método 1: Instalação Local

```bash
# Clone o repositório
git clone <repository-url>
cd mcp_orchestrator

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API
```

### Método 2: Docker

```bash
# Clone o repositório
git clone <repository-url>
cd mcp_orchestrator

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env

# Execute com Docker Compose
docker-compose up -d
```

### Método 3: Script Automatizado

```bash
# Execute o script de instalação
chmod +x scripts/install.sh
./scripts/install.sh
```

## ⚙️ Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```bash
# API Keys (opcionais)
ANTHROPIC_API_KEY="sk-ant-..."      # Claude API
GOOGLE_API_KEY="AIza..."            # Gemini API
OPENAI_API_KEY="sk-..."             # OpenAI API
MISTRAL_API_KEY="..."               # Mistral API
COHERE_API_KEY="..."                # Cohere API
PERPLEXITY_API_KEY="pplx-..."       # Perplexity API

# LLMs Locais (opcionais)
OLLAMA_BASE_URL="http://localhost:11434"
LM_STUDIO_BASE_URL="http://localhost:1234/v1"

# Configurações do Servidor
LOG_LEVEL="INFO"
TIMEOUT=30
MAX_RETRIES=3
```

### Configuração de Agentes

Edite `config/agents.yaml` para personalizar:

```yaml
agents:
  claude_api:
    enabled: true
    priority: 1
    model: "claude-3-sonnet-20240229"
    max_tokens: 2048
    timeout: 30
    fallback_chain: ["claude_cli", "gemini_api", "gemini_cli"]
```

## 🚀 Uso

### Iniciar o Servidor

```bash
# Método direto
python src/mcp_orchestrator/server.py

# Via módulo
python -m mcp_orchestrator.server

# Via Docker
docker-compose up -d
```

### Integração com Clientes MCP

#### Cursor

Adicione ao `settings.json` do Cursor:

```json
{
  "mcp": {
    "servers": {
      "orchestrator": {
        "command": "python",
        "args": ["/caminho/para/mcp_orchestrator/src/mcp_orchestrator/server.py"]
      }
    }
  }
}
```

#### Claude Desktop

Adicione ao `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "orchestrator": {
      "command": "python",
      "args": ["/caminho/para/mcp_orchestrator/src/mcp_orchestrator/server.py"]
    }
  }
}
```

### Exemplos de Uso

#### 1. Resposta Básica

```python
# Via MCP client
response = mcp_client.call_tool("get_ai_response", {
    "prompt": "Explique o que é inteligência artificial",
    "agent": "claude_api"
})
```

#### 2. Com Fallback Automático

```python
# Se claude_api falhar, automaticamente tenta claude_cli, depois gemini_api
response = mcp_client.call_tool("get_ai_response", {
    "prompt": "Analise este código Python",
    "agent": "claude_api",
    "params": {"max_tokens": 1000}
})
```

#### 3. Usando LLM Local

```python
# Usa Ollama local (gratuito)
response = mcp_client.call_tool("get_ai_response", {
    "prompt": "Gere um script de backup",
    "agent": "ollama",
    "params": {"model": "llama3.1:8b"}
})
```

## 🧪 Testes

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar testes
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=mcp_orchestrator --cov-report=html

# Linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

## 📊 Monitoramento

### Logs

Os logs são escritos em:
- `stderr`: Logs de debug e erro
- `logs/mcp_orchestrator.log`: Logs estruturados
- `logs/errors.log`: Apenas erros

### Métricas

Acesse métricas em tempo real:

```bash
# Health check
curl http://localhost:8000/health

# Métricas Prometheus
curl http://localhost:8000/metrics
```

### Dashboard Grafana

Acesse o dashboard em `http://localhost:3000` (se configurado).

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. "Claude CLI not installed"
```bash
# Instale o Claude CLI
npm install -g @anthropic-ai/claude
```

#### 2. "Ollama connection failed"
```bash
# Inicie o Ollama
ollama serve

# Baixe um modelo
ollama pull llama3.1:8b
```

#### 3. "API key not valid"
```bash
# Verifique suas chaves no .env
cat .env | grep API_KEY
```

### Logs Detalhados

```bash
# Aumentar nível de log
export LOG_LEVEL=DEBUG
python src/mcp_orchestrator/server.py
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Desenvolvimento

```bash
# Instalar em modo desenvolvimento
pip install -e .

# Executar testes antes de commit
make test
make lint
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [FastMCP](https://github.com/jlowin/fastmcp) - Framework MCP
- [Anthropic](https://anthropic.com/) - Claude API
- [Google AI](https://ai.google.dev/) - Gemini API
- [Ollama](https://ollama.ai/) - LLMs locais

## 📞 Suporte

- 📧 Email: [seu-email@exemplo.com]
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/mcp-orchestrator/issues)
- 📖 Documentação: [docs/](docs/)

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!** 