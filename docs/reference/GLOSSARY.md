# 📚 Glossário - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 🎯 Termos Técnicos do Projeto

### Agent API
**Definição:** API REST principal do sistema que gerencia campanhas, métricas e automações do Facebook Ads.

**Contexto:** Endpoint central em `http://localhost:8000` que expõe funcionalidades via REST API.

**Relacionado:** [API-REFERENCE.md](../api/agent-api/API-REFERENCE.md)

### Analytics
**Definição:** Componente responsável pela coleta, processamento e análise de dados de marketing.

**Contexto:** Inclui pipelines de dados, dashboards BI e insights automatizados.

**Relacionado:** [Analytics README](../../analytics/README.md)

### MCP (Model Context Protocol)
**Definição:** Protocolo que permite agentes de IA acessarem e interagirem com a documentação do sistema.

**Contexto:** Servidor MCP expõe recursos de documentação para clientes como Claude Desktop.

**Relacionado:** [MCP-DOCUMENTATION-GUIDE.md](../MCP-DOCUMENTATION-GUIDE.md)

### Supabase
**Definição:** Plataforma de backend-as-a-service usada como data warehouse para armazenar métricas.

**Contexto:** PostgreSQL gerenciado que centraliza dados de múltiplas fontes (Facebook, Google, etc.).

**Relacionado:** [Setup Supabase](../../analytics/docs/setup-supabase.md)

### Apache Superset
**Definição:** Plataforma de Business Intelligence para criação de dashboards e visualizações.

**Contexto:** Interface web para análise de dados armazenados no Supabase.

**Relacionado:** [Setup Superset](../../analytics/docs/setup-apache-superset.md)

### N8N
**Definição:** Plataforma de automação de workflows que conecta diferentes serviços e APIs.

**Contexto:** Orquestra coleta de dados, alertas e integrações entre sistemas.

**Relacionado:** [N8N-GUIDE.md](../api/integrations/N8N-GUIDE.md)

---

## 📊 Termos de Marketing

### CTR (Click-Through Rate)
**Definição:** Taxa de cliques, calculada como (cliques ÷ impressões) × 100.

**Contexto:** Métrica fundamental para medir relevância e performance de anúncios.

**Fórmula:** `CTR = (Clicks / Impressions) × 100`

### CPC (Cost Per Click)
**Definição:** Custo por clique, calculado como gasto total ÷ número de cliques.

**Contexto:** Indica eficiência de investimento em anúncios.

**Fórmula:** `CPC = Spend / Clicks`

### ROAS (Return on Ad Spend)
**Definição:** Retorno sobre investimento em anúncios, calculado como receita ÷ gasto.

**Contexto:** Métrica principal para avaliar lucratividade das campanhas.

**Fórmula:** `ROAS = Revenue / Ad Spend`

### CPA (Cost Per Acquisition)
**Definição:** Custo por aquisição, calculado como gasto total ÷ número de conversões.

**Contexto:** Indica eficiência em gerar conversões desejadas.

**Fórmula:** `CPA = Spend / Conversions`

### CPM (Cost Per Mille)
**Definição:** Custo por mil impressões, calculado como (gasto ÷ impressões) × 1000.

**Contexto:** Padrão da indústria para comparar custos de alcance.

**Fórmula:** `CPM = (Spend / Impressions) × 1000`

### Frequency
**Definição:** Frequência média de visualização de anúncios por usuário.

**Contexto:** Indica saturação do público-alvo e necessidade de refresh criativo.

**Fórmula:** `Frequency = Impressions / Reach`

### Reach
**Definição:** Número único de pessoas que viram o anúncio pelo menos uma vez.

**Contexto:** Mede alcance real da campanha, diferente de impressões.

### Impressions
**Definição:** Número total de vezes que o anúncio foi exibido.

**Contexto:** Inclui múltiplas visualizações pela mesma pessoa.

### Clicks
**Definição:** Número total de cliques nos anúncios.

**Contexto:** Interações diretas com o anúncio.

### Conversions
**Definição:** Ações desejadas completadas pelos usuários (compras, cadastros, etc.).

**Contexto:** Objetivo final das campanhas de marketing.

### Revenue
**Definição:** Receita gerada pelas conversões.

**Contexto:** Valor monetário das conversões para cálculo de ROAS.

---

## 🏗️ Termos de Arquitetura

### Monorepo
**Definição:** Estrutura de repositório que contém múltiplos projetos relacionados em um único repositório Git.

**Contexto:** Este projeto organiza backend, analytics, frontend e shared em um monorepo.

### Microservices
**Definição:** Arquitetura que divide aplicação em serviços independentes e comunicáveis.

**Contexto:** Agent API, Analytics e N8N funcionam como microservices distintos.

### API Gateway
**Definição:** Ponto único de entrada que roteia requisições para serviços apropriados.

**Contexto:** Agent API atua como gateway para funcionalidades de marketing.

### Data Pipeline
**Definição:** Fluxo automatizado de dados desde coleta até análise.

**Contexto:** Facebook API → Agent API → Supabase → Superset.

### ETL (Extract, Transform, Load)
**Definição:** Processo de extrair dados de fontes, transformar e carregar em destino.

**Contexto:** N8N workflows executam ETL de métricas do Facebook para Supabase.

### Data Warehouse
**Definição:** Repositório centralizado de dados históricos para análise.

**Contexto:** Supabase funciona como data warehouse para métricas de marketing.

### Business Intelligence (BI)
**Definição:** Processo de transformar dados em insights acionáveis para negócios.

**Contexto:** Superset fornece capacidades de BI sobre dados de marketing.

### Real-time Processing
**Definição:** Processamento de dados conforme são gerados, sem delay significativo.

**Contexto:** Métricas são coletadas e processadas em tempo real.

### Batch Processing
**Definição:** Processamento de dados em lotes em intervalos regulares.

**Contexto:** Relatórios diários são gerados via batch processing.

---

## 🔧 Termos de Desenvolvimento

### FastAPI
**Definição:** Framework web moderno e rápido para APIs em Python.

**Contexto:** Agent API é construído com FastAPI para alta performance.

### Pydantic
**Definição:** Biblioteca para validação de dados usando type hints do Python.

**Contexto:** Usado para validação de schemas de request/response na API.

### SQLAlchemy
**Definição:** ORM (Object-Relational Mapping) para Python.

**Contexto:** Usado para interação com banco de dados PostgreSQL.

### Celery
**Definição:** Sistema de filas de tarefas assíncronas para Python.

**Contexto:** Processa tarefas pesadas em background (coleta de métricas).

### Redis
**Definição:** Banco de dados em memória usado para cache e sessões.

**Contexto:** Acelera acesso a dados frequentes e gerencia sessões.

### Docker
**Definição:** Plataforma de containerização para aplicações.

**Contexto:** Todos os serviços rodam em containers Docker para isolamento.

### Docker Compose
**Definição:** Ferramenta para definir e executar aplicações multi-container.

**Contexto:** Orquestra todos os serviços do sistema (API, DB, Redis, etc.).

### CI/CD
**Definição:** Integração Contínua e Deploy Contínuo.

**Contexto:** GitHub Actions automatiza testes e deploy.

### Rate Limiting
**Definição:** Controle de taxa de requisições para prevenir abuso.

**Contexto:** API implementa rate limiting para proteger recursos.

### JWT (JSON Web Token)
**Definição:** Padrão para tokens de autenticação seguros.

**Contexto:** Usado para autenticação de usuários na API.

### OAuth
**Definição:** Protocolo de autorização para acesso a recursos.

**Contexto:** Usado para integração com APIs externas (Facebook, Google).

---

## 🔌 Termos de Integração

### Webhook
**Definição:** Mecanismo para notificar sistemas sobre eventos em tempo real.

**Contexto:** N8N usa webhooks para disparar workflows automaticamente.

### REST API
**Definição:** Arquitetura de API baseada em princípios REST.

**Contexto:** Agent API segue padrões REST para comunicação.

### GraphQL
**Definição:** Query language e runtime para APIs.

**Contexto:** Facebook Graph API usa GraphQL para consultas flexíveis.

### SDK (Software Development Kit)
**Definição:** Conjunto de ferramentas para desenvolvimento de software.

**Contexto:** Facebook Marketing API SDK para Python.

### API Key
**Definição:** Chave de identificação para acesso a APIs.

**Contexto:** Usado para autenticação com serviços externos.

### Bearer Token
**Definição:** Tipo de token de acesso usado em autenticação HTTP.

**Contexto:** Facebook API usa Bearer tokens para autenticação.

### CORS (Cross-Origin Resource Sharing)
**Definição:** Mecanismo de segurança para requisições cross-origin.

**Contexto:** Configurado na API para permitir acesso de frontend.

---

## 📊 Termos de Analytics

### KPI (Key Performance Indicator)
**Definição:** Métricas-chave para medir sucesso de objetivos.

**Contexto:** CTR, ROAS, CPA são KPIs principais de marketing.

### Cohort Analysis
**Definição:** Análise de comportamento de grupos de usuários ao longo do tempo.

**Contexto:** Usado para entender retenção e lifetime value.

### Attribution
**Definição:** Processo de atribuir conversões a touchpoints específicos.

**Contexto:** Facebook usa attribution para creditar conversões a anúncios.

### Funnel Analysis
**Definição:** Análise do funil de conversão desde awareness até purchase.

**Contexto:** Identifica gargalos no processo de conversão.

### A/B Testing
**Definição:** Método de comparar duas versões para determinar qual performa melhor.

**Contexto:** Testes de criativos, audiences e landing pages.

### Machine Learning
**Definição:** Algoritmos que aprendem padrões em dados para fazer previsões.

**Contexto:** Facebook usa ML para otimização automática de campanhas.

### Predictive Analytics
**Definição:** Uso de dados históricos para prever tendências futuras.

**Contexto:** Previsão de performance de campanhas baseada em dados históricos.

---

## 🚨 Termos de Segurança

### OWASP Top 10
**Definição:** Lista dos 10 riscos de segurança mais críticos em aplicações web.

**Contexto:** Sistema implementa proteções contra vulnerabilidades OWASP.

### SQL Injection
**Definição:** Ataque que injeta código SQL malicioso em queries.

**Contexto:** Prevenido usando SQLAlchemy ORM e prepared statements.

### XSS (Cross-Site Scripting)
**Definição:** Ataque que injeta scripts maliciosos em páginas web.

**Contexto:** Prevenido com sanitização de inputs e headers de segurança.

### CSRF (Cross-Site Request Forgery)
**Definição:** Ataque que força usuários a executar ações não intencionais.

**Contexto:** Prevenido com tokens CSRF e validação de origem.

### Rate Limiting
**Definição:** Controle de taxa de requisições para prevenir ataques.

**Contexto:** Implementado para proteger APIs contra abuso.

### Encryption
**Definição:** Processo de codificar dados para proteger informações sensíveis.

**Contexto:** Senhas são hasheadas e tokens são criptografados.

### Authentication
**Definição:** Processo de verificar identidade de usuários.

**Contexto:** Implementado via JWT tokens e OAuth.

### Authorization
**Definição:** Processo de determinar permissões de usuários autenticados.

**Contexto:** Controle de acesso baseado em roles e permissions.

---

## 🔗 Acrônimos e Siglas

| Sigla | Significado | Contexto |
|-------|-------------|----------|
| **API** | Application Programming Interface | Interface para comunicação entre sistemas |
| **BI** | Business Intelligence | Análise de dados para insights de negócio |
| **CTR** | Click-Through Rate | Taxa de cliques em anúncios |
| **CPC** | Cost Per Click | Custo por clique |
| **ROAS** | Return on Ad Spend | Retorno sobre investimento em anúncios |
| **CPA** | Cost Per Acquisition | Custo por aquisição |
| **CPM** | Cost Per Mille | Custo por mil impressões |
| **ETL** | Extract, Transform, Load | Processo de pipeline de dados |
| **JWT** | JSON Web Token | Padrão para tokens de autenticação |
| **OAuth** | Open Authorization | Protocolo de autorização |
| **REST** | Representational State Transfer | Arquitetura de APIs |
| **SDK** | Software Development Kit | Kit de desenvolvimento |
| **API** | Application Programming Interface | Interface de programação |
| **ML** | Machine Learning | Aprendizado de máquina |
| **AI** | Artificial Intelligence | Inteligência artificial |
| **KPI** | Key Performance Indicator | Indicador-chave de performance |
| **XSS** | Cross-Site Scripting | Ataque de script cross-site |
| **CSRF** | Cross-Site Request Forgery | Falsificação de requisição cross-site |
| **CORS** | Cross-Origin Resource Sharing | Compartilhamento de recursos cross-origin |
| **OWASP** | Open Web Application Security Project | Projeto de segurança de aplicações web |

---

## 📚 Referências Externas

### Documentação Oficial
- **Facebook Marketing API:** https://developers.facebook.com/docs/marketing-api
- **Supabase Docs:** https://supabase.com/docs
- **Apache Superset:** https://superset.apache.org/docs
- **N8N Docs:** https://docs.n8n.io
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Docker Docs:** https://docs.docker.com

### Padrões e Especificações
- **REST API Guidelines:** https://restfulapi.net
- **JWT Specification:** https://tools.ietf.org/html/rfc7519
- **OAuth 2.0:** https://oauth.net/2/
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/

### Comunidade
- **Stack Overflow:** https://stackoverflow.com
- **GitHub:** https://github.com
- **Reddit r/Marketing:** https://reddit.com/r/marketing
- **Facebook Developers Community:** https://developers.facebook.com/community

---

## ✅ Como Usar Este Glossário

### Para Desenvolvedores
1. **Consulte termos técnicos** antes de implementar funcionalidades
2. **Use acrônimos** para comunicação eficiente com a equipe
3. **Referencie documentação** relacionada para implementação

### Para Usuários de Negócio
1. **Entenda métricas de marketing** para interpretar relatórios
2. **Compreenda arquitetura** para entender capacidades do sistema
3. **Use termos corretos** em comunicações com equipe técnica

### Para Novos Membros
1. **Leia glossário completo** para familiarização com o projeto
2. **Consulte referências** para aprofundamento em tópicos específicos
3. **Contribua** adicionando novos termos conforme necessário

---

**💡 Dica:** Use Ctrl+F (Cmd+F no Mac) para buscar termos específicos neste glossário!
