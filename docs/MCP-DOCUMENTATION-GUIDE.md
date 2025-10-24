# Guia de Uso MCP - Marketing Automation Platform

**Versão:** 1.0.0  
**Data:** 23 de Outubro, 2025  
**Status:** ✅ Implementado e Funcional

---

## 🎯 O Que é MCP?

O **Model Context Protocol (MCP)** permite que agentes de IA acessem e consultem a documentação do projeto de forma inteligente. Com MCP, você pode:

- 🔍 **Buscar documentação** com queries em linguagem natural
- 📖 **Ler recursos específicos** da documentação
- 🛠️ **Obter exemplos de código** para features específicas
- 🆘 **Troubleshoot problemas** automaticamente
- 📚 **Navegar pela documentação** de forma semântica

---

## 🚀 Configuração Rápida

### 1. Instalar Dependências

```bash
# Navegar para o servidor MCP
cd mcp-server

# Instalar dependências
npm install

# Compilar TypeScript
npm run build
```

### 2. Configurar Cliente MCP

#### Para Claude Desktop
Adicione ao arquivo de configuração do Claude:

```json
{
  "mcpServers": {
    "marketing-automation-docs": {
      "command": "node",
      "args": ["/caminho/para/marketing-automation/mcp-server/dist/index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

#### Para Outros Clientes MCP
```bash
# Iniciar servidor MCP
node mcp-server/dist/index.js
```

### 3. Testar Conexão

```bash
# Verificar se servidor está rodando
curl http://localhost:3000/health

# Testar busca
curl -X POST http://localhost:3000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "como configurar Facebook API"}'
```

---

## 📚 Recursos Disponíveis

### Estrutura de URIs

Todos os recursos seguem o padrão:
```
docs://marketing-automation/[categoria]/[arquivo]
```

### Categorias Disponíveis

#### 🚀 Getting Started
- `docs://marketing-automation/overview` - Visão geral do projeto
- `docs://marketing-automation/quick-start` - Guia de início rápido
- `docs://marketing-automation/installation` - Instalação detalhada

#### 🏗️ Architecture
- `docs://marketing-automation/architecture/overview` - Arquitetura do sistema
- `docs://marketing-automation/architecture/decisions` - Decisões arquiteturais
- `docs://marketing-automation/architecture/dependencies` - Mapa de dependências

#### 📖 Guides
- `docs://marketing-automation/guides/user/daily-usage` - Uso diário
- `docs://marketing-automation/guides/developer/contributing` - Contribuição
- `docs://marketing-automation/guides/operations/deployment` - Deploy

#### 🔌 API
- `docs://marketing-automation/api/agent-api/endpoints` - Endpoints da API
- `docs://marketing-automation/api/integrations/n8n` - Integração N8N
- `docs://marketing-automation/api/integrations/notion` - Integração Notion

#### 📋 Reference
- `docs://marketing-automation/reference/troubleshooting/common-issues` - Problemas comuns
- `docs://marketing-automation/reference/configuration/env-vars` - Variáveis de ambiente
- `docs://marketing-automation/reference/glossary` - Glossário técnico

---

## 🛠️ Ferramentas Disponíveis

### 1. `search_docs` - Busca Semântica

Busca inteligente na documentação usando queries em linguagem natural.

**Parâmetros:**
- `query` (string, obrigatório): Query de busca
- `limit` (number, opcional): Número máximo de resultados (padrão: 10)

**Exemplo de uso:**
```javascript
// Buscar sobre autenticação
search_docs({
  query: "como configurar autenticação JWT",
  limit: 5
})

// Buscar sobre troubleshooting
search_docs({
  query: "erro 403 Facebook API",
  limit: 3
})
```

### 2. `get_examples` - Exemplos de Código

Obtém exemplos de código para features específicas.

**Parâmetros:**
- `feature` (string, obrigatório): Nome da feature

**Exemplo de uso:**
```javascript
// Obter exemplos de autenticação
get_examples({
  feature: "authentication"
})

// Obter exemplos de API
get_examples({
  feature: "api endpoints"
})
```

### 3. `troubleshoot` - Troubleshooting

Obtém ajuda para resolver problemas específicos.

**Parâmetros:**
- `error` (string, obrigatório): Mensagem de erro ou descrição do problema

**Exemplo de uso:**
```javascript
// Troubleshoot erro específico
troubleshoot({
  error: "Connection refused to localhost:8000"
})

// Troubleshoot problema de configuração
troubleshoot({
  error: "Facebook API returns 403"
})
```

---

## 💡 Casos de Uso Práticos

### 1. Desenvolvedor Novo no Projeto

```javascript
// Obter visão geral
read_resource("docs://marketing-automation/overview")

// Guia de início rápido
read_resource("docs://marketing-automation/quick-start")

// Como contribuir
read_resource("docs://marketing-automation/guides/developer/contributing")
```

### 2. Configurar Ambiente de Desenvolvimento

```javascript
// Buscar guias de setup
search_docs({
  query: "como configurar ambiente de desenvolvimento",
  limit: 5
})

// Obter exemplos de configuração
get_examples({
  feature: "environment setup"
})
```

### 3. Resolver Problema de Produção

```javascript
// Troubleshoot erro específico
troubleshoot({
  error: "Agent API not responding"
})

// Buscar soluções
search_docs({
  query: "API not responding troubleshooting",
  limit: 3
})
```

### 4. Entender Arquitetura

```javascript
// Arquitetura geral
read_resource("docs://marketing-automation/architecture/overview")

// Decisões arquiteturais
read_resource("docs://marketing-automation/architecture/decisions")

// Mapa de dependências
read_resource("docs://marketing-automation/architecture/dependencies")
```

### 5. Integrar com APIs Externas

```javascript
// Buscar sobre integrações
search_docs({
  query: "como integrar com N8N",
  limit: 5
})

// Obter exemplos de integração
get_examples({
  feature: "n8n integration"
})
```

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# Configurações do servidor MCP
export MCP_SERVER_PORT=3000
export MCP_SERVER_HOST=localhost
export MCP_LOG_LEVEL=info
export MCP_CACHE_TTL=3600
```

### Configuração de Cache

```json
{
  "cache": {
    "enabled": true,
    "ttl": 3600,
    "maxSize": 1000
  },
  "search": {
    "fuzzyThreshold": 0.3,
    "maxResults": 50
  }
}
```

### Configuração de Segurança

```json
{
  "security": {
    "rateLimit": {
      "enabled": true,
      "maxRequests": 100,
      "windowMs": 60000
    },
    "authentication": {
      "enabled": false,
      "apiKey": "optional-api-key"
    }
  }
}
```

---

## 📊 Monitoramento e Métricas

### Logs do Servidor

```bash
# Ver logs em tempo real
tail -f logs/mcp-server.log

# Ver logs de busca
grep "search" logs/mcp-server.log

# Ver logs de erro
grep "ERROR" logs/mcp-server.log
```

### Métricas Disponíveis

- **Total de recursos:** 166 documentos
- **Categorias:** 6 (getting-started, architecture, guides, api, reference, archive)
- **Ferramentas:** 3 (search_docs, get_examples, troubleshoot)
- **Busca semântica:** Implementada com Fuse.js
- **Cache:** Ativo com TTL configurável

---

## 🆘 Troubleshooting MCP

### Problemas Comuns

#### Servidor não inicia
```bash
# Verificar dependências
npm install

# Verificar compilação
npm run build

# Verificar permissões
chmod +x mcp-server/dist/index.js
```

#### Busca não funciona
```bash
# Verificar índice de busca
curl http://localhost:3000/health

# Reconstruir índice
curl -X POST http://localhost:3000/reindex
```

#### Cliente não conecta
```bash
# Verificar configuração do cliente
cat ~/.claude/mcp_config.json

# Testar conexão
telnet localhost 3000
```

### Logs de Debug

```bash
# Ativar logs detalhados
export MCP_LOG_LEVEL=debug

# Iniciar servidor com debug
node --inspect mcp-server/dist/index.js
```

---

## 🔗 Links Úteis

### Documentação MCP
- **Especificação MCP:** https://modelcontextprotocol.io/
- **SDK MCP:** https://github.com/modelcontextprotocol/sdk
- **Exemplos MCP:** https://github.com/modelcontextprotocol/examples

### Marketing Automation Platform
- **Repositório:** https://github.com/Marcocardoso91/marketing-automation
- **Documentação:** [INDEX.md](INDEX.md)
- **Quick Start:** [QUICK-START.md](getting-started/QUICK-START.md)

### Ferramentas Relacionadas
- **Claude Desktop:** https://claude.ai/desktop
- **Fuse.js:** https://fusejs.io/
- **Gray Matter:** https://github.com/jonschlinkert/gray-matter

---

## 📈 Roadmap MCP

### Versão 1.1 (Próximo mês)
- [ ] Busca por tags
- [ ] Filtros por categoria
- [ ] Histórico de buscas
- [ ] Bookmarks de recursos

### Versão 1.2 (2 meses)
- [ ] Busca por código
- [ ] Análise de dependências
- [ ] Sugestões automáticas
- [ ] Integração com IDE

### Versão 2.0 (3 meses)
- [ ] Busca por imagem
- [ ] Análise de diagramas
- [ ] Geração automática de docs
- [ ] Integração com CI/CD

---

## 🎯 Conclusão

O MCP para Marketing Automation Platform oferece uma interface inteligente e semântica para acessar toda a documentação do projeto. Com busca avançada, exemplos de código e troubleshooting automático, desenvolvedores podem encontrar informações rapidamente e resolver problemas de forma eficiente.

### Benefícios Principais
- ✅ **Busca semântica** em 166 documentos
- ✅ **3 ferramentas especializadas** para diferentes casos de uso
- ✅ **Integração nativa** com agentes de IA
- ✅ **Configuração simples** e flexível
- ✅ **Monitoramento completo** e logs detalhados

---

**Última atualização:** 23 de Outubro, 2025  
**Versão:** 1.0.0  
**Status:** ✅ Implementado e Funcional
