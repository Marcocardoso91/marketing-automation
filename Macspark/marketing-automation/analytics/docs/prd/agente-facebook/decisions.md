# Decisões Arquiteturais (ADRs) - Projeto Sabrina

**Projeto:** Agente Facebook / Projeto Sabrina  
**Versão:** 2.0.0  
**Data:** 18 de Outubro, 2025

---

## Sumário

Este documento registra todas as **Decisões Arquiteturais (Architecture Decision Records - ADRs)** tomadas durante o desenvolvimento e evolução do Projeto Sabrina. Cada decisão é documentada com contexto, justificativa, alternativas consideradas, consequências e status atual.

---

## ADR-001: Escolha do n8n como Orquestrador de Workflows

**Data:** 2025-10-11  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de automação visual, versionável e self-hosted para orquestrar coleta de métricas do Meta Ads e persistência no Notion.

### Alternativas Consideradas
1. **Zapier** - Plataforma no-code líder de mercado
2. **Make (Integromat)** - Alternativa ao Zapier com mais flexibilidade
3. **n8n** - Open-source, self-hosted, workflow visual
4. **Airflow** - Python-based, mais complexo, focado em data pipelines

### Decisão
Escolhemos **n8n** como orquestrador principal.

### Justificativa
- ✅ **Gratuito e open-source** → Zero custo recorrente
- ✅ **Self-hosted** → Controle total sobre dados e infraestrutura
- ✅ **Interface visual** → Fácil debugging e manutenção
- ✅ **Versionável** → Workflows exportáveis em JSON
- ✅ **Já hospedado** → Instância existente em https://fluxos.macspark.dev
- ✅ **Integrações nativas** → Meta Ads API + Notion API built-in
- ✅ **Comunidade ativa** → Templates e suporte disponíveis

### Consequências
**Positivas:**
- Sem custos de plataforma (vs R$ 100-300/mês do Zapier/Make)
- Controle total sobre execuções e logs
- Possibilidade de customização ilimitada

**Negativas:**
- Requer manutenção própria (atualizações, monitoramento)
- Depende da disponibilidade do VPS
- Curva de aprendizado inicial para editar workflows

**Mitigação:**
- Monitoramento via Portainer + alertas
- Backup diário via snapshots Docker
- Script Python como fallback manual

---

## ADR-002: Notion como Database Principal

**Data:** 2025-10-11  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de interface amigável + database estruturado + visualizações flexíveis para gestão de métricas e conteúdo.

### Alternativas Consideradas
1. **Airtable** - Database visual com API robusta
2. **Google Sheets** - Simplicidade máxima com integrações via Apps Script
3. **Notion** - Interface superior com databases relacionais
4. **PostgreSQL** - Database tradicional com mais controle

### Decisão
Escolhemos **Notion** como database principal e interface de gestão.

### Justificativa
- ✅ **Interface superior** → UX incomparável para visualização de dados
- ✅ **Databases relacionais** → 4 databases interligados (Calendário, Métricas, Campanhas, Ideias)
- ✅ **Visualizações múltiplas** → Table, Calendar, Board, Gallery
- ✅ **API robusta** → v2022-06-28 com endpoints completos
- ✅ **Já utilizado** → Sabrina já familiarizada com Notion
- ✅ **Colaboração nativa** → Compartilhamento e comentários built-in
- ✅ **Versionamento** → Histórico de alterações automático

### Consequências
**Positivas:**
- Interface amigável sem necessidade de treinamento
- Visualizações ricas (dashboards, calendários, kanban)
- Centralização de docs + dados + estratégia

**Negativas:**
- Rate limit de 3 requests/second (aceitável para caso de uso)
- Não é um database tradicional (sem SQL direto)
- Vendor lock-in moderado (migração trabalhosa)

**Mitigação:**
- Throttling no n8n para respeitar rate limits
- Export semanal automático para backup
- Dados críticos também em inventory.json

---

## ADR-003: Python como Fallback Manual

**Data:** 2025-10-12  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de backup caso n8n falhe ou esteja indisponível.

### Alternativas Consideradas
1. **Apenas n8n** - Sem fallback, depender 100% da automação
2. **Script Bash + curl** - Mais leve, mas menos robusto
3. **Script Python** - Legível, com bibliotecas maduras (requests, dotenv)
4. **Node.js Script** - Consistência com n8n, mas mais complexo

### Decisão
Criar **script Python independente** (`scripts/meta-to-notion.py`) com mesma lógica do workflow n8n.

### Justificativa
- ✅ **Execução manual rápida** → `python3 meta-to-notion.py` em 10 segundos
- ✅ **Sem dependências de plataforma** → Roda em qualquer máquina
- ✅ **Legibilidade** → Fácil de entender e modificar
- ✅ **Bibliotecas maduras** → requests, python-dotenv, datetime
- ✅ **Mesma lógica** → Garante consistência de dados

### Consequências
**Positivas:**
- Continuidade garantida mesmo se n8n cair
- Útil para testes e debugging
- Documentação viva da lógica de negócio

**Negativas:**
- Código duplicado (Python + n8n nodes)
- Requer manutenção sincronizada
- Dependência de Python 3.x instalado

**Mitigação:**
- Testar script Python mensalmente
- Documentar diferenças explicitamente
- Considerar script como "source of truth" para lógica

---

## ADR-004: Docker para Deploy e Isolamento

**Data:** 2025-10-11  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de ambiente replicável, versionado e com rollback fácil.

### Alternativas Consideradas
1. **Instalação nativa** - Direto no sistema operacional do VPS
2. **Docker Compose** - Containerização com orquestração simples
3. **Kubernetes** - Orquestração avançada, mas overhead alto
4. **Systemd services** - Gestão via systemd units

### Decisão
Usar **Docker Compose** para deploy do n8n e futuros serviços.

### Justificativa
- ✅ **Isolamento** → n8n não interfere com outros serviços do VPS
- ✅ **Portabilidade** → Imagem Docker pode ser movida entre servidores
- ✅ **Rollback rápido** → Via snapshots de imagens/volumes
- ✅ **Versionamento** → docker-compose.yml versionado em git
- ✅ **Monitoramento** → Integração nativa com Portainer
- ✅ **Recursos gerenciáveis** → Limites de CPU/RAM definidos

### Consequências
**Positivas:**
- Ambiente replicável em minutos
- Rollback em segundos via `docker run` de snapshot
- Isolamento de dependências

**Negativas:**
- Overhead mínimo de recursos (~50-100MB RAM extra)
- Requer conhecimento básico de Docker
- Volumes precisam de backup separado

**Mitigação:**
- Overhead é aceitável para VPS moderno
- Documentação completa em `docs/setup-n8n-meta-ads.md`
- Cron job para backup diário de volumes

---

## ADR-005: Segurança de Tokens via .env (Não em Código)

**Data:** 2025-10-11  
**Status:** ✅ Aceito e Implementado  
**Prioridade:** 🔴 Crítico  
**Contexto:** Tokens sensíveis (Meta Ads, Notion, n8n) nunca devem ser expostos em repositórios públicos ou código versionado.

### Alternativas Consideradas
1. **Hardcoded no código** - ❌ Péssima prática, inseguro
2. **Arquivo .env** - ✅ Padrão indústria, gitignored
3. **Docker Secrets** - Mais seguro, mas mais complexo
4. **HashiCorp Vault** - Enterprise-grade, overhead alto

### Decisão
Usar **arquivo .env** local (gitignored) + `env.example.txt` versionado.

### Justificativa
- ✅ **Padrão indústria** → Adotado por 99% dos projetos
- ✅ **Simples de usar** → `python-dotenv` carrega automaticamente
- ✅ **Gitignored** → `.env` nunca é commitado
- ✅ **Template versionado** → `env.example.txt` mostra estrutura
- ✅ **Compatibilidade** → n8n, Python, Docker Compose suportam

### Consequências
**Positivas:**
- Tokens protegidos de exposição acidental
- Fácil rotação de tokens
- Cada ambiente (dev/prod) tem seu .env

**Negativas:**
- Arquivo .env deve ser transferido manualmente
- Risco de perda se não houver backup
- Não é tão seguro quanto Vault/Secrets Manager

**Mitigação:**
- Backup criptografado do .env em local seguro
- Instruções claras em `env.example.txt`
- Documentar processo de rotação de tokens

---

## ADR-006: Bilinguismo Documental (PT-BR + EN-US)

**Data:** 2025-10-18  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de documentação acessível para stakeholders brasileiros E comunidade internacional (potencial open-source futuro).

### Alternativas Consideradas
1. **Apenas PT-BR** - Foco no público atual
2. **Apenas EN-US** - Padrão internacional
3. **PT-BR + EN-US** - Bilíngue completo
4. **PT-BR + i18n** - Múltiplos idiomas via framework

### Decisão
Manter **dois PRDs completos**: `PRD.pt-BR.md` + `PRD.en-US.md`.

### Justificativa
- ✅ **Acessibilidade local** → Sabrina e equipe falam PT-BR
- ✅ **Potencial open-source** → EN-US facilita contribuições futuras
- ✅ **Profissionalismo** → Demonstra rigor documental
- ✅ **Rastreabilidade** → Ambos versões com mesma estrutura

### Consequências
**Positivas:**
- Documentação acessível para todos stakeholders
- Facilita futura abertura do código
- Melhora qualidade via revisão em dois idiomas

**Negativas:**
- Manutenção duplicada (mudanças devem ser feitas em ambos)
- Risco de dessincronia entre versões
- Tempo de geração 50% maior

**Mitigação:**
- Agente Orquestrador gera ambos automaticamente
- Diff check antes de cada release
- Versioning sincronizado (ambos sempre 2.0.0)

---

## ADR-007: Rastreabilidade entre Requisitos e Código

**Data:** 2025-10-18  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de auditar origem de cada decisão e validar implementação contra requisitos.

### Alternativas Consideradas
1. **Sem rastreabilidade** - Documentação independente do código
2. **Comentários inline** - Links nos arquivos de código
3. **Inventory.json** - Mapeamento central de dependências
4. **Jira/Trello** - Plataforma externa de tracking

### Decisão
Criar **`inventory.json`** centralizado + **coerencia.md** com matriz de rastreabilidade.

### Justificativa
- ✅ **Single source of truth** → Tudo em um arquivo JSON versionado
- ✅ **Auditável** → Cada RF/RNF linkado a arquivo específico
- ✅ **Programático** → Pode ser processado por scripts
- ✅ **Versionado** → Histórico de mudanças via git
- ✅ **Independente** → Não depende de plataforma externa

### Consequências
**Positivas:**
- Rastreabilidade completa do PRD ao código
- Auditorias automáticas via scripts
- Base para geração de relatórios

**Negativas:**
- Requer atualização manual a cada mudança
- Risco de ficar desatualizado
- JSON pode ficar grande e complexo

**Mitigação:**
- Agente Orquestrador atualiza automaticamente
- Validação via Evaluator (Fase 3)
- Estrutura modular e bem documentada

---

## ADR-008: Mudança de Nicho no Instagram

**Data:** 2025-10-11  
**Status:** ✅ Aceito e em Execução  
**Contexto:** Instagram da Sabrina está em transição de nicho, o que causa perda temporária de seguidores.

### Alternativas Consideradas
1. **Manter nicho antigo** - Seguidores estáveis, mas não alinhados
2. **Mudança abrupta** - Transição rápida, perda alta
3. **Mudança gradual** - Transição suave, perda controlada ✅
4. **Criar novo perfil** - Começar do zero (descartado)

### Decisão
Realizar **mudança gradual de nicho** focando em conteúdo 100% novo nicho, aceitando perda temporária de seguidores.

### Justificativa
- ✅ **Seguidores qualificados** → Novos seguidores do nicho correto são mais valiosos
- ✅ **Perda mínima** → -5 seguidores líquidos (perdeu 14, ganhou 9) é aceitável
- ✅ **Crescimento org ânico mantido** → +58,5% de alcance demonstra força do conteúdo
- ✅ **Autenticidade** → Alinhamento com propósito real

### Consequências
**Positivas:**
- Seguidores novos altamente engajados
- Crescimento sustentável de longo prazo
- Autenticidade e conexão genuína com audiência

**Negativas:**
- Perda temporária de seguidores (esperado)
- Métricas de crescimento inicialmente menores
- Necessidade de paciência durante transição

**Mitigação:**
- Foco em qualidade vs quantidade
- Monitorar engagement rate (não apenas follower count)
- Stories diárias para manter comunidade engajada

---

## ADR-009: Correção de Dados do Instagram (18 Out)

**Data:** 2025-10-18  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Identificada divergência nos dados - Instagram sendo trabalhado tem 16.130 seguidores (não 1.142).

### Problema Identificado
- Sabrina tem **dois Instagrams**
- Dados iniciais misturaram screenshots de perfis diferentes
- Instagram correto: **16.130 seguidores** (baseline 11 Out: 16.129)
- Instagram incorreto: 1.142 seguidores (não é o que estamos trabalhando)

### Decisão
**Corrigir imediatamente** todos os dados no Notion e documentação para refletir Instagram real.

### Ações Tomadas
1. ✅ Criar páginas de correção no Notion:
   - "📊 CORREÇÃO - Dados Reais Instagram (11/10/2025)"
   - "📊 Linha de Base CORRIGIDA - Instagram Real"
   - "🎯 Estratégia CORRIGIDA - Mudança de Nicho"
2. ✅ Atualizar inventory.json com métricas corretas
3. ✅ Atualizar PRDs (PT-BR + EN-US) com dados reais
4. ✅ Documentar correção em ADR

### Consequências
**Positivas:**
- Dados corretos refletem realidade
- Estratégia ajustada para contexto real (mudança de nicho)
- Rastreabilidade da correção

**Negativas:**
- Tempo gasto em correção
- Documentos anteriores com dados incorretos (marcados como obsoletos)

**Aprendizado:**
- ✅ Sempre validar qual Instagram está sendo trabalhado
- ✅ Screenshots devem incluir handle (@username) para identificação
- ✅ Confirmar dados críticos com stakeholder antes de processar

---

---

## ADR-010: Supabase como Data Warehouse Central

**Data:** 2025-10-18  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de data warehouse escalável e gratuito para armazenar métricas de múltiplas fontes (Meta Ads, Google Analytics, Google Ads, YouTube).

### Alternativas Consideradas
1. **Apenas Notion** - Simples, mas não escala para SQL avançado
2. **BigQuery** - Poderoso, mas pago após free tier
3. **Supabase** - PostgreSQL gratuito com API REST ← ESCOLHIDO
4. **PostgreSQL Local** - Gratuito, mas requer manutenção

### Decisão
Utilizar **Supabase** (PostgreSQL cloud) como data warehouse central.

### Justificativa
- ✅ **Free tier generoso** → 500MB database, 2GB bandwidth/mês
- ✅ **PostgreSQL completo** → Queries SQL avançadas, views, índices
- ✅ **API REST automática** → Supabase gera endpoints CRUD automaticamente
- ✅ **Integração nativa n8n** → HTTP Request node funciona perfeitamente
- ✅ **Dashboard embutido** → SQL Editor para queries manuais
- ✅ **Real-time** → Opcional para features futuras
- ✅ **Validado por Context7** → Trust Score 10, 24.046 code snippets

### Consequências
**Positivas:**
- Queries SQL complexas (JOINs, agregações, window functions)
- Visualização via Apache Superset
- Escalável para milhões de registros
- Backup automático

**Negativas:**
- Dependência de serviço cloud (Supabase)
- Limite de 500MB (suficiente para anos de métricas)
- Mais complexo que Notion

**Mitigação:**
- Export semanal para backup local
- Monitorar uso de espaço
- Documentação completa em `docs/setup-supabase.md`

---

## ADR-011: Arquitetura Modular de Workflows

**Data:** 2025-10-18  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Decisão entre workflow monolítico (tudo em 1) vs modular (workflows separados por fonte).

### Alternativas Consideradas
1. **Workflow Monolítico** - Tudo em 1 arquivo, mais simples
2. **Arquitetura Modular** - Workflows separados por fonte ← ESCOLHIDO
3. **Sub-workflows** - Workflow pai chamando sub-workflows

### Decisão
Criar **5 workflows n8n separados** (1 por fonte + 1 consolidador).

### Justificativa
- ✅ **Debugging isolado** → Problema em Google Ads não afeta Meta Ads
- ✅ **Manutenção facilitada** → Modificar 1 fonte sem risco de quebrar outras
- ✅ **Escalabilidade** → Adicionar nova fonte = novo workflow
- ✅ **Performance** → Execuções paralelas (9h, 9:15h, 9:30h, 9:45h)
- ✅ **Validado por Exa Search** → Medium 2025 "Scalable Automation Project"
- ✅ **Best practice** → Hostinger 2025 "n8n best practices"

### Consequências
**Positivas:**
- Falha em 1 workflow não afeta sistema completo
- Logs separados facilitam troubleshooting
- Pode ativar/desativar fontes individualmente

**Negativas:**
- Mais arquivos para gerenciar (5 vs 1)
- Configuração inicial mais trabalhosa

**Mitigação:**
- Documentação clara de cada workflow
- Templates reutilizáveis (Supabase insert é idêntico)
- Workflow consolidador unifica tudo

---

## ADR-012: Apache Superset para Visualização

**Data:** 2025-10-18  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de dashboards avançados para visualizar métricas de múltiplas fontes.

### Alternativas Consideradas
1. **Apenas Notion** - Simples, mas limitado em visualizações
2. **Metabase** - Open-source, mais simples que Superset
3. **Apache Superset** - Mais completo, padrão indústria ← ESCOLHIDO
4. **Grafana** - Focado em time-series, menos adequado para marketing
5. **Tableau/Power BI** - Pagos (R$ 70-200/mês)

### Decisão
Utilizar **Apache Superset** (self-hosted via Docker).

### Justificativa
- ✅ **100% Gratuito** → Open-source, self-hosted
- ✅ **40+ chart types** → Linha, barra, pizza, heatmap, gauge, etc
- ✅ **SQL Lab** → Queries customizadas ilimitadas
- ✅ **Performance** → Superior a Metabase em datasets grandes
- ✅ **Comunidade** → Mantido por Apache Foundation
- ✅ **Validado por Exa Search** → Preset.io 2025 "Leader in Open-Source BI"

### Consequências
**Positivas:**
- Dashboards profissionais sem custo
- Queries SQL avançadas
- Múltiplas fontes de dados
- Export para PDF/PNG

**Negativas:**
- Requer Docker (overhead ~300MB RAM)
- Curva de aprendizado média
- Manutenção própria (updates)

**Mitigação:**
- Docker Compose simplifica deploy
- Documentação em `docs/setup-apache-superset.md`
- Monitoramento via Portainer
- Updates opcionais (não críticos)

---

## ADR-013: OpenAI para Insights Automatizados

**Data:** 2025-10-18  
**Status:** ✅ Aceito e Implementado  
**Contexto:** Necessidade de análise inteligente automatizada das métricas consolidadas.

### Alternativas Consideradas
1. **Análise Manual** - Sabrina analisa dados manualmente
2. **Regras IF/THEN** - Alertas baseados em thresholds fixos
3. **OpenAI GPT-4o-mini** - IA generativa para insights ← ESCOLHIDO
4. **Claude** - Alternativa, mas pago
5. **Gemini** - Gratuito, mas menos preciso em PT-BR

### Decisão
Utilizar **OpenAI GPT-4o-mini** para gerar insights diários em PT-BR.

### Justificativa
- ✅ **Free tier** → 500 requests/mês (suficiente para diário)
- ✅ **Qualidade superior** → Análises contextuais e acionáveis
- ✅ **PT-BR nativo** → Respostas em português fluente
- ✅ **JSON mode** → Dados estruturados quando necessário
- ✅ **Integração n8n** → Node LangChain ou HTTP Request
- ✅ **Validado por n8n MCP** → nodes-langchain.lmChatOpenAi oficial

### Consequências
**Positivas:**
- Insights automatizados sem intervenção humana
- Detecção de padrões não óbvios
- Recomendações acionáveis personalizadas
- Economiza 1-2h/dia de análise manual

**Negativas:**
- Dependência de API externa (OpenAI)
- Free tier limitado (500 calls/mês)
- Custo se exceder tier ($0.15/1M tokens input, $0.60/1M tokens output)

**Mitigação:**
- Implementar cache de insights (evitar chamadas repetidas)
- Reduzir para análise semanal se exceder tier
- Monitorar usage no dashboard OpenAI
- Alternativa: usar prompts mais curtos ou gpt-3.5-turbo

---

## Sumário de Decisões Ativas

| ADR | Título | Status | Impacto |
|-----|--------|--------|---------|
| ADR-001 | n8n como Orquestrador | ✅ Ativo | Alto |
| ADR-002 | Notion como Database | ✅ Ativo | Alto |
| ADR-003 | Python como Fallback | ✅ Ativo | Médio |
| ADR-004 | Docker para Deploy | ✅ Ativo | Alto |
| ADR-005 | Segurança de Tokens | ✅ Ativo | Crítico |
| ADR-006 | Bilinguismo Documental | ✅ Ativo | Médio |
| ADR-007 | Rastreabilidade | ✅ Ativo | Alto |
| ADR-008 | Mudança de Nicho | ✅ Em Execução | Alto |
| ADR-009 | Correção Dados Instagram | ✅ Resolvido | Alto |
| **ADR-010** | **Supabase Data Warehouse** | ✅ Ativo | **Crítico** |
| **ADR-011** | **Arquitetura Modular** | ✅ Ativo | **Alto** |
| **ADR-012** | **Apache Superset Visualization** | ✅ Ativo | **Alto** |
| **ADR-013** | **OpenAI Insights** | ✅ Ativo | **Médio** |

**Total ADRs:** 13 decisões documentadas

---

## Decisões Futuras (Em Avaliação)

### DEC-FUTURE-001: Integração com WhatsApp Business API
**Contexto:** Potencial de engajamento via WhatsApp para novos seguidores.  
**Status:** 📅 Em avaliação para Fase 5  
**Complexidade:** Alta  
**Benefício Esperado:** Aumento de 20-30% em retenção

### DEC-FUTURE-002: Machine Learning para Previsão de Performance
**Contexto:** Uso de dados históricos para prever performance de criativos.  
**Status:** 📅 Em avaliação para Fase 6  
**Complexidade:** Muito Alta  
**Benefício Esperado:** Redução de 40% em criativos de baixa performance

### DEC-FUTURE-003: Open-sourcing do Projeto
**Contexto:** Compartilhar framework com comunidade Instagram/Meta Ads.  
**Status:** 📅 Em avaliação para pós-ciclo 28 dias  
**Complexidade:** Média  
**Benefício Esperado:** Contribuições externas + reputação

---

**Documento mantido pelo Agente Orquestrador**  
**Última atualização:** 18 de Outubro, 2025 - 23:55 BRT
