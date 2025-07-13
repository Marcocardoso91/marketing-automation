# Guia dos Agentes Cursor AI - Ecossistema Macspark

Este guia explica como utilizar os agentes especializados do Cursor AI configurados para o ecossistema Macspark.

## Estrutura de Agentes

O projeto possui **5 agentes especializados** configurados através de workspaces:

```
Macspark/
├── .cursor/                # 🤖 Agente Geral (Coordenador)
├── Macspark-App/.cursor/   # ⚛️ Agente React Frontend
├── Macspark-Setup/.cursor/ # 🐳 Agente DevOps/Docker
├── Macspark-MCPs/.cursor/  # 🐍 Agente Python MCP
└── Macspark-Docs/.cursor/  # 📚 Agente Documentação
```

## Como Usar

### 1. Agente Geral (Raiz)
**Localização**: `/Macspark/.cursor/`
**Especialidade**: Coordenação geral do ecossistema

**Use quando**:
- Trabalhar com múltiplos componentes
- Planejar features cross-project
- Arquitetura geral do sistema
- Integração entre componentes

**Exemplo de prompt**:
```
Preciso integrar o SparkOne (Macspark-App) com o MCP Orchestrator (Macspark-MCPs). 
Como estruturar a comunicação?
```

### 2. Agente React Frontend
**Localização**: `/Macspark-App/.cursor/`
**Especialidade**: React 18, TypeScript, Tailwind CSS

**Use quando**:
- Desenvolver componentes React
- Implementar funcionalidades frontend
- Trabalhar com agentes de IA (SparkOne, SparkPolyglot)
- Otimizar performance frontend

**Exemplo de prompt**:
```
Crie um componente React para o Mission Center do SparkOne que exiba 
métricas em tempo real usando WebSocket do Supabase.
```

**Comandos contextuais**:
```
@package.json - Ver dependências
@src/components - Analisar componentes existentes
@tailwind.config.ts - Verificar configuração de design
```

### 3. Agente DevOps/Docker
**Localização**: `/Macspark-Setup/.cursor/`
**Especialidade**: Docker Swarm, automação, infraestrutura

**Use quando**:
- Configurar novos serviços Docker
- Criar scripts de automação
- Monitoramento e observabilidade
- Segurança e hardening

**Exemplo de prompt**:
```
Crie um novo stack Docker para deploy do MCP Orchestrator com 
health checks, métricas Prometheus e integração Traefik.
```

**Comandos contextuais**:
```
@stacks/ai - Ver serviços de IA
@install.sh - Analisar automação principal
@scripts/ - Ver scripts disponíveis
```

### 4. Agente Python MCP
**Localização**: `/Macspark-MCPs/.cursor/`
**Especialidade**: Python, MCP, FastAPI, coordenação de IA

**Use quando**:
- Desenvolver orquestrador MCP
- Implementar novos agentes IA
- Configurar fallback entre provedores
- Otimizar performance Python

**Exemplo de prompt**:
```
Implemente um novo agente MCP para análise de código que use 
fallback de Ollama local para Claude API.
```

**Comandos contextuais**:
```
@config/agents.yaml - Ver configuração de agentes
@src/mcp_orchestrator/server.py - Analisar servidor principal
@Makefile - Ver comandos disponíveis
```

### 5. Agente Documentação
**Localização**: `/Macspark-Docs/.cursor/`
**Especialidade**: Documentação técnica, Markdown

**Use quando**:
- Criar/atualizar documentação
- Escrever guias técnicos
- Documentar APIs e arquitetura
- Manter READMEs atualizados

**Exemplo de prompt**:
```
Atualize o ARCHITECTURE.md com a nova integração entre 
Macspark-App e Macspark-MCPs via WebSocket.
```

## Dicas de Uso Avançado

### Contexto Cruzado
Para trabalhar com múltiplos componentes:

```
Baseado no @Macspark-App/src/config/sparkone.config.ts, 
atualize o @Macspark-MCPs/config/agents.yaml para incluir 
as novas configurações do SparkOne.
```

### Referências Úteis
- `@CLAUDE.md` - Instruções globais do projeto
- `@README.md` - Documentação específica de cada componente
- `@package.json` / `@pyproject.toml` - Dependências
- `@.env.example` - Variáveis de ambiente

### Comandos de Terminal
Os agentes conhecem os comandos específicos:

**Macspark-App**:
```bash
npm run dev          # Desenvolvimento
npm run lint         # Verificar código
npm run type-check   # TypeScript
```

**Macspark-Setup**:
```bash
./install.sh                    # Instalação completa
docker stack deploy -c [file]   # Deploy
./scripts/health-monitor.sh     # Monitoramento
```

**Macspark-MCPs**:
```bash
make run-dev        # Desenvolvimento
make lint           # Verificar código
make test           # Executar testes
```

## Fluxo de Trabalho Recomendado

1. **Planejamento**: Use o agente geral (raiz) para arquitetura
2. **Implementação**: Mude para o workspace específico
3. **Integração**: Volte ao agente geral para conectar componentes
4. **Documentação**: Use o agente de docs para atualizar documentação
5. **Deploy**: Use o agente DevOps para infraestrutura

## Troubleshooting

### Agente não reconhece contexto
- Verifique se está no workspace correto
- Use referências explícitas: `@arquivo.ts`
- Reinicie o Cursor se necessário

### Conflito entre agentes
- Cada workspace tem suas próprias regras
- O agente mais próximo do arquivo atual tem prioridade
- Use o agente geral para decisões arquiteturais

### Performance lenta
- Limite o contexto a arquivos relevantes
- Use `.cursor/settings.json` para excluir pastas grandes
- Evite incluir `node_modules` ou `dist` no contexto

---

**💡 Dica**: Sempre mencione o componente específico no prompt para melhor contexto!

Exemplo: "No **Macspark-App**, crie um componente..." vs "Crie um componente..."