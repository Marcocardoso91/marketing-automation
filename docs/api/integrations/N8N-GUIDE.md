# 🔧 Guia N8N - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 🎯 O Que É N8N e Para Que Serve

**N8N** é uma plataforma de automação de workflows que permite conectar diferentes serviços e APIs sem código. No Marketing Automation Platform, o N8N é usado para:

- ✅ **Coleta automatizada** de métricas do Facebook Ads
- ✅ **Sincronização** de dados entre sistemas
- ✅ **Alertas inteligentes** baseados em performance
- ✅ **Relatórios automáticos** para Notion
- ✅ **Integração** com múltiplas fontes de dados

---

## 📋 Pré-requisitos

### Sistema
- ✅ N8N instalado e rodando (Docker ou local)
- ✅ Marketing Automation Platform funcionando
- ✅ Conta Facebook Business Manager
- ✅ Acesso ao Supabase
- ✅ Conta Notion (opcional)

### Credenciais Necessárias
- **Facebook Access Token** (com permissões `ads_read`, `ads_management`)
- **Supabase URL e Key**
- **Notion API Key** (se usando integração Notion)
- **Agent API Key** (para endpoints de métricas)

---

## 🚀 Configuração Inicial

### 1. Acessar N8N

**URL:** http://localhost:5678 (ou sua instância)

**Primeira vez:**
1. Criar conta de administrador
2. Definir senha segura
3. Configurar timezone (UTC-3 para Brasil)

### 2. Configurar Credenciais

#### 2.1 Facebook API Credential

1. **Settings → Credentials → Add Credential**
2. **Tipo:** "HTTP Request Auth"
3. **Configuração:**
   ```json
   {
     "name": "Facebook API",
     "authentication": "predefinedCredentialType",
     "data": {
       "httpAuth": {
         "authType": "bearer",
         "token": "EAA_your_facebook_token_here"
       }
     }
   }
   ```

#### 2.2 Supabase Credential

1. **Settings → Credentials → Add Credential**
2. **Tipo:** "HTTP Request Auth"
3. **Configuração:**
   ```json
   {
     "name": "Supabase",
     "authentication": "predefinedCredentialType",
     "data": {
       "httpAuth": {
         "authType": "headerAuth",
         "headerAuth": {
           "name": "apikey",
           "value": "your_supabase_anon_key"
         }
       }
     }
   }
   ```

#### 2.3 Agent API Credential

1. **Settings → Credentials → Add Credential**
2. **Tipo:** "HTTP Request Auth"
3. **Configuração:**
   ```json
   {
     "name": "Agent API",
     "authentication": "predefinedCredentialType",
     "data": {
       "httpAuth": {
         "authType": "headerAuth",
         "headerAuth": {
           "name": "X-API-Key",
           "value": "your_agent_api_key"
         }
       }
     }
   }
   ```

---

## 📦 Workflows Disponíveis

### 1. Meta Ads → Supabase

**Arquivo:** `analytics/n8n-workflows/meta-ads-supabase.json`

**Funcionalidade:**
- Coleta métricas do Facebook Ads
- Salva no Supabase
- Executa diariamente às 20h

**Configuração:**
1. **Import from File:** `meta-ads-supabase.json`
2. **Configure credentials** nos nós
3. **Set schedule** (cron: `0 20 * * *`)
4. **Activate workflow**

### 2. Meta Ads → Notion

**Arquivo:** `analytics/n8n-workflows/meta-ads-notion.json`

**Funcionalidade:**
- Coleta métricas do Facebook
- Cria relatório no Notion
- Envia por email

**Configuração:**
1. **Import from File:** `meta-ads-notion.json`
2. **Configure Notion credential**
3. **Set database ID**
4. **Activate workflow**

### 3. Google Ads → Supabase

**Arquivo:** `analytics/n8n-workflows/google-ads-supabase.json`

**Funcionalidade:**
- Coleta métricas do Google Ads
- Salva no Supabase
- Integração com Facebook Ads

### 4. Google Analytics → Supabase

**Arquivo:** `analytics/n8n-workflows/google-analytics-supabase.json`

**Funcionalidade:**
- Coleta dados do GA4
- Salva no Supabase
- Correlaciona com campanhas

### 5. YouTube → Supabase

**Arquivo:** `analytics/n8n-workflows/youtube-supabase.json`

**Funcionalidade:**
- Coleta métricas do YouTube
- Salva no Supabase
- Análise de performance

### 6. Consolidate, Analyze & Notify

**Arquivo:** `analytics/n8n-workflows/consolidate-analyze-notify.json`

**Funcionalidade:**
- Consolida dados de múltiplas fontes
- Análise de performance
- Alertas inteligentes
- Relatórios automáticos

---

## 🛠️ Criar Workflow Customizado

### 1. Workflow Básico: Coleta de Métricas

**Passos:**
1. **Trigger:** Schedule (diário às 20h)
2. **HTTP Request:** GET `/api/v1/metrics/export`
3. **Data Processing:** Transformar dados
4. **HTTP Request:** POST para Supabase
5. **Notification:** Slack/Email (opcional)

**Configuração do Trigger:**
```json
{
  "rule": {
    "interval": [
      {
        "field": "cronExpression",
        "expression": "0 20 * * *"
      }
    ]
  }
}
```

**Configuração do HTTP Request (Agent API):**
```json
{
  "method": "GET",
  "url": "http://localhost:8000/api/v1/metrics/export",
  "headers": {
    "X-API-Key": "={{$credentials.agentApi.apiKey}}"
  },
  "qs": {
    "date_from": "={{$now.minus({days: 1}).format('YYYY-MM-DD')}}",
    "date_until": "={{$now.format('YYYY-MM-DD')}}"
  }
}
```

### 2. Workflow Avançado: Alertas Inteligentes

**Passos:**
1. **Trigger:** Schedule (a cada 4 horas)
2. **HTTP Request:** GET `/api/v1/analytics/dashboard`
3. **IF Node:** Verificar condições
4. **Switch Node:** Diferentes tipos de alerta
5. **HTTP Request:** POST para Slack
6. **Email:** Notificação por email

**Condições de Alerta:**
- CTR < 1%
- CPA > R$ 50
- Spend > 80% do orçamento
- Campanhas pausadas inesperadamente

### 3. Workflow de Relatórios

**Passos:**
1. **Trigger:** Schedule (semanal)
2. **HTTP Request:** GET dados consolidados
3. **Data Processing:** Calcular métricas
4. **HTTP Request:** POST para Notion
5. **Email:** Enviar relatório

---

## 🔌 Integração com Agent API

### Endpoints Disponíveis

#### GET `/api/v1/metrics/export`
**Uso:** Coleta métricas formatadas
```json
{
  "method": "GET",
  "url": "http://localhost:8000/api/v1/metrics/export",
  "headers": {
    "X-API-Key": "your_api_key"
  },
  "qs": {
    "date_from": "2025-10-20",
    "date_until": "2025-10-23"
  }
}
```

#### GET `/api/v1/analytics/dashboard`
**Uso:** Dados do dashboard
```json
{
  "method": "GET",
  "url": "http://localhost:8000/api/v1/analytics/dashboard",
  "headers": {
    "Authorization": "Bearer your_jwt_token"
  }
}
```

#### POST `/api/v1/automation/pause-underperforming`
**Uso:** Sugestões de otimização
```json
{
  "method": "POST",
  "url": "http://localhost:8000/api/v1/automation/pause-underperforming",
  "headers": {
    "Authorization": "Bearer your_jwt_token",
    "Content-Type": "application/json"
  },
  "body": {
    "ctr_threshold": 1.0,
    "cpa_threshold": 50.0
  }
}
```

---

## 📊 Exemplos Práticos

### Exemplo 1: Coleta Diária Automática

```json
{
  "name": "Daily Metrics Collection",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "cronExpression", "expression": "0 20 * * *"}]
        }
      }
    },
    {
      "name": "Get Metrics",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "GET",
        "url": "http://localhost:8000/api/v1/metrics/export",
        "headers": {
          "X-API-Key": "={{$credentials.agentApi.apiKey}}"
        },
        "qs": {
          "date_from": "={{$now.minus({days: 1}).format('YYYY-MM-DD')}}",
          "date_until": "={{$now.format('YYYY-MM-DD')}}"
        }
      }
    },
    {
      "name": "Save to Supabase",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "{{$credentials.supabase.url}}/rest/v1/campaigns",
        "headers": {
          "apikey": "={{$credentials.supabase.apiKey}}",
          "Content-Type": "application/json"
        },
        "body": "={{$json}}"
      }
    }
  ]
}
```

### Exemplo 2: Alerta de Performance

```json
{
  "name": "Performance Alert",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "cronExpression", "expression": "0 */4 * * *"}]
        }
      }
    },
    {
      "name": "Get Dashboard",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "GET",
        "url": "http://localhost:8000/api/v1/analytics/dashboard",
        "headers": {
          "Authorization": "Bearer {{$credentials.agentApi.jwtToken}}"
        }
      }
    },
    {
      "name": "Check Performance",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{$json.summary.average_ctr}}",
              "operation": "smaller",
              "value2": 1.0
            }
          ]
        }
      }
    },
    {
      "name": "Send Slack Alert",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#marketing-alerts",
        "text": "⚠️ CTR baixo detectado: {{$json.summary.average_ctr}}%"
      }
    }
  ]
}
```

---

## 🚨 Troubleshooting N8N

### Problemas Comuns

#### ❌ Workflow Não Executa
**Sintomas:** Workflow ativo mas não executa

**Soluções:**
1. Verificar **schedule** configurado corretamente
2. Verificar **credentials** válidas
3. Verificar **logs** do workflow
4. Testar **execução manual**

#### ❌ Credentials Inválidas
**Sintomas:** Erro 401/403 nos requests

**Soluções:**
1. **Renovar tokens** (Facebook, Notion)
2. **Verificar permissões** das APIs
3. **Testar credentials** individualmente
4. **Recriar credentials** se necessário

#### ❌ Rate Limit Exceeded
**Sintomas:** Erro 429 (Too Many Requests)

**Soluções:**
1. **Reduzir frequência** de execução
2. **Implementar delays** entre requests
3. **Usar diferentes tokens** se disponível
4. **Monitorar rate limits** das APIs

#### ❌ Dados Não Aparecem
**Sintomas:** Workflow executa mas dados não chegam

**Soluções:**
1. **Verificar logs** de cada nó
2. **Testar endpoints** manualmente
3. **Verificar formato** dos dados
4. **Validar mapeamento** de campos

### Debugging

#### Ver Logs do Workflow
1. **Workflow → Executions**
2. **Clicar na execução** específica
3. **Ver logs** de cada nó
4. **Identificar erro** específico

#### Testar Nós Individualmente
1. **Clicar no nó** com problema
2. **Execute Node** (teste individual)
3. **Verificar output** do nó
4. **Ajustar configuração** se necessário

#### Verificar Credentials
1. **Settings → Credentials**
2. **Clicar na credential** específica
3. **Test Connection** (se disponível)
4. **Verificar valores** configurados

---

## 📈 Monitoramento e Otimização

### Métricas Importantes

- **Taxa de sucesso** dos workflows
- **Tempo de execução** médio
- **Erros por tipo** de nó
- **Rate limits** das APIs

### Otimizações

1. **Paralelizar** requests quando possível
2. **Implementar retry** para erros temporários
3. **Usar webhooks** em vez de polling
4. **Monitorar** performance dos workflows

### Alertas de Sistema

1. **Workflow falha** consecutivamente
2. **Rate limit** excedido
3. **Credential expira** em breve
4. **Sistema N8N** indisponível

---

## 🔗 Recursos Adicionais

### Documentação
- **N8N Docs:** https://docs.n8n.io
- **Node Reference:** https://docs.n8n.io/integrations/
- **API Reference:** [docs/api/agent-api/API-REFERENCE.md](../agent-api/API-REFERENCE.md)

### Comunidade
- **N8N Community:** https://community.n8n.io
- **GitHub:** https://github.com/n8n-io/n8n
- **Discord:** https://discord.gg/n8n

### Suporte
- **Troubleshooting:** [docs/reference/troubleshooting/TROUBLESHOOTING.md](../../reference/troubleshooting/TROUBLESHOOTING.md)
- **GitHub Issues:** [Criar issue](https://github.com/your-repo/issues)

---

## ✅ Checklist de Configuração

### Configuração Básica
- [ ] ✅ N8N instalado e funcionando
- [ ] ✅ Credenciais Facebook configuradas
- [ ] ✅ Credenciais Supabase configuradas
- [ ] ✅ Credenciais Agent API configuradas
- [ ] ✅ Workflow básico importado
- [ ] ✅ Workflow ativo e executando

### Configuração Avançada
- [ ] ✅ Workflows customizados criados
- [ ] ✅ Alertas configurados
- [ ] ✅ Integração Notion funcionando
- [ ] ✅ Monitoramento ativo
- [ ] ✅ Backup dos workflows
- [ ] ✅ Documentação da equipe

---

**💡 Dica:** Comece com workflows simples e vá adicionando complexidade gradualmente!
