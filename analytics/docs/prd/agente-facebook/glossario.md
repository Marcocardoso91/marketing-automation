# Glossário - Projeto Sabrina / Agente Facebook

**Versão:** 2.0.0  
**Data:** 18 de Outubro, 2025  
**Tipo:** Termos Técnicos Bilíngues (PT-BR / EN-US)

---

## A

### ABO (Ad Set Budget Optimization)
**PT:** Otimização de orçamento em nível de conjunto de anúncios  
**EN:** Ad Set Budget Optimization  
**Definição:** Método onde o orçamento é controlado manualmente para cada ad set, permitindo controle granular sobre distribuição de budget.  
**Uso no Projeto:** Utilizado nas Semanas 2-3 para testes A/B controlados antes de migrar para CBO.  
**Ref:** ADR-002, FEAT-010

### ADR (Architecture Decision Record)
**PT:** Registro de Decisão Arquitetural  
**EN:** Architecture Decision Record  
**Definição:** Documento que captura uma decisão técnica importante, incluindo contexto, alternativas, justificativa e consequências.  
**Uso no Projeto:** 9 ADRs documentados em `decisions.md`.  
**Ref:** decisions.md

### API (Application Programming Interface)
**PT:** Interface de Programação de Aplicações  
**EN:** Application Programming Interface  
**Definição:** Conjunto de endpoints e métodos que permitem comunicação entre sistemas.  
**APIs Utilizadas:** Meta Ads API v21.0, Notion API v2022-06-28  
**Ref:** PRD.pt-BR.md seção 5.1

---

## B

### Baseline (Linha de Base)
**PT:** Linha de Base  
**EN:** Baseline  
**Definição:** Estado inicial capturado em um momento específico para servir como referência para comparações futuras.  
**Uso no Projeto:** 16.130 seguidores em 11 Out 2025.  
**Ref:** inventory.json, RF-008

### Budget (Orçamento)
**PT:** Orçamento  
**EN:** Budget  
**Definição:** Valor monetário alocado para campanhas de anúncios.  
**Uso no Projeto:** R$ 1.120 total (28 dias), R$ 40/dia (Semana 2).  
**Ref:** inventory.json metrics.targets

---

## C

### CBO (Campaign Budget Optimization)
**PT:** Otimização de Orçamento da Campanha  
**EN:** Campaign Budget Optimization  
**Definição:** Método onde o Meta Ads distribui automaticamente o orçamento entre ad sets com base em performance.  
**Uso no Projeto:** Planejado para Semana 4 após identificar ad sets vencedores.  
**Ref:** FEAT-010, ADR-002

### CPC (Cost Per Click)
**PT:** Custo Por Clique  
**EN:** Cost Per Click  
**Definição:** Valor médio pago por cada clique em anúncio.  
**Meta Projeto:** ≤ R$ 0,50  
**Atual:** Variável por AD (melhor: R$ 0,27 no AD 02)  
**Ref:** PRD.pt-BR.md seção 10.1

### CPE (Cost Per Engagement)
**PT:** Custo Por Engajamento  
**EN:** Cost Per Engagement  
**Definição:** Valor médio pago por cada engajamento (like, comment, save, share).  
**Meta Projeto:** ≤ R$ 0,70  
**Atual:** R$ 0,003 (excelente)  
**Ref:** inventory.json metrics.current_state

### CPM (Cost Per Mille / Cost Per Thousand Impressions)
**PT:** Custo Por Mil Impressões  
**EN:** Cost Per Thousand Impressions  
**Definição:** Valor pago para alcançar 1.000 impressões.  
**Atual:** R$ 2,03 (ótimo para Brasil)  
**Ref:** DADOS-EXTRAIDOS-IMAGENS.md

### Creative Fatigue (Fadiga Criativa)
**PT:** Fadiga Criativa  
**EN:** Creative Fatigue  
**Definição:** Fenômeno onde criativos perdem eficácia após exposição repetida à mesma audiência.  
**Indicador:** Queda de 15%+ no CTR ou aumento de 20%+ no CPE.  
**Mitigação:** Rotação criativa a cada 7-10 dias (FEAT-006).  
**Ref:** Análise do Plano, FEAT-006

### CTR (Click-Through Rate)
**PT:** Taxa de Cliques  
**EN:** Click-Through Rate  
**Definição:** Percentual de pessoas que clicaram após ver o anúncio.  
**Fórmula:** (Cliques / Impressões) × 100  
**Meta Projeto:** ≥ 1,5%  
**Atual:** 0,42% (em otimização)  
**Ref:** PRD.pt-BR.md seção 10.1

---

## D

### DM (Direct Message)
**PT:** Mensagem Direta  
**EN:** Direct Message  
**Definição:** Mensagens privadas no Instagram entre perfis.  
**Uso no Projeto:** Estratégia de engajamento via DM automation (FEAT-007).  
**Ref:** Análise do Plano, FEAT-007

### Docker
**PT:** Docker  
**EN:** Docker  
**Definição:** Plataforma de containerização que empacota aplicações e dependências em containers isolados.  
**Uso no Projeto:** Deploy do n8n via Docker Compose.  
**Ref:** ADR-004, inventory.json dependencies.platforms

---

## E

### Engagement Rate (Taxa de Engajamento)
**PT:** Taxa de Engajamento  
**EN:** Engagement Rate  
**Definição:** Percentual de interações (likes, comments, saves, shares) em relação ao alcance ou seguidores.  
**Fórmula:** (Interações / Alcance) × 100  
**Meta Indústria Beleza:** 1,5-2,4%  
**Ref:** PRD.pt-BR.md seção 10.2

---

## F

### Frequency (Frequência)
**PT:** Frequência  
**EN:** Frequency  
**Definição:** Número médio de vezes que cada pessoa viu o anúncio.  
**Fórmula:** Impressões / Alcance  
**Meta Projeto:** ≤ 2,5 (evitar ad fatigue)  
**Atual:** 1,00 (ideal)  
**Ref:** inventory.json metrics.current_state

### Frequency Cap (Limite de Frequência)
**PT:** Limite de Frequência  
**EN:** Frequency Cap  
**Definição:** Configuração que limita quantas vezes uma pessoa vê o mesmo anúncio em um período.  
**Uso no Projeto:** 2 impressões a cada 7 dias (FEAT-002).  
**Ref:** Análise do Plano, FEAT-002

---

## H

### Hook (Gancho)
**PT:** Gancho  
**EN:** Hook  
**Definição:** Primeiros 1-3 segundos de um vídeo/anúncio que capturam atenção.  
**Importância:** Fator #1 do algoritmo Instagram 2025.  
**Uso no Projeto:** Testes A/B de hooks nos Reels (FEAT-004).  
**Ref:** Análise do Plano, FEAT-004

---

## I

### Insights
**PT:** Insights / Métricas  
**EN:** Insights  
**Definição:** Dados analíticos sobre performance de perfil ou anúncios.  
**Fontes:** Instagram Insights (perfil), Meta Ads Manager (anúncios).  
**Ref:** RF-004, docs/screenshots-guide.md

### Inventory (Inventário)
**PT:** Inventário  
**EN:** Inventory  
**Definição:** Arquivo JSON centralizando mapeamento de arquivos, dependências, requisitos e métricas do projeto.  
**Arquivo:** `inventory.json`  
**Ref:** ADR-007, planner-001

---

## K

### KPI (Key Performance Indicator)
**PT:** Indicador-Chave de Performance  
**EN:** Key Performance Indicator  
**Definição:** Métrica crítica que mede sucesso em relação a objetivos.  
**KPIs Primários:** Novos Seguidores, Custo/Seguidor, CTR, Frequência, CPE, ROI.  
**Ref:** PRD.pt-BR.md seção 10.1

---

## L

### Lookalike Audience (Público Semelhante)
**PT:** Público Semelhante  
**EN:** Lookalike Audience  
**Definição:** Audiência criada pelo Meta Ads com características similares a uma source audience.  
**Tamanhos:** 1% (mais similar), 3% (balanceado), 5% (maior alcance).  
**Uso no Projeto:** Planejado para Semana 4 (FEAT-009).  
**Ref:** Análise do Plano, FEAT-009

---

## M

### Meta Ads API
**PT:** API do Meta Ads  
**EN:** Meta Ads API  
**Definição:** Interface programática para acessar dados de campanhas Facebook/Instagram.  
**Versão:** v21.0  
**Endpoint:** `https://graph.facebook.com/v21.0`  
**Ref:** inventory.json dependencies.apis

### MCP (Model Context Protocol)
**PT:** Protocolo de Contexto de Modelo  
**EN:** Model Context Protocol  
**Definição:** Servidores especializados para tarefas específicas (Notion, n8n, pesquisa, etc.).  
**MCPs Utilizados:** Notion MCP, n8n MCP, Exa Search, Context7, Sequential Thinking.  
**Ref:** inventory.json dependencies.tools

---

## N

### n8n
**PT:** n8n  
**EN:** n8n  
**Definição:** Plataforma open-source de automação de workflows com interface visual.  
**URL:** https://fluxos.macspark.dev  
**Uso:** Orquestração principal Meta Ads → Notion.  
**Ref:** ADR-001, RF-001

### Nicho (Niche)
**PT:** Nicho  
**EN:** Niche  
**Definição:** Segmento específico de mercado ou audiência.  
**Contexto Projeto:** Mudança de nicho em andamento (ADR-008), resultando em -5 seguidores líquidos (esperado).  
**Ref:** ADR-008, ADR-009

### Notion
**PT:** Notion  
**EN:** Notion  
**Definição:** Plataforma all-in-one de produtividade com databases relacionais e API robusta.  
**Uso:** Database principal + interface de gestão.  
**Ref:** ADR-002, RF-002

---

## O

### OAuth2
**PT:** OAuth 2.0  
**EN:** OAuth 2.0  
**Definição:** Protocolo de autorização para acesso seguro a APIs via tokens.  
**Uso:** Autenticação no Meta Ads API.  
**Ref:** inventory.json dependencies.apis

---

## P

### Portainer
**PT:** Portainer  
**EN:** Portainer  
**Definição:** Interface web para gerenciar containers Docker.  
**Uso:** Monitoramento do n8n no VPS.  
**Ref:** ADR-004, RNF-004

### PRD (Product Requirements Document)
**PT:** Documento de Requisitos do Produto  
**EN:** Product Requirements Document  
**Definição:** Documento formal especificando objetivos, requisitos, arquitetura e critérios de sucesso.  
**Arquivos:** `PRD.pt-BR.md`, `PRD.en-US.md`  
**Ref:** ADR-006

---

## R

### Rate Limit (Limite de Taxa)
**PT:** Limite de Taxa  
**EN:** Rate Limit  
**Definição:** Número máximo de requisições permitidas por período em uma API.  
**Meta Ads API:** 200 calls/hour  
**Notion API:** 3 requests/second  
**Ref:** inventory.json dependencies.apis

### Reach (Alcance)
**PT:** Alcance  
**EN:** Reach  
**Definição:** Número de pessoas únicas que viram o conteúdo.  
**Atual:** 41.251 pessoas (Meta Ads, 1-18 Out)  
**Ref:** inventory.json metrics.current_state

### Reel
**PT:** Reel  
**EN:** Reel  
**Definição:** Formato de vídeo curto vertical do Instagram (até 90 segundos).  
**Performance:** 20,5-22,9% das visualizações (potencial de crescimento).  
**Ref:** ADR-009, plano-crescimento-sabrina

### RF (Requisito Funcional)
**PT:** Requisito Funcional  
**EN:** Functional Requirement  
**Definição:** Especificação de uma funcionalidade que o sistema deve realizar.  
**Total:** 10 RFs (RF-001 a RF-010).  
**Ref:** PRD.pt-BR.md seção 3.1

### RNF (Requisito Não-Funcional)
**PT:** Requisito Não-Funcional  
**EN:** Non-Functional Requirement  
**Definição:** Especificação de qualidade, performance ou restrição do sistema.  
**Total:** 7 RNFs (RNF-001 a RNF-007).  
**Ref:** PRD.pt-BR.md seção 3.2

### ROI (Return on Investment)
**PT:** Retorno sobre Investimento  
**EN:** Return on Investment  
**Definição:** Razão entre lucro/valor gerado e investimento realizado.  
**Fórmula:** (Valor Gerado - Custo) / Custo  
**Meta Projeto:** 2,5-3,5x  
**Ref:** inventory.json metrics.targets

---

## S

### Scaling (Escalonamento)
**PT:** Escalonamento  
**EN:** Scaling  
**Definição:** Processo de aumentar budget ou audiência mantendo ou melhorando performance.  
**Protocolo Seguro:** Aumentar budget em 20% a cada 3-4 dias (FEAT-008).  
**Ref:** Análise do Plano, FEAT-008

### Seguidores (Followers)
**PT:** Seguidores  
**EN:** Followers  
**Definição:** Contas que seguem um perfil no Instagram.  
**Baseline:** 16.130 (11 Out 2025)  
**Meta:** +900 a 1.300 novos em 28 dias  
**Ref:** inventory.json metrics

### Stories
**PT:** Stories  
**EN:** Stories  
**Definição:** Formato de conteúdo efêmero (24h) no Instagram.  
**Performance:** 76,5-79% das visualizações (formato dominante).  
**Ref:** ADR-009, plano-crescimento-sabrina

---

## T

### Token
**PT:** Token  
**EN:** Token  
**Definição:** Chave de autenticação para acessar APIs.  
**Tipos Utilizados:** Meta Ads Access Token, Notion Integration Token, n8n API Key.  
**Segurança:** Armazenados em `.env` (nunca em código) - ADR-005.  
**Ref:** RNF-001, ADR-005

### Traceability (Rastreabilidade)
**PT:** Rastreabilidade  
**EN:** Traceability  
**Definição:** Capacidade de rastrear cada requisito até sua implementação e fontes.  
**Implementação:** inventory.json + coerencia.md.  
**Ref:** ADR-007, RNF-007

---

## U

### UGC (User-Generated Content)
**PT:** Conteúdo Gerado pelo Usuário  
**EN:** User-Generated Content  
**Definição:** Conteúdo criado por clientes/seguidores (depoimentos, fotos, vídeos).  
**Conversão:** +67% vs conteúdo de marca.  
**Ref:** Análise do Plano de Crescimento

### Uptime
**PT:** Tempo de Atividade  
**EN:** Uptime  
**Definição:** Percentual de tempo que um sistema está operacional.  
**Meta:** 99%+ para automação n8n.  
**Ref:** RNF-004

---

## V

### VPS (Virtual Private Server)
**PT:** Servidor Privado Virtual  
**EN:** Virtual Private Server  
**Definição:** Servidor virtualizado hospedando aplicações.  
**Uso:** Hospedagem do n8n via Docker.  
**Ref:** ADR-004, inventory.json architecture

---

## W

### Workflow
**PT:** Fluxo de Trabalho  
**EN:** Workflow  
**Definição:** Sequência automatizada de tarefas conectadas.  
**Principal:** `n8n-workflows/meta-ads-notion.json`  
**Execução:** Diária às 9h (Schedule Trigger).  
**Ref:** RF-001, ADR-001

---

## Total de Termos: 45+

---

**Documento mantido pelo Agente Orquestrador**  
**Última atualização:** 18 de Outubro, 2025 - 23:58 BRT  
**Próxima revisão:** A cada nova funcionalidade ou decisão técnica
