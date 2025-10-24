# 🤖 MCP Server - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 🎯 O Que É o MCP Server

O **MCP Server** (Model Context Protocol) é um servidor que expõe a documentação do Marketing Automation Platform para agentes de IA, permitindo acesso inteligente e contextual aos recursos de documentação.

### Funcionalidades
- ✅ **Busca semântica** na documentação
- ✅ **Leitura de recursos** específicos
- ✅ **Exemplos de código** automáticos
- ✅ **Troubleshooting** inteligente
- ✅ **Integração** com Claude Desktop e outros clientes MCP

---

## 🏗️ Arquitetura do Servidor

### Componentes Principais

```
mcp-server/
├── src/
│   ├── index.ts          # Servidor principal
│   ├── resources.ts      # Gerenciamento de recursos
│   ├── tools.ts          # Ferramentas disponíveis
│   └── types.ts          # Tipos TypeScript
├── package.json          # Dependências Node.js
├── tsconfig.json         # Configuração TypeScript
└── README.md            # Este arquivo
```

### Recursos Disponíveis

| Recurso | URI | Descrição |
|---------|-----|-----------|
| **Documentação Principal** | `docs://README.md` | README principal do projeto |
| **Guia de Uso** | `docs://USER-GUIDE.md` | Guia completo de uso |
| **API Reference** | `docs://api/agent-api/API-REFERENCE.md` | Referência completa da API |
| **Troubleshooting** | `docs://reference/troubleshooting/TROUBLESHOOTING.md` | Guia de resolução de problemas |
| **Configuração** | `docs://reference/configuration/ENV-VARS.md` | Variáveis de ambiente |
| **Arquitetura** | `docs://architecture/ARCHITECTURE.md` | Visão geral da arquitetura |
| **Integrações** | `docs://api/integrations/` | Guias de integração (N8N, Notion) |

### Tools Disponíveis

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| **list_resources** | Lista todos os recursos disponíveis | - |
| **read_resource** | Lê conteúdo de um recurso específico | `uri` |
| **search_docs** | Busca semântica na documentação | `query`, `limit` |
| **get_examples** | Obtém exemplos de código | `topic`, `language` |
| **troubleshoot** | Diagnostica problemas comuns | `error`, `context` |

---

## 🚀 Instalação

### Pré-requisitos
- ✅ Node.js 18+ instalado
- ✅ npm ou yarn
- ✅ TypeScript (opcional, para desenvolvimento)

### Instalação Rápida

```bash
# 1. Navegar para o diretório
cd mcp-server

# 2. Instalar dependências
npm install

# 3. Compilar TypeScript
npm run build

# 4. Testar servidor
npm test
```

### Instalação com Script

```bash
# Script automatizado (Linux/Mac)
chmod +x install.sh
./install.sh

# Script automatizado (Windows)
.\install.ps1
```

---

## 🔧 Configuração

### Arquivo de Configuração

O servidor usa o arquivo `mcp-config.json` na raiz do projeto:

```json
{
  "mcpServers": {
    "marketing-automation-docs": {
      "command": "node",
      "args": ["mcp-server/dist/index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

### Variáveis de Ambiente

```bash
# Configuração do servidor
NODE_ENV=production
LOG_LEVEL=info
DOCS_PATH=../docs

# Configuração de cache
CACHE_TTL=3600
MAX_CACHE_SIZE=100
```

---

## 🚀 Como Executar

### Desenvolvimento

```bash
# Modo desenvolvimento com hot reload
npm run dev

# Com debug ativado
DEBUG=mcp-server npm run dev
```

### Produção

```bash
# Compilar e executar
npm run build
npm start

# Com PM2 (recomendado)
pm2 start dist/index.js --name mcp-server
```

### Docker

```bash
# Build da imagem
docker build -t mcp-server .

# Executar container
docker run -d --name mcp-server -p 3000:3000 mcp-server
```

---

## 🧪 Como Testar

### Testes Unitários

```bash
# Executar todos os testes
npm test

# Testes com coverage
npm run test:coverage

# Testes específicos
npm test -- --grep "list_resources"
```

### Testes de Integração

```bash
# Testar servidor completo
npm run test:integration

# Testar com cliente MCP
npm run test:client
```

### Testes Manuais

```bash
# Testar recursos
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "resources/list"}'

# Testar busca
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "search_docs", "arguments": {"query": "API endpoints"}}}'
```

---

## 🔌 Integração com Clientes MCP

### Claude Desktop

1. **Editar configuração:** `~/.claude-desktop/config.json`
2. **Adicionar servidor:**
   ```json
   {
     "mcpServers": {
       "marketing-automation-docs": {
         "command": "node",
         "args": ["/path/to/mcp-server/dist/index.js"]
       }
     }
   }
   ```
3. **Reiniciar Claude Desktop**

### Outros Clientes

#### Cursor
```json
{
  "mcp": {
    "servers": {
      "marketing-docs": {
        "command": "node",
        "args": ["mcp-server/dist/index.js"]
      }
    }
  }
}
```

#### Continue
```json
{
  "mcpServers": {
    "marketing-docs": {
      "command": "node",
      "args": ["mcp-server/dist/index.js"]
    }
  }
}
```

---

## 🛠️ Desenvolvimento Local

### Estrutura do Projeto

```
mcp-server/
├── src/
│   ├── index.ts          # Ponto de entrada
│   ├── server.ts         # Servidor MCP
│   ├── resources.ts      # Gerenciamento de recursos
│   ├── tools.ts          # Implementação das tools
│   ├── search.ts         # Busca semântica
│   ├── examples.ts       # Geração de exemplos
│   └── types.ts          # Tipos TypeScript
├── tests/
│   ├── unit/            # Testes unitários
│   ├── integration/     # Testes de integração
│   └── fixtures/        # Dados de teste
├── package.json
├── tsconfig.json
└── README.md
```

### Adicionar Novos Recursos

1. **Editar `src/resources.ts`:**
   ```typescript
   export const resources = [
     // ... recursos existentes
     {
       uri: "docs://new-guide.md",
       name: "New Guide",
       description: "Description of the new guide",
       mimeType: "text/markdown"
     }
   ];
   ```

2. **Atualizar tipos em `src/types.ts`**
3. **Adicionar testes em `tests/`**
4. **Recompilar:** `npm run build`

### Adicionar Novas Tools

1. **Editar `src/tools.ts`:**
   ```typescript
   export const tools = [
     // ... tools existentes
     {
       name: "new_tool",
       description: "Description of the new tool",
       inputSchema: {
         type: "object",
         properties: {
           param1: { type: "string" }
         }
       }
     }
   ];
   ```

2. **Implementar função:**
   ```typescript
   export async function new_tool(params: any) {
     // Implementação da tool
     return { result: "success" };
   }
   ```

3. **Adicionar testes**
4. **Recompilar:** `npm run build`

---

## 📊 Monitoramento

### Métricas Importantes

- **Requests por minuto**
- **Tempo de resposta médio**
- **Taxa de erro**
- **Uso de cache**
- **Recursos mais acessados**

### Logs

```bash
# Ver logs em tempo real
npm run logs

# Filtrar por nível
npm run logs -- --level error

# Salvar logs em arquivo
npm run logs > logs/mcp-server.log
```

### Health Check

```bash
# Verificar saúde do servidor
curl http://localhost:3000/health

# Response esperado:
{
  "status": "healthy",
  "uptime": 3600,
  "version": "1.0.0",
  "resources": 15,
  "tools": 5
}
```

---

## 🚨 Troubleshooting

### Problemas Comuns

#### ❌ Servidor Não Inicia
**Sintomas:** `Error: Cannot find module`

**Soluções:**
1. **Verificar dependências:** `npm install`
2. **Verificar compilação:** `npm run build`
3. **Verificar Node.js:** `node --version` (deve ser 18+)

#### ❌ Cliente MCP Não Conecta
**Sintomas:** Cliente não encontra servidor

**Soluções:**
1. **Verificar configuração** do cliente
2. **Verificar caminho** do executável
3. **Verificar permissões** de execução
4. **Testar manualmente:** `node dist/index.js`

#### ❌ Recursos Não Carregam
**Sintomas:** `Resource not found`

**Soluções:**
1. **Verificar caminho** dos arquivos
2. **Verificar permissões** de leitura
3. **Verificar estrutura** de diretórios
4. **Testar acesso:** `ls -la docs/`

#### ❌ Busca Não Funciona
**Sintomas:** `Search failed` ou resultados vazios

**Soluções:**
1. **Verificar índice** de busca
2. **Verificar dependências** de busca
3. **Verificar configuração** do cache
4. **Reconstruir índice:** `npm run rebuild-index`

### Debugging

#### Ativar Debug
```bash
# Debug completo
DEBUG=mcp-server:* npm run dev

# Debug específico
DEBUG=mcp-server:search npm run dev
```

#### Verificar Logs
```bash
# Logs detalhados
npm run logs -- --level debug

# Filtrar por componente
npm run logs -- --grep "resources"
```

#### Testar Componentes
```bash
# Testar recursos
npm run test:resources

# Testar busca
npm run test:search

# Testar tools
npm run test:tools
```

---

## 📈 Performance

### Otimizações

1. **Cache de recursos** para acesso rápido
2. **Índice de busca** pré-construído
3. **Compressão** de respostas
4. **Pool de conexões** para arquivos

### Benchmarks

| Operação | Tempo Médio | P95 |
|-----------|-------------|-----|
| **list_resources** | 50ms | 100ms |
| **read_resource** | 100ms | 200ms |
| **search_docs** | 200ms | 500ms |
| **get_examples** | 150ms | 300ms |

### Monitoramento

```bash
# Verificar performance
npm run benchmark

# Monitorar em tempo real
npm run monitor

# Gerar relatório
npm run report
```

---

## 🔗 Recursos Adicionais

### Documentação
- **MCP Specification:** https://modelcontextprotocol.io
- **Claude Desktop:** https://claude.ai/desktop
- **TypeScript:** https://www.typescriptlang.org

### Comunidade
- **MCP Discord:** https://discord.gg/mcp
- **GitHub Issues:** [Criar issue](https://github.com/your-repo/issues)
- **Documentação:** [docs/MCP-DOCUMENTATION-GUIDE.md](../docs/MCP-DOCUMENTATION-GUIDE.md)

### Suporte
- **Troubleshooting:** [docs/reference/troubleshooting/TROUBLESHOOTING.md](../docs/reference/troubleshooting/TROUBLESHOOTING.md)
- **API Reference:** [docs/api/agent-api/API-REFERENCE.md](../docs/api/agent-api/API-REFERENCE.md)

---

## ✅ Checklist de Configuração

### Instalação Básica
- [ ] ✅ Node.js 18+ instalado
- [ ] ✅ Dependências instaladas
- [ ] ✅ Projeto compilado
- [ ] ✅ Testes passando
- [ ] ✅ Servidor funcionando

### Integração MCP
- [ ] ✅ Cliente MCP configurado
- [ ] ✅ Conexão estabelecida
- [ ] ✅ Recursos acessíveis
- [ ] ✅ Tools funcionando
- [ ] ✅ Busca operacional

### Produção
- [ ] ✅ Configuração otimizada
- [ ] ✅ Monitoramento ativo
- [ ] ✅ Logs configurados
- [ ] ✅ Backup implementado
- [ ] ✅ Documentação atualizada

---

**💡 Dica:** Use `npm run dev` para desenvolvimento e `npm start` para produção!**
