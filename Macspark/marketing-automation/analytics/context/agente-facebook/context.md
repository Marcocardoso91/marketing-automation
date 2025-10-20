# Contexto Estratégico - Agente Facebook / Projeto Sabrina

**Versão:** 2.0.0  
**Data:** 18 de Outubro, 2025  
**Status:** Em Execução - Semana 2

---

## Missão

Transformar o crescimento do Instagram da Sabrina em um **processo sistemático, automatizado e baseado em dados**, combinando **Meta Ads + Conteúdo Orgânico**, com objetivo de conquistar **+900 a 1.300 novos seguidores em 28 dias** (11 Out - 8 Nov 2025) através de automação inteligente que integra Meta Ads API, Notion API e n8n.

---

## Visão de Longo Prazo

Criar um **framework replicável** de crescimento em redes sociais que:
- ✅ Elimine trabalho manual repetitivo
- ✅ Forneça insights em tempo real
- ✅ Permita decisões baseadas em dados
- ✅ Seja escalável para outros perfis/nichos
- ✅ Possa ser open-sourced para comunidade

---

## Stakeholders

### 🎯 **Primary Stakeholder**
**Sabrina** (Gestora de Marketing / Product Owner)
- **Responsabilidade:** Definir objetivos, criar conteúdo, executar estratégia
- **Expectativa:** Sistema funcional que reduza 80% do trabalho manual
- **Nível de Envolvimento:** Alto (uso diário)
- **Canal de Comunicação:** Notion + feedback direto

### 🔧 **Technical Stakeholders**
**Equipe de Automação (n8n)**
- **Responsabilidade:** Manter workflows, resolver bugs, implementar melhorias
- **Expectativa:** Sistema estável com <1% de falhas
- **Nível de Envolvimento:** Médio (manutenção semanal)
- **Canal de Comunicação:** Logs n8n + Portainer

**Analistas de Dados**
- **Responsabilidade:** Validar métricas, identificar padrões, gerar insights
- **Expectativa:** Dados precisos e rastreáveis
- **Nível de Envolvimento:** Baixo (revisão semanal)
- **Canal de Comunicação:** Notion Databases + Relatórios

### 🌐 **External Stakeholders**
**Instagram Followers (Audiência Final)**
- **Responsabilidade:** Consumir conteúdo e engajar
- **Expectativa:** Conteúdo de qualidade e autêntico
- **Nível de Envolvimento:** Passivo (consumo)

**Meta Platforms (Provedor de API)**
- **Responsabilidade:** Manter APIs estáveis e documentadas
- **Expectativa:** Uso dentro de rate limits e termos de serviço
- **Nível de Envolvimento:** Indireto (via API)

---

## Contexto do Negócio

### 📊 **Estado Atual (18 Out 2025)**

**Instagram Real:**
- **Seguidores:** 16.130 (baseline: 16.129 em 11 Out)
- **Mudança Líquida:** -5 seguidores (perdeu 14, ganhou 9)
- **Contexto:** Mudança de nicho em andamento
- **Performance Orgânica:** +58,5% crescimento em alcance

**Campanhas Meta Ads:**
- **Gasto Total:** R$ 83,78 (1-18 Out)
- **Alcance:** 41.251 pessoas
- **Frequência:** 1,00 (ideal)
- **CPE:** R$ 0,003 (excelente)
- **CTR:** 0,42% (abaixo da meta, em otimização)

**Performance de Conteúdo:**
- **Stories:** 76,5-79% das visualizações (formato dominante)
- **Reels:** 20,5-22,9% das visualizações (alto potencial)
- **Posts:** 0,5-0,7% das visualizações (baixo desempenho)

### 🎯 **Objetivos de Negócio**

**Primário:**
- Conquistar +900 a 1.300 novos seguidores em 28 dias

**Secundários:**
- Manter custo por seguidor ≤ R$ 1,30
- Atingir ROI de 2,5-3,5x
- Estabelecer processo replicável
- Reduzir 80% do tempo em coleta manual

**Terciários:**
- Aumentar engagement rate para 1,5-2,4%
- Melhorar CTR para ≥ 1,5%
- Construir comunidade engajada (não apenas números)

---

## Restrições

### 🔒 **Segurança**
- ✅ **CRÍTICO**: Tokens e segredos NUNCA em repositórios públicos
- ✅ **OBRIGATÓRIO**: Uso de `.env` (gitignored) para credenciais
- ✅ **RECOMENDADO**: Docker Secrets para produção (planejado)
- ✅ **PROIBIDO**: Hardcoded tokens em código versionado

### 💰 **Orçamento**
- **Total:** R$ 1.120 (28 dias)
- **Distribuição:**
  - Semana 1: R$ 140 (✅ Executado: +116 seguidores)
  - Semana 2: R$ 280 (🔵 Em andamento)
  - Semana 3: R$ 312 (📅 Planejado)
  - Semana 4: R$ 384 (📅 Planejado)
- **Restrição:** Não exceder budget total
- **Contingência:** 10% de margem (R$ 112) para testes

### 🔗 **APIs Externas**
- **Meta Ads API**: 200 calls/hour (rate limit)
- **Notion API**: 3 requests/second (rate limit)
- **Instagram Insights**: Manual (sem API pública)

**Mitigações:**
- Throttling no n8n para respeitar limites
- Retry logic com exponential backoff
- Fallback para script Python em caso de falha n8n

### ⏱️ **Tempo**
- **Deadline Fixo:** 8 de Novembro, 2025
- **Duração:** 28 dias (4 semanas)
- **Não Negociável:** Budget e prazo são fixos
- **Flexível:** Estratégia pode ser ajustada baseada em dados

### 🏗️ **Infraestrutura**
- **VPS:** Recursos limitados (compartilhado)
- **Docker:** Overhead aceitável (<100MB RAM)
- **Uptime:** Depende de VPS (sem SLA garantido)

**Mitigações:**
- Monitoramento via Portainer
- Script Python como fallback (não depende de VPS)
- Snapshots diários para recovery rápido

---

## Premissas

### ✅ **Validadas e Confirmadas**

1. **Notion API e Meta Ads API ativas** com credenciais válidas
   - Status: ✅ Testado e funcionando
   - Última validação: 18 Out 2025

2. **Servidor VPS configurado** com Docker e Portainer
   - Status: ✅ n8n rodando em produção
   - URL: https://fluxos.macspark.dev

3. **Sabrina tem acesso** ao Meta Ads Manager e Instagram Insights
   - Status: ✅ Confirmado
   - Permissões: Admin em Business Manager

4. **Instagram em conta Business/Professional**
   - Status: ✅ Validado
   - Insights disponíveis

5. **Budget aprovado** e disponível
   - Status: ✅ R$ 1.120 alocados
   - Fonte: Sabrina (PO)

### ⚠️ **Premissas de Risco (Validação Contínua)**

1. **Meta Ads API permanecerá estável**
   - Risco: Mudanças breaking na API
   - Mitigação: Versioning fixo (v21.0)

2. **Notion não mudará rate limits drasticamente**
   - Risco: Throttling mais agressivo
   - Mitigação: Backup via export semanal

3. **VPS manterá uptime >99%**
   - Risco: Downtime imprevisto
   - Mitigação: Script Python como fallback

4. **Audiência responderá positivamente ao novo nicho**
   - Risco: Perda de seguidores durante transição
   - Mitigação: Foco em qualidade > quantidade

5. **Tokens Meta Ads serão renovados antes de expirar**
   - Risco: Token expirado = automação quebrada
   - Mitigação: Alerta 7 dias antes + processo documentado

---

## Decisões Estratégicas Chave

### 🎯 **Mudança de Nicho (ADR-008)**
**Decisão:** Transição gradual para novo nicho, aceitando perda temporária de seguidores.

**Justificativa:**
- Seguidores do novo nicho são mais valiosos (engajamento alto)
- Autenticidade gera conexão de longo prazo
- Crescimento orgânico (+58,5%) valida força do conteúdo

**Impacto:**
- ✅ Seguidores qualificados
- ⚠️ Perda temporária esperada (-5 líquidos é aceitável)
- 📊 Métricas de qualidade > quantidade

### 🤖 **Automação como Prioridade (ADR-001)**
**Decisão:** Investir em automação (n8n + Python) ao invés de coleta manual.

**Justificativa:**
- Reduz 80% do tempo manual
- Elimina erros humanos
- Permite decisões em tempo real

**Impacto:**
- ✅ Eficiência operacional
- ✅ Dados sempre atualizados
- ⚠️ Dependência de infraestrutura

### 📊 **Rastreabilidade Total (ADR-007)**
**Decisão:** Cada requisito deve ser rastreável até implementação e fonte.

**Justificativa:**
- Auditoria automática
- Validação de coerência
- Base para relatórios

**Impacto:**
- ✅ Score de coerência 100%
- ✅ PRD vivo e atualizado
- ⚠️ Overhead de documentação

---

## Riscos Estratégicos

| ID | Risco | Probabilidade | Impacto | Mitigação | Status |
|----|-------|--------------|---------|-----------|--------|
| **RISK-001** | Token Meta expira sem aviso | Média | Alto | Alerta 7 dias antes + docs renovação | 🟢 Monitorando |
| **RISK-002** | API Meta breaking change | Baixa | Alto | Versioning fixo + monitor changelog | 🟢 Ativo |
| **RISK-003** | Rate limit excedido | Baixa | Médio | Throttling + retry logic | 🟢 Ativo |
| **RISK-004** | Perda acelerada de seguidores | Alta | Baixo | Qualidade > quantidade + engajamento | 🟡 Observando |
| **RISK-005** | n8n downtime | Baixa | Médio | Portainer + Python fallback | 🟢 Mitigado |
| **RISK-006** | Budget insuficiente | Baixa | Alto | Contingência 10% + otimização contínua | 🟢 Controlado |
| **RISK-007** | Instagram muda algoritmo | Média | Médio | Adaptação estratégia + testes A/B | 🟡 Observando |

---

## Oportunidades Identificadas

### 🚀 **Curto Prazo (Semanas 2-4)**
1. **Otimizar hooks dos Reels** (primeiros 3 seg) → +25% CTR
2. **Implementar DM automation** → +35% retenção
3. **Pausar AD 03** (baixo CTR) → Economia R$ 40-50/dia
4. **Escalar budget 20%** após vencedores identificados

### 📈 **Médio Prazo (1-3 meses)**
1. **Lookalike Audiences** → Expandir alcance 3x
2. **Conteúdo UGC** → +67% conversão vs branded
3. **WhatsApp integration** → Canal direto com followers

### 🌟 **Longo Prazo (3-6 meses)**
1. **Open-sourcing framework** → Contribuições comunidade
2. **ML para previsão** → -40% criativos baixa performance
3. **Replicar para outros nichos** → Escalabilidade

---

## Lições Aprendidas (Atualizado 18 Out)

### ✅ **O que funcionou**
1. **CPE R$ 0,003** - Muito abaixo da média (R$ 0,50-0,70)
2. **Frequência 1,00** - Ideal, sem ad fatigue
3. **Crescimento orgânico +58,5%** - Conteúdo forte
4. **Stories dominam** (79%) - Formato certo

### ⚠️ **O que precisa melhorar**
1. **CTR 0,42%** - Abaixo da meta (1,5%)
2. **AD 03 desperdiça budget** - CTR 0,28%
3. **Posts estáticos** - Apenas 0,6% views

### 🔧 **Correções aplicadas**
1. **ADR-009**: Corrigir dados Instagram (16.130 vs 1.142)
2. **Planejar pausar AD 03** e realocar budget
3. **Focar em Reels + Stories** (abandonar posts estáticos)

---

## Próximos Marcos

| Data | Marco | Critério de Sucesso |
|------|-------|---------------------|
| **24 Out** | Fim Semana 2 | +200-280 seguidores \| CTR >1,0% |
| **31 Out** | Fim Semana 3 | +250-350 seguidores \| Criativos vencedores identificados |
| **7 Nov** | Fim Semana 4 | +300-450 seguidores \| ROI 2,5-3,5x |
| **8 Nov** | Conclusão Projeto | +900-1.300 total \| Sistema escalável validado |

---

## Contato e Escalação

**Product Owner:**  
Sabrina - Decisões de negócio e estratégia

**Technical Lead:**  
Equipe n8n - Infraestrutura e automação

**Documentação:**  
Agente Orquestrador - Manutenção de PRDs e rastreabilidade

**Escalação de Problemas:**
1. **Nível 1**: Logs n8n + Python script (self-service)
2. **Nível 2**: Equipe n8n (bugs técnicos)
3. **Nível 3**: Sabrina (decisões estratégicas)

---

**Documento mantido pelo Agente Orquestrador**  
**Última atualização:** 18 de Outubro, 2025 - 00:05 BRT  
**Próxima revisão:** Fim de cada semana
