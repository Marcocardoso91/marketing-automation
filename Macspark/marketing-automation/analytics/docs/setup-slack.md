# Setup Slack - Alertas e Notificações

**Versão:** 1.0.0  
**Data:** 18 de Outubro, 2025  
**Tempo Estimado:** 10 minutos

---

## 🎯 Objetivo

Configurar **Slack** para receber alertas automáticos e relatórios diários de métricas de marketing com insights gerados por IA.

---

## 📋 Métodos de Integração

Escolha um dos métodos abaixo:

---

### **MÉTODO 1: Webhook (Mais Simples)** ⭐ Recomendado

**Vantagens:**
- ✅ Setup em 2 minutos
- ✅ Sem autenticação complexa
- ✅ Suficiente para enviar mensagens

**Desvantagens:**
- ❌ Não permite ler mensagens ou criar canais

#### **Passo a Passo:**

1. **Criar Webhook:**
   - Acesse: https://api.slack.com/apps
   - Clique em **"Create New App"**
   - Escolha **"From scratch"**
   - Nome: `Marketing Metrics Bot`
   - Workspace: Selecione seu workspace
   - Clique em **"Create App"**

2. **Ativar Incoming Webhooks:**
   - No menu lateral, **"Incoming Webhooks"**
   - Toggle **"Activate Incoming Webhooks"** para ON
   - Scroll down e clique em **"Add New Webhook to Workspace"**
   - Selecione o canal: `#marketing-metrics` (ou criar novo)
   - Clique em **"Allow"**

3. **Copiar Webhook URL:**
   - ✅ Copie a URL que apareceu:
   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
   ```

4. **Testar Webhook:**
   ```bash
   curl -X POST https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX \
   -H 'Content-Type: application/json' \
   -d '{"text":"🚀 Bot de Marketing funcionando!"}'
   ```

5. **Adicionar ao `.env`:**
   ```bash
   # Slack Configuration
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../XXX...
   SLACK_CHANNEL=#marketing-metrics
   ```

✅ **Pronto! Webhook configurado.**

---

### **MÉTODO 2: OAuth App (Completo)**

**Use se precisar:**
- Criar canais programaticamente
- Ler mensagens
- Funcionalidades avançadas

#### **Passo a Passo:**

1. **Criar App** (igual Método 1, passos 1)

2. **Configurar OAuth Scopes:**
   - Menu lateral → **"OAuth & Permissions"**
   - Em **"Scopes"** → **"Bot Token Scopes"**, adicionar:
     - `chat:write` (enviar mensagens)
     - `chat:write.public` (mensagens em canais públicos)
     - `channels:read` (listar canais)
     - `channels:manage` (criar/modificar canais)
   - Scroll up e clique em **"Install to Workspace"**
   - Clique em **"Allow"**

3. **Copiar Bot Token:**
   - ✅ Copie **"Bot User OAuth Token"**:
   ```
   xoxb-000000000000-000000000000-XXXXXXXXXXXXXXXXXXXX
   ```

4. **Adicionar ao `.env`:**
   ```bash
   # Slack OAuth
   SLACK_BOT_TOKEN=xoxb-000...
   SLACK_CHANNEL=C01234567 # ID do canal (obter via Slack)
   ```

---

## 🔧 Uso no n8n

### **Webhook Method:**

**Node:** HTTP Request
```json
{
  "method": "POST",
  "url": "={{$env.SLACK_WEBHOOK_URL}}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "text": "📊 *Relatório Diário - {{$now.format('DD/MM/YYYY')}}*\n\n💰 Gasto Total: R$ {{$json.total_spend}}\n📈 Alcance: {{$json.total_reach}}\n👥 Novos Seguidores: {{$json.total_followers}}\n\n🤖 Insight IA:\n{{$json.ai_insight}}"
  }
}
```

### **OAuth Method:**

**Node:** Slack (oficial)
- Resource: `Message`
- Operation: `Send`
- Channel: `#marketing-metrics`
- Message Type: `Simple Text Message` ou `Blocks`

---

## 📝 Templates de Mensagem

### **Relatório Diário Simples:**

```json
{
  "text": "📊 *Relatório Diário - 18/10/2025*\n\n💰 Gasto: R$ 40,00\n📈 Alcance: 15.234 pessoas\n👥 Novos Seguidores: +12\n💵 Custo/Seguidor: R$ 3,33\n\n🤖 *Insight IA:*\nPerformance estável. CTR abaixo da meta (0,42% vs 1,5%). Recomendo pausar AD 03 e realocar budget para AD 02."
}
```

### **Alerta de Anomalia:**

```json
{
  "text": "⚠️ *ALERTA - Queda de Performance*\n\n🔴 CTR caiu 25% hoje (0,42% → 0,32%)\n🔴 CPC aumentou 30% (R$ 0,48 → R$ 0,62)\n\n🔍 *Possíveis Causas:*\n- Ad fatigue (frequência > 2,5)\n- Criativo perdendo eficácia\n- Mudança de algoritmo\n\n✅ *Ações Recomendadas:*\n1. Pausar ads de baixa performance\n2. Testar novos criativos\n3. Revisar segmentação"
}
```

### **Resumo Semanal:**

```json
{
  "text": "📈 *RESUMO SEMANAL - 11-17 Out*\n\n🎯 *Resultados:*\n• Gasto: R$ 280,00\n• Alcance: 85.432 pessoas\n• Novos Seguidores: +245\n• Custo/Seguidor: R$ 1,14 ✅\n\n📊 *Performance por Fonte:*\n• Meta Ads: +180 seguidores (R$ 1,05/seg)\n• Orgânico: +65 seguidores (R$ 0,00/seg)\n\n🏆 *Destaques:*\n• AD 02 superou meta (CTR 1,8%)\n• Stories geraram 45% do engajamento\n• Reels cresceram 30% em views\n\n📅 *Próxima Semana:*\n• Escalar AD 02 (+20% budget)\n• Pausar AD 03 (CTR 0,28%)\n• Testar 3 novos hooks"
}
```

---

## 🎨 Formatação Avançada (Blocks)

Para mensagens ricas com botões/imagens, use Blocks:

**Block Kit Builder:** https://app.slack.com/block-kit-builder

Exemplo:
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📊 Relatório Diário de Marketing"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Gasto:*\nR$ 40,00"
        },
        {
          "type": "mrkdwn",
          "text": "*Alcance:*\n15.234"
        },
        {
          "type": "mrkdwn",
          "text": "*CTR:*\n0,42%"
        },
        {
          "type": "mrkdwn",
          "text": "*Seguidores:*\n+12"
        }
      ]
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "🤖 *Insight IA:*\nPerformance estável. Recomendo otimizar hooks dos Reels para aumentar CTR."
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Ver Dashboard"
          },
          "url": "https://app.supabase.com/project/[id]/editor"
        }
      ]
    }
  ]
}
```

---

## 🔔 Alertas Recomendados

**Configure alertas para:**

1. **Diário (9h):**
   - Resumo de métricas do dia anterior
   - Comparação com média semanal

2. **Anomalias (tempo real):**
   - CTR cai >20%
   - CPC aumenta >30%
   - Frequência >2,5 (ad fatigue)
   - Erro em API (Meta Ads, Google, etc)

3. **Semanal (Segunda 10h):**
   - Resumo completo da semana
   - ROI calculado
   - Insights IA com recomendações

4. **Mensal (Dia 1, 10h):**
   - Relatório completo do mês
   - Comparação com meta
   - Projeção para próximo mês

---

## ✅ Checklist de Setup

- [ ] App Slack criado
- [ ] Webhook URL ou Bot Token obtido
- [ ] Canal `#marketing-metrics` criado
- [ ] Webhook testado com curl
- [ ] `.env` atualizado com credenciais
- [ ] Mensagem de teste recebida no Slack
- [ ] Templates de mensagem salvos

---

## 📞 Suporte

**Documentação Slack:**
- Webhook: https://api.slack.com/messaging/webhooks
- Block Kit: https://api.slack.com/block-kit
- OAuth: https://api.slack.com/authentication/oauth-v2

**Troubleshooting:**
- Webhook não funciona: Verificar URL completa sem espaços
- Mensagem não formata: Usar `mrkdwn` em blocks
- Erro 404: Webhook foi revogado, criar novo

---

**🎉 Slack configurado! Próximo: Criar workflows n8n**

