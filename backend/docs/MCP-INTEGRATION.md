# Integração com MCP (Model Context Protocol)

Este guia explica como conectar o projeto **facebook-ads-ai-agent** a servidores MCP externos, permitindo que agentes (ex.: Claude, Cursor) interajam com o n8n e o Notion de forma programática.

## Visão Geral

- O backend FastAPI continua consumindo as integrações via REST/SDK (Facebook, Notion, n8n).
- O MCP roda como um serviço separado (normalmente em Node/TypeScript) e expõe ferramentas que o agente pode chamar.
- O repositório `C:\Users\marco\Macspark\mcp_orchestrator` contém o esqueleto para criar esses servidores MCP.

## 1. Servidor MCP para n8n

### Opção A – Reutilizar `n8n-mcp-server`

1. Instale as dependências no projeto MCP (Node requerido):
   ```bash
   git clone https://github.com/leonardsellem/n8n-mcp-server.git
   cd n8n-mcp-server
   npm install
   npm run build
   ```
2. Configure as variáveis:
   ```bash
   export N8N_MODE=true
   export MCP_MODE=http
   export MCP_AUTH_TOKEN=<token-seguro>
   export AUTH_TOKEN=$MCP_AUTH_TOKEN
   export N8N_API_URL=https://<sua-instancia-n8n>
   export N8N_API_KEY=<api-key-n8n>
   export PORT=3000
   ```
3. Execute:
   ```bash
   npm start
   ```
4. No agente (ex.: `claude.json`), registre o servidor:
   ```json
   {
     "mcpServers": {
       "n8n": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/mcp-remote@latest",
           "connect",
           "http://localhost:3000/mcp"
         ],
         "env": {
           "MCP_AUTH_TOKEN": "<token-seguro>"
         }
       }
     }
   }
   ```

### Opção B – Implementar no `mcp_orchestrator`

1. Use o template do diretório `mcp_orchestrator` para criar um servidor MCP em TypeScript.
2. Utilize o pacote `@modelcontextprotocol/sdk` para expor ferramentas (ex.: listar, criar e ativar workflows via API n8n).
3. Replique o bloco de configuração JSON acima para registrar o novo servidor no agente.

## 2. Servidor MCP para Notion

Não há um servidor oficial pronto. Você pode:

1. Criar um novo servidor MCP no `mcp_orchestrator` utilizando o SDK Python/Node do Notion.
2. Implementar ferramentas como:
   - `listDatabases`
   - `createPage`
   - `appendBlock`
3. Registrar o servidor no agente com a mesma estrutura de configuração (`mcpServers`).

Sugestão de inicialização com a SDK Python (para backend e testes):
```python
import os
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])
```
O servidor MCP (Node) precisará chamar o SDK oficial (JavaScript) ou expor um wrapper REST.

## 3. Segurança

- Armazene os tokens (`N8N_API_KEY`, `NOTION_TOKEN`, `MCP_AUTH_TOKEN`) em um cofre seguro.
- Use tokens separados por ambiente (dev/homolog/prod).
- Configure HTTPS ou execute behind proxy com TLS.

## 4. Checklist de Integração

- [ ] Servidor MCP compilado e rodando (Node/PM2/etc.)
- [ ] Variáveis de ambiente ajustadas (`N8N_API_URL`, `N8N_API_KEY`, etc.)
- [ ] Arquivo de configuração do agente (Claude/Cursor) referenciando o comando `npx ...`
- [ ] Logs revisados (verificar acesso autorizado)
- [ ] Documentação interna atualizada com endpoints/tarefas disponíveis

## 5. Referências

- [n8n-mcp-server (GitHub)](https://github.com/leonardsellem/n8n-mcp-server)
- [Modelo `mcp-remote` oficial](https://www.npmjs.com/package/@modelcontextprotocol/mcp-remote)
- [Notion SDK Python](https://github.com/ramnes/notion-sdk-py)
- [Model Context Protocol](https://modelcontextprotocol.com/)
