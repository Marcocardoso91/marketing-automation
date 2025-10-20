# n8n Workflows Documentation
## Dashboard Sabrina Costa - Automações

**Versão:** 1.0  
**n8n Instance:** https://fluxos.macspark.dev  
**Total de Workflows:** 4

---

## Índice
1. [Workflow 1: Processar Métricas](#workflow-1-processar-métricas)
2. [Workflow 2: Alertas WhatsApp](#workflow-2-alertas-whatsapp)
3. [Workflow 3: Relatório Diário](#workflow-3-relatório-diário)
4. [Workflow 4: Lembretes de Postagem](#workflow-4-lembretes-de-postagem)
5. [Variáveis de Ambiente](#variáveis-de-ambiente)
6. [Troubleshooting](#troubleshooting)

---

## Workflow 1: Processar Métricas

**Nome:** `Sabrina_01_ProcessarMetricas`  
**Descrição:** Recebe CSV/JSON de métricas do Instagram, valida, processa e salva no banco de dados via API. Verifica thresholds e dispara alertas se necessário.  
**Status:** Ativo  
**Execução:** On-demand (Webhook)

### Trigger

**Node:** Webhook  
**Tipo:** POST  
**Path:** `/webhook/sabrina/metricas`  
**Autenticação:** Header Token

**Headers esperados:**
```
X-Webhook-Token: {{WEBHOOK_SECRET}}
Content-Type: application/json ou text/csv
```

### Fluxo de Nós

#### 1. Webhook Trigger
```json
{
  "name": "Webhook - Receber Métricas",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 1,
  "position": [250, 300],
  "webhookId": "sabrina-metricas",
  "parameters": {
    "httpMethod": "POST",
    "path": "sabrina/metricas",
    "responseMode": "responseNode",
    "options": {
      "rawBody": true
    }
  }
}
```

#### 2. Detectar Formato (CSV ou JSON)
```json
{
  "name": "Detectar Formato",
  "type": "n8n-nodes-base.function",
  "typeVersion": 1,
  "position": [450, 300],
  "parameters": {
    "functionCode": "const contentType = $input.item.headers['content-type'];\nconst body = $input.item.body;\n\nif (contentType.includes('text/csv') || typeof body === 'string') {\n  return { json: { format: 'csv', data: body } };\n} else {\n  return { json: { format: 'json', data: body } };\n}"
  }
}
```

#### 3a. Parse CSV (Branch)
```json
{
  "name": "Parse CSV",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [650, 200],
  "parameters": {
    "language": "javaScript",
    "jsCode": "const Papa = require('papaparse');\nconst csvData = $input.item.json.data;\n\nconst parsed = Papa.parse(csvData, {\n  header: true,\n  skipEmptyLines: true,\n  dynamicTyping: true\n});\n\nif (parsed.errors.length > 0) {\n  throw new Error('Erro ao parsear CSV: ' + JSON.stringify(parsed.errors));\n}\n\nreturn parsed.data.map(row => ({ json: row }));"
  }
}
```

#### 3b. Validar JSON (Branch)
```json
{
  "name": "Validar JSON",
  "type": "n8n-nodes-base.function",
  "typeVersion": 1,
  "position": [650, 400],
  "parameters": {
    "functionCode": "const data = $input.item.json.data;\n\n// Se for array, retorna cada item\nif (Array.isArray(data)) {\n  return data.map(item => ({ json: item }));\n}\n\n// Se for objeto único, retorna como array de 1\nreturn [{ json: data }];"
  }
}
```

#### 4. Merge Branches
```json
{
  "name": "Merge",
  "type": "n8n-nodes-base.merge",
  "typeVersion": 2,
  "position": [850, 300],
  "parameters": {
    "mode": "append"
  }
}
```

#### 5. Validar Campos Obrigatórios
```json
{
  "name": "Validar Campos",
  "type": "n8n-nodes-base.function",
  "typeVersion": 1,
  "position": [1050, 300],
  "parameters": {
    "functionCode": "const item = $input.item.json;\n\n// Campos obrigatórios\nconst required = ['date', 'ctr', 'cpc', 'cost'];\n\nfor (const field of required) {\n  if (item[field] === undefined || item[field] === null) {\n    throw new Error(`Campo obrigatório faltando: ${field}`);\n  }\n}\n\n// Validar tipos\nif (isNaN(parseFloat(item.ctr))) {\n  throw new Error('CTR deve ser um número');\n}\n\nif (parseFloat(item.ctr) < 0 || parseFloat(item.ctr) > 100) {\n  throw new Error('CTR deve estar entre 0 e 100');\n}\n\n// Validar data\nconst date = new Date(item.date);\nif (isNaN(date.getTime())) {\n  throw new Error('Data inválida');\n}\n\nif (date > new Date()) {\n  throw new Error('Data não pode ser futura');\n}\n\nreturn { json: item };"
  }
}
```

#### 6. Calcular Campos Derivados
```json
{
  "name": "Calcular Derivados",
  "type": "n8n-nodes-base.function",
  "typeVersion": 1,
  "position": [1250, 300],
  "parameters": {
    "functionCode": "const item = $input.item.json;\n\n// Custo por seguidor\nif (item.newFollowers && item.newFollowers > 0) {\n  item.costPerFollower = (item.cost / item.newFollowers).toFixed(2);\n} else {\n  item.costPerFollower = null;\n}\n\n// Calcular clicks se não fornecido\nif (!item.clicks && item.impressions && item.ctr) {\n  item.clicks = Math.round(item.impressions * (item.ctr / 100));\n}\n\n// Formatar date para YYYY-MM-DD\nitem.date = new Date(item.date).toISOString().split('T')[0];\n\nreturn { json: item };"
  }
}
```

#### 7. HTTP Request - Salvar no Banco
```json
{
  "name": "POST /api/webhook/metrics",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 3,
  "position": [1450, 300],
  "parameters": {
    "method": "POST",
    "url": "={{$env.API_BASE_URL}}/api/webhook/metrics",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-Webhook-Token",
          "value": "={{$env.WEBHOOK_SECRET}}"
        }
      ]
    },
    "sendBody": true,
    "bodyParameters": {
      "parameters": []
    },
    "options": {
      "response": {
        "response": {
          "fullResponse": false,
          "neverError": false
        }
      }
    }
  }
}
```

#### 8. Verificar Thresholds
```json
{
  "name": "Verificar Thresholds",
  "type": "n8n-nodes-base.function",
  "typeVersion": 1,
  "position": [1650, 300],
  "parameters": {
    "functionCode": "const metrics = $input.item.json;\nconst alerts = [];\n\n// Thresholds (podem vir de config da API futuramente)\nconst thresholds = {\n  ctrMin: 1.5,\n  cpcMax: 0.70,\n  cpmMax: 10.0,\n  frequencyMax: 3.0,\n  costPerFollowerMax: 1.30\n};\n\n// Verificar CTR\nif (metrics.ctr && metrics.ctr < thresholds.ctrMin) {\n  alerts.push({\n    type: 'ctr_low',\n    message: `⚠️ CTR abaixo da meta: ${metrics.ctr}% (meta: ${thresholds.ctrMin}%)`,\n    metadata: {\n      date: metrics.date,\n      value: metrics.ctr,\n      threshold: thresholds.ctrMin\n    }\n  });\n}\n\n// Verificar CPC\nif (metrics.cpc && metrics.cpc > thresholds.cpcMax) {\n  alerts.push({\n    type: 'cpc_high',\n    message: `⚠️ CPC acima da meta: R$${metrics.cpc} (meta: R$${thresholds.cpcMax})`,\n    metadata: {\n      date: metrics.date,\n      value: metrics.cpc,\n      threshold: thresholds.cpcMax\n    }\n  });\n}\n\n// Verificar Frequência\nif (metrics.frequency && metrics.frequency > thresholds.frequencyMax) {\n  alerts.push({\n    type: 'frequency_high',\n    message: `⚠️ Frequência muito alta: ${metrics.frequency} (meta: ${thresholds.frequencyMax})`,\n    metadata: {\n      date: metrics.date,\n      value: metrics.frequency,\n      threshold: thresholds.frequencyMax\n    }\n  });\n}\n\n// Verificar Custo por Seguidor\nif (metrics.costPerFollower && parseFloat(metrics.costPerFollower) > thresholds.costPerFollowerMax) {\n  alerts.push({\n    type: 'cost_per_follower_high',\n    message: `⚠️ Custo por seguidor alto: R$${metrics.costPerFollower} (meta: R$${thresholds.costPerFollowerMax})`,\n    metadata: {\n      date: metrics.date,\n      value: metrics.costPerFollower,\n      threshold: thresholds.costPerFollowerMax\n    }\n  });\n}\n\nreturn [{ json: { alerts, metrics, hasAlerts: alerts.length > 0 } }];"
  }
}
```

#### 9. IF - Tem Alertas?
```json
{
  "name": "Tem Alertas?",
  "type": "n8n-nodes-base.if",
  "typeVersion": 1,
  "position": [1850, 300],
  "parameters": {
    "conditions": {
      "boolean": [
        {
          "value1": "={{$json.hasAlerts}}",
          "value2": true
        }
      ]
    }
  }
}
```

#### 10a. Enviar Alertas WhatsApp
```json
{
  "name": "Enviar Alertas WhatsApp",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 3,
  "position": [2050, 200],
  "parameters": {
    "method": "POST",
    "url": "={{$env.EVOLUTION_API_URL}}/message/sendText/{{$env.WHATSAPP_INSTANCE}}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "apikey",
          "value": "={{$env.EVOLUTION_API_KEY}}"
        }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={\n  \"number\": \"{{$env.WHATSAPP_NUMBER}}\",\n  \"text\": \"{{$json.alerts.map(a => a.message).join('\\n\\n')}}\"\n}",
    "options": {}
  }
}
```

#### 10b. Salvar Alertas no Banco
```json
{
  "name": "POST /api/alerts",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 3,
  "position": [2050, 400],
  "parameters": {
    "method": "POST",
    "url": "={{$env.API_BASE_URL}}/api/alerts",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-Webhook-Token",
          "value": "={{$env.WEBHOOK_SECRET}}"
        }
      ]
    },
    "sendBody": true,
    "options": {}
  }
}
```

#### 11. Resposta de Sucesso
```json
{
  "name": "Resposta Sucesso",
  "type": "n8n-nodes-base.respondToWebhook",
  "typeVersion": 1,
  "position": [2250, 300],
  "parameters": {
    "respondWith": "json",
    "responseBody": "={\n  \"success\": true,\n  \"message\": \"Métricas processadas com sucesso\",\n  \"savedRecords\": {{$json.savedRecords || 1}},\n  \"alertsGenerated\": {{$json.alerts ? $json.alerts.length : 0}}\n}",
    "options": {
      "responseCode": 200
    }
  }
}
```

---

## Workflow 2: Alertas WhatsApp

**Nome:** `Sabrina_02_AlertasWhatsApp`  
**Descrição:** Verifica métricas diariamente às 18h e envia alertas via WhatsApp se alguma métrica estiver fora do padrão.  
**Status:** Ativo  
**Execução:** Cron (diariamente às 18:00)

### Trigger

**Node:** Cron  
**Schedule:** `0 18 * * *` (18h todos os dias)

```json
{
  "name": "Cron - 18h Diariamente",
  "type": "n8n-nodes-base.cron",
  "typeVersion": 1,
  "position": [250, 300],
  "parameters": {
    "triggerTimes": {
      "item": [
        {
          "hour": 18,
          "minute": 0
        }
      ]
    }
  }
}
```

### Fluxo de Nós

#### 1. GET Métricas do Dia
```json
{
  "name": "GET /api/metrics hoje",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 3,
  "position": [450, 300],
  "parameters": {
    "method": "GET",
    "url": "={{$env.API_BASE_URL}}/api/metrics?date={{$today}}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-Webhook-Token",
          "value": "={{$env.WEBHOOK_SECRET}}"
        }
      ]
    },
    "options": {}
  }
}
```

#### 2. GET Configurações de Thresholds
```json
{
  "name": "GET /api/alerts/config",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 3,
  "position": [650, 300],
  "parameters": {
    "method": "GET",
    "url": "={{$env.API_BASE_URL}}/api/alerts/config",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-Webhook-Token",
          "value": "={{$env.WEBHOOK_SECRET}}"
        }
      ]
    },
    "options": {}
  }
}
```

#### 3. Verificar Thresholds
```json
{
  "name": "Verificar Thresholds",
  "type": "n8n-nodes-base.function",
  "typeVersion": 1,
  "position": [850, 300],
  "parameters": {
    "functionCode": "const metrics = $input.first().json.data[0]; // Métricas de hoje\nconst config = $input.last().json.data.thresholds; // Thresholds\n\nconst alerts = [];\n\nif (!metrics) {\n  return [{ json: { hasAlerts: false, message: 'Sem métricas para hoje' } }];\n}\n\n// CTR\nif (metrics.ctr < config.ctrMin) {\n  alerts.push(`⚠️ *CTR Baixo*\\nValor: ${metrics.ctr}%\\nMeta: ${config.ctrMin}%\\nAção: Testar novos ganchos`);\n}\n\n// CPC\nif (metrics.cpc > config.cpcMax) {\n  alerts.push(`⚠️ *CPC Alto*\\nValor: R$${metrics.cpc}\\nMeta: R$${config.cpcMax}\\nAção: Refinar público ou criativos`);\n}\n\n// CPM\nif (metrics.cpm && metrics.cpm > config.cpmMax) {\n  alerts.push(`⚠️ *CPM Alto*\\nValor: R$${metrics.cpm}\\nMeta: R$${config.cpmMax}\\nAção: Verificar concorrência`);\n}\n\n// Frequência\nif (metrics.frequency > config.frequencyMax) {\n  alerts.push(`⚠️ *Frequência Alta*\\nValor: ${metrics.frequency}\\nMeta: ${config.frequencyMax}\\nAção: Expandir público ou pausar`);\n}\n\n// Custo por Seguidor\nif (metrics.costPerFollower && parseFloat(metrics.costPerFollower) > config.costPerFollowerMax) {\n  alerts.push(`⚠️ *Custo por Seguidor Alto*\\nValor: R$${metrics.costPerFollower}\\nMeta: R$${config.costPerFollowerMax}\\nAção: Otimizar conversão`);\n}\n\nreturn [{\n  json: {\n    hasAlerts: alerts.length > 0,\n    alerts,\n    metrics,\n    date: metrics.date\n  }\n}];"
  }
}
```

#### 4. IF - Tem Alertas?
```json
{
  "name": "Tem Alertas?",
  "type": "n8n-nodes-base.if",
  "typeVersion": 1,
  "position": [1050, 300],
  "parameters": {
    "conditions": {
      "boolean": [
        {
          "value1": "={{$json.hasAlerts}}",
          "value2": true
        }
      ]
    }
  }
}
```

#### 5. Formatar Mensagem WhatsApp
```json
{
  "name": "Formatar Mensagem",
  "type": "n8n-nodes-base.function",
  "typeVersion": 1,
  "position": [1250, 200],
  "parameters": {
    "functionCode": "const data = $input.item.json;\nconst date = new Date(data.date).toLocaleDateString('pt-BR');\n\nconst message = `\n🚨 *ALERTAS DE MÉTRICAS* 🚨\nData: ${date}\n\n${data.alerts.join('\\n\\n---\\n\\n')}\n\n📊 *Métricas do Dia*\n• Alcance: ${data.metrics.impressions || 'N/A'}\n• CTR: ${data.metrics.ctr}%\n• CPC: R$${data.metrics.cpc}\n• Frequência: ${data.metrics.frequency}\n• Novos Seguidores: ${data.metrics.newFollowers || 'N/A'}\n• Investimento: R$${data.metrics.cost}\n\n🔗 Ver dashboard: ${process.env.DASHBOARD_URL}\n`;\n\nreturn [{ json: { message } }];"
  }
}
```

#### 6. Enviar WhatsApp
```json
{
  "name": "Enviar WhatsApp",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 3,
  "position": [1450, 200],
  "parameters": {
    "method": "POST",
    "url": "={{$env.EVOLUTION_API_URL}}/message/sendText/{{$env.WHATSAPP_INSTANCE}}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "apikey",
          "value": "={{$env.EVOLUTION_API_KEY}}"
        }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={\n  \"number\": \"{{$env.WHATSAPP_NUMBER}}\",\n  \"text\": \"{{$json.message}}\"\n}",
    "options": {
      "response": {
        "response": {
          "neverError": true
        }
      },
      "timeout": 10000
    }
  }
}
```

#### 7. Log Alerta no Banco
```json
{
  "name": "POST /api/alerts",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 3,
  "position": [1650, 200],
  "parameters": {
    "method": "POST",
    "url": "={{$env.API_BASE_URL}}/api/alerts",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-Webhook-Token",
          "value": "={{$env.WEBHOOK_SECRET}}"
        }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={\n  \"type\": \"daily_check\",\n  \"message\": \"Alertas enviados via WhatsApp\",\n  \"metadata\": {{$json}}\n}",
    "options": {}
  }
}
```

---

## Workflow 3: Relatório Diário

**Nome:** `Sabrina_03_RelatorioDiario`  
**Descrição:** Compila métricas do dia e envia relatório formatado via WhatsApp às 18h05 (após verificação de alertas).  
**Status:** Ativo  
**Execução:** Cron (diariamente às 18:05)

### Trigger

**Node:** Cron  
**Schedule:** `5 18 * * *` (18h05 todos os dias)

### Fluxo Simplificado

1. **Cron Trigger** → Dispara às 18h05
2. **GET Métricas Hoje** → Busca métricas do dia
3. **GET Métricas Ontem** → Busca métricas de ontem (comparação)
4. **Calcular Comparações** → Calcula variações percentuais
5. **Determinar Status Geral** → Bom/Atenção/Crítico baseado em regras
6. **Formatar Relatório** → Cria mensagem formatada
7. **Enviar WhatsApp** → Envia via Evolution API

**Template de Mensagem:**
```
📊 RELATÓRIO DIÁRIO - DD/MM/AAAA

✅ MÉTRICAS DO DIA
• Alcance: X.XXX
• CTR: X.XX% (↑X.X% vs ontem)
• CPC: R$X.XX (↓X.X% vs ontem)
• CPM: R$X.XX
• Frequência: X.XX
• Visitas ao Perfil: XX
• Novos Seguidores: XX (↑X vs ontem)
• Investimento: R$XX.XX

📈 PERFORMANCE
vs Ontem: [↑ Melhorou / ↓ Piorou / → Estável]
vs Meta: [✅ Atingindo / ⚠️ Atenção / ❌ Crítico]

🎯 STATUS GERAL: [✅ Bom / ⚠️ Atenção / ❌ Crítico]

💡 RECOMENDAÇÕES:
• [Ação sugerida 1]
• [Ação sugerida 2]

---
🔗 Ver detalhes: [URL do Dashboard]
```

---

## Workflow 4: Lembretes de Postagem

**Nome:** `Sabrina_04_LembretesPostagem`  
**Descrição:** Envia lembretes de posts planejados nos horários configurados (11h e 17h30).  
**Status:** Ativo  
**Execução:** Cron (múltiplos horários)

### Triggers

**Node 1:** Cron - 11h  
**Schedule:** `0 11 * * *`

**Node 2:** Cron - 17h30  
**Schedule:** `30 17 * * *`

### Fluxo Simplificado

1. **Cron Trigger** → Dispara em horário configurado
2. **GET Cronograma Hoje** → Busca posts planejados para hoje
3. **Filtrar Posts Próximos** → Filtra posts nas próximas 2 horas
4. **IF - Tem Posts?** → Verifica se há posts
5. **Loop Posts** → Para cada post encontrado:
   - Formatar lembrete com detalhes
   - Enviar via WhatsApp

**Template de Lembrete:**
```
🎬 LEMBRETE DE POSTAGEM

📅 Data: DD/MM/AAAA
⏰ Horário sugerido: HH:MM
📱 Formato: [Reel/Carrossel/Stories]

🎯 Tema: [Tema do Post]

💡 Hook Sugerido:
"[Gancho]"

✍️ CTA:
"[Call to Action]"

📝 Ideias de Stories:
[Ideas para stories]

---
✅ Marcar como concluído: [URL]
```

---

## Variáveis de Ambiente

### Configuração no n8n

Acessar: **Settings → Environments**

```bash
# API Backend
API_BASE_URL=https://dashboard-sabrina.vercel.app
WEBHOOK_SECRET=your_webhook_secret_token_here
DASHBOARD_URL=https://dashboard-sabrina.vercel.app

# Evolution API (WhatsApp)
EVOLUTION_API_URL=https://evolution.macspark.dev
EVOLUTION_API_KEY=your_evolution_api_key
WHATSAPP_INSTANCE=sabrina-instance
WHATSAPP_NUMBER=+5511999999999

# Timezone
TZ=America/Sao_Paulo
```

### Como Usar nas Expressões

```javascript
// Acessar variável de ambiente
{{$env.API_BASE_URL}}

// Exemplo em URL
url: "={{$env.API_BASE_URL}}/api/metrics"

// Exemplo em header
headerParameters: {
  parameters: [
    {
      name: "apikey",
      value: "={{$env.EVOLUTION_API_KEY}}"
    }
  ]
}
```

---

## Troubleshooting

### Problema 1: Webhook não recebe dados

**Sintomas:**
- Status 404 ou 500 no POST
- Workflow não executa

**Soluções:**
1. Verificar se workflow está ativo
2. Confirmar path do webhook: `/webhook/sabrina/metricas`
3. Verificar header `X-Webhook-Token`
4. Testar com Postman/curl primeiro
5. Verificar logs do n8n (Executions → Ver detalhes)

**Teste com curl:**
```bash
curl -X POST https://fluxos.macspark.dev/webhook/sabrina/metricas \
  -H "X-Webhook-Token: seu_token" \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-10-21","ctr":7.5,"cpc":0.09,"cost":20.00}'
```

---

### Problema 2: Alertas não são enviados

**Sintomas:**
- Workflow executa mas WhatsApp não recebe

**Soluções:**
1. Verificar credenciais Evolution API
2. Testar Evolution API diretamente:
```bash
curl -X POST https://evolution.macspark.dev/message/sendText/sabrina-instance \
  -H "apikey: seu_api_key" \
  -H "Content-Type: application/json" \
  -d '{"number":"+5511999999999","text":"Teste"}'
```
3. Verificar se número WhatsApp está correto (com +55)
4. Verificar logs do workflow (node "Enviar WhatsApp")
5. Verificar se Evolution API está online

---

### Problema 3: Cron não dispara no horário

**Sintomas:**
- Workflow configurado mas não executa automaticamente

**Soluções:**
1. Verificar timezone: `TZ=America/Sao_Paulo`
2. Confirmar expressão cron:
   - `0 18 * * *` = 18h00
   - `5 18 * * *` = 18h05
   - `30 17 * * *` = 17h30
3. Verificar se workflow está **ativo**
4. Testar execução manual primeiro
5. Verificar logs do n8n (System → Logs)

---

### Problema 4: CSV parsing falha

**Sintomas:**
- Erro ao processar CSV
- Dados não são salvos

**Soluções:**
1. Verificar encoding do CSV (UTF-8)
2. Confirmar separador (vírgula)
3. Verificar se header está presente
4. Testar CSV com dados de exemplo
5. Logs mostrarão linha com erro

**CSV Exemplo Válido:**
```csv
date,ctr,cpc,cpm,frequency,visits,newFollowers,cost,impressions,clicks
2025-10-21,7.5,0.09,2.0,0.98,90,50,20.00,1200,90
```

---

### Problema 5: Métricas duplicadas

**Sintomas:**
- Mesma métrica inserida múltiplas vezes

**Soluções:**
1. API deve ter constraint UNIQUE em `date`
2. Usar `INSERT ... ON CONFLICT` no banco
3. Verificar se workflow não está sendo chamado múltiplas vezes
4. Adicionar verificação no workflow antes de salvar

---

## Logs e Monitoramento

### Acessar Logs

**n8n Interface:**
1. Ir em **Executions**
2. Filtrar por workflow
3. Clicar em execução para ver detalhes
4. Ver output de cada node

### Logs Importantes

**Workflow 1 (Processar Métricas):**
- Node "Validar Campos": Ver erros de validação
- Node "POST /api/webhook/metrics": Ver resposta da API
- Node "Verificar Thresholds": Ver alertas gerados

**Workflow 2 (Alertas):**
- Node "GET /api/metrics": Ver se métricas foram encontradas
- Node "Verificar Thresholds": Ver quais alertas foram detectados
- Node "Enviar WhatsApp": Ver se mensagem foi enviada

### Alertas de Falha

Configurar email de notificação em **Settings → Workflows**:
- Enviar email se workflow falhar
- Enviar email se alerta crítico

---

## Importação dos Workflows

### Via Interface n8n

1. Acessar https://fluxos.macspark.dev
2. Clicar em **Workflows** → **Import from File**
3. Selecionar arquivo JSON (ex: `01-receber-metricas.json`)
4. Revisar configurações
5. Ativar workflow

### Via API

```bash
# Listar workflows
curl -X GET https://fluxos.macspark.dev/api/v1/workflows \
  -H "X-N8N-API-KEY: seu_api_key"

# Importar workflow
curl -X POST https://fluxos.macspark.dev/api/v1/workflows \
  -H "X-N8N-API-KEY: seu_api_key" \
  -H "Content-Type: application/json" \
  -d @01-receber-metricas.json
```

---

## Manutenção

### Backup dos Workflows

**Automatizado:**
- n8n já faz backup automático no banco
- Exportar JSON via interface periodicamente

**Manual:**
1. Acessar cada workflow
2. Clicar em "..." → **Download**
3. Salvar arquivo JSON
4. Commit no Git

### Atualização de Thresholds

Thresholds são configuráveis via API `/api/alerts/config`.

Para atualizar diretamente no workflow (não recomendado):
1. Editar node "Verificar Thresholds"
2. Alterar valores de `thresholds`
3. Salvar e ativar

---

**Última Atualização:** 20/10/2025  
**Próxima Revisão:** 20/11/2025

