# CLAUDE.md

Este arquivo fornece orientações para o Claude Code (claude.ai/code) ao trabalhar com código neste repositório.

**IMPORTANTE**: Sempre se comunique em português brasileiro com o usuário Marco. Esta é uma preferência essencial do desenvolvedor.

## Visão Geral do Repositório

Este é o **Ecossistema Macspark** - uma plataforma abrangente composta por três componentes principais:

1. **Macspark-App**: Aplicação web React 18 + TypeScript com agentes de IA, ferramentas de colaboração e recursos empresariais
2. **Macspark-MCPs**: Orquestrador Python baseado em MCP (Model Context Protocol) para coordenação de múltiplos agentes LLM  
3. **Macspark-Setup**: Automação de infraestrutura Docker Swarm com mais de 60 serviços empresariais

## Arquitetura

### Macspark-App (Plataforma Frontend)
- **React 18** com TypeScript, sistema de build Vite
- **Supabase** backend com colaboração em tempo real
- **Tailwind CSS** com sistema de design
- **Progressive Web App** com capacidades offline
- **Agentes de IA**: SparkOne (principal), SparkPolyglot (tutor de idiomas), IA Proativa
- **Colaboração em tempo real** com integração WebSocket
- **Recursos empresariais**: Multi-tenancy, centro de segurança, gerenciamento de API

### Macspark-MCPs (Orquestrador de IA)
- **Python 3.10+** servidor MCP para coordenação de agentes de IA
- **FastMCP** framework com suporte a múltiplos provedores
- **Deploy híbrido**: APIs (Claude, OpenAI, Gemini) + LLMs Locais (Ollama, LM Studio)
- **Fallback inteligente** em cadeia para alta disponibilidade
- **Otimização de custos** através da priorização de LLMs locais

### Macspark-Setup (Infraestrutura)
- **Docker Swarm** orquestração com proxy Traefik
- **60+ serviços** incluindo monitoramento, produtividade, IA, segurança
- **Cloudflare Tunnel** integração para servidores domésticos
- **SSL automático** com Let's Encrypt
- **Stack de monitoramento empresarial** (Prometheus, Grafana, Netdata)

## Comandos de Desenvolvimento

### Macspark-App
```bash
# Desenvolvimento
npm run dev                    # Iniciar servidor dev
npm run build                  # Build de produção  
npm run build:dev             # Build de desenvolvimento
npm run preview               # Preview do build

# Qualidade de Código
npm run lint                  # Verificação ESLint
npm run lint:fix             # Corrigir problemas ESLint
npm run type-check           # Verificação TypeScript
npm run format              # Formatação Prettier

# Testes
npm run test                 # Executar testes Vitest
npm run test:e2e            # Testes E2E Cypress
npm run test:coverage      # Relatório de cobertura

# Otimização
npm run optimize:build      # Remover console logs + build prod
npm run clean              # Limpar artefatos de build
```

### Macspark-MCPs
```bash
# Desenvolvimento
make install-dev            # Instalar dependências dev
make run-dev               # Executar com debug logging
make test                  # Executar todos os testes
make test-unit            # Apenas testes unitários

# Qualidade de Código  
make format               # Formatação Black + isort
make lint                # Verificação Flake8 + MyPy
make security-check      # Escaneamento de segurança Bandit

# Docker
make docker-build        # Build da imagem Docker
make docker-run         # Executar com Docker Compose

# LLMs Locais
make setup-local-llms   # Instalar modelos Ollama
make health-check       # Verificar saúde dos serviços
```

### Macspark-Setup
```bash
# Instalação Principal
sudo bash install.sh        # Setup completo de infraestrutura

# Gerenciamento de Serviços
docker service ls           # Listar todos os serviços
docker stack deploy -c stacks/[categoria]/[servico].yml [nome]
docker service logs -f [servico]

# Exemplos
docker stack deploy -c stacks/ai/ollama.yml ollama
docker stack deploy -c stacks/apps/n8n.yml n8n
```

## Estrutura do Projeto

### Diretórios Principais
```
Macspark-App/
├── src/
│   ├── components/         # Componentes React por funcionalidade
│   ├── pages/             # Componentes de rota
│   ├── hooks/             # Custom React hooks
│   ├── services/          # Integração com APIs
│   ├── utils/             # Utilitários e helpers
│   └── types/             # Definições TypeScript
├── docs/                  # Documentação abrangente
└── scripts/               # Scripts de build e deploy

Macspark-MCPs/mcp_orchestrator/
├── src/mcp_orchestrator/  # Pacote Python principal
├── config/                # Configurações de agentes
├── tests/                 # Suítes de teste
└── docs/                  # Documentação da API

Macspark-Setup/
├── stacks/                # Definições de stacks Docker  
├── scripts/               # Scripts de instalação
└── docs/                  # Guias de infraestrutura
```

### Arquivos Importantes
- `Macspark-App/package.json`: Dependências e scripts
- `Macspark-MCPs/mcp_orchestrator/pyproject.toml`: Configuração do projeto Python
- `Macspark-Setup/install.sh`: Automação de infraestrutura
- `*/README.md`: Documentação específica dos componentes

## Fluxo de Desenvolvimento

### Antes de Fazer Alterações
1. **Executar linting**: `npm run lint` (App) ou `make lint` (MCPs)
2. **Verificação de tipos**: `npm run type-check` (App) ou `make lint` (MCPs)  
3. **Executar testes**: `npm run test` (App) ou `make test` (MCPs)

### Padrões de Código
- **TypeScript**: Modo strict habilitado, cobertura de tipos completa obrigatória
- **React**: Componentes funcionais com hooks, sem componentes de classe
- **Python**: Formatação Black, type hints obrigatórios, limite de 88 caracteres
- **Docker**: Builds multi-stage, escaneamento de segurança habilitado

### Pontos de Integração de IA
- **SparkOne**: Centro de controle de missões em `src/components/mission-center/`
- **SparkPolyglot**: Aprendizado de idiomas em `src/components/polyglot/`
- **MCP Orchestrator**: Coordenação de IA em `src/mcp_orchestrator/server.py`

### Integração de Banco de Dados
- **Supabase**: Banco de dados primário com subscrições em tempo real
- **PostgreSQL**: Banco de dados de analytics local (componente Setup)
- **Redis**: Cache e armazenamento de sessões

### Considerações de Segurança
- **Variáveis de ambiente**: Nunca commitar chaves de API ou secrets
- **Rate limiting**: Implementado nas camadas Traefik e aplicação
- **SSL/TLS**: Auto-gerenciado pelo Let's Encrypt através do Traefik
- **Validação de entrada**: Schemas Zod para todas as entradas de API

### Notas de Performance
- **Otimização de bundle**: Vite com code splitting e tree shaking
- **Otimização de imagem**: Imagens responsivas com estados de carregamento
- **Estratégia de cache**: Cache multi-camadas (Redis, browser, CDN)
- **Score Lighthouse**: Meta de 95+ no score de performance

### Estratégia de Testes
- **Testes unitários**: Vitest para utilitários e hooks
- **Testes de componente**: React Testing Library
- **Testes E2E**: Cypress para fluxos críticos do usuário
- **Testes Python**: Pytest com suporte async

### Deploy
- **Staging**: Auto-deploy da branch `develop`
- **Produção**: Deploy manual da branch `main`
- **Infraestrutura**: Docker Swarm com deploys zero-downtime
- **Monitoramento**: Métricas Prometheus, dashboards Grafana

## Problemas Comuns e Soluções

### Falhas de Build
- **Problemas de memória**: Aumentar heap size do Node.js com `--max-old-space-size=4096`
- **Erros de tipo**: Executar `npm run type-check` para diagnósticos detalhados
- **Erros de importação**: Verificar aliases de caminho em `vite.config.ts`

### Problemas de Conexão MCP
- **LLMs locais**: Verificar se Ollama/LM Studio estão rodando com `make health-check`
- **Credenciais de API**: Verificar se variáveis de ambiente estão configuradas corretamente
- **Rede**: Garantir que redes Docker estão configuradas adequadamente

### Problemas de Infraestrutura
- **Startup de serviços**: Verificar `docker service logs [servico]` para erros
- **Problemas SSL**: Verificar configuração DNS e Cloudflare Tunnel
- **Limites de recursos**: Monitorar com Netdata ou `docker stats`