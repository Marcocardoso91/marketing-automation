# Integração Google Ads

**Tempo Estimado:** 20-25 minutos  
**Dificuldade:** Média-Alta  
**Custo:** Gratuito

---

## 🎯 Objetivo

Conectar **Google Ads** ao n8n para coletar automaticamente métricas de campanhas (cliques, impressões, custo, conversões).

---

## 📋 Pré-requisitos

- ✅ Conta Google Ads ativa com campanhas
- ✅ Google Cloud Project criado (pode usar o mesmo do GA4)
- ✅ n8n rodando

---

## 🔑 Passo 1: Obter Customer ID (2 min)

1. Acesse: https://ads.google.com
2. No canto superior direito, veja o Customer ID (formato: `123-456-7890`)
3. ✅ Salve no `.env`:
   ```bash
   GOOGLE_ADS_CUSTOMER_ID=123-456-7890
   ```

---

## 🔐 Passo 2: Obter Developer Token (5 min)

1. No Google Ads, clique em **"Tools & Settings"** (ícone chave inglesa)
2. **Setup** → **API Center**
3. Se não tiver Developer Token:
   - Preencha formulário de solicitação
   - ⏳ Aprovação pode levar 24h
4. ✅ Copie o **Developer Token** quando aprovado
5. Salve no `.env`:
   ```bash
   GOOGLE_ADS_DEVELOPER_TOKEN=xxxxxxxxxxxxxx
   ```

**💡 Dica:** Para testes, use `insert_test_customer_id` (sem aprovação necessária)

---

## 🔑 Passo 3: Configurar OAuth2 (5 min)

**Use as mesmas credenciais do Google Analytics:**

1. Google Cloud Console → **"APIs & Services"** → **"Library"**
2. Busque e ative: **"Google Ads API"**
3. Usar Client ID e Client Secret já criados para GA4
4. Adicionar scope adicional:
   ```
   https://www.googleapis.com/auth/adwords
   ```

---

## 🔧 Passo 4: Configurar no n8n (5 min)

1. **Credentials:**
   - n8n → **Credentials** → **"Google Ads OAuth2 API"**
   - Pode reutilizar a credential do Google (adicionar scope)

2. **Importar Workflow:**
   - **Import from File**: `n8n-workflows/google-ads-supabase.json`

3. **Configurar Node:**
   - **Customer ID:** `={{$env.GOOGLE_ADS_CUSTOMER_ID}}`
   - **Date Range:** `YESTERDAY`
   - **Fields:** (já configurado)

4. **Testar:**
   - Execute workflow manualmente
   - ✅ Verificar dados no Supabase

---

## 📊 Métricas Coletadas

| Métrica | Nome API | Descrição |
|---------|----------|-----------|
| **Cliques** | `metrics.clicks` | Total de cliques nos anúncios |
| **Impressões** | `metrics.impressions` | Vezes que anúncio foi exibido |
| **Custo** | `metrics.cost_micros` | Valor gasto (em micros, /1M) |
| **CTR** | `metrics.ctr` | Click-through rate |
| **CPC Médio** | `metrics.average_cpc` | Custo médio por clique |
| **Conversões** | `metrics.conversions` | Ações valiosas (compra, lead, etc) |
| **Custo/Conversão** | `metrics.cost_per_conversion` | ROI da conversão |

---

## 🎯 Queries Úteis (Google Ads Query Language)

### **Campanhas Ativas (Últimos 7 dias):**

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  metrics.clicks,
  metrics.impressions,
  metrics.cost_micros,
  metrics.ctr,
  metrics.conversions
FROM campaign
WHERE
  campaign.status = 'ENABLED'
  AND segments.date DURING LAST_7_DAYS
ORDER BY metrics.clicks DESC
```

### **Performance por Grupo de Anúncios:**

```sql
SELECT
  ad_group.name,
  metrics.clicks,
  metrics.impressions,
  metrics.ctr,
  metrics.average_cpc
FROM ad_group
WHERE
  segments.date = YESTERDAY
ORDER BY metrics.clicks DESC
LIMIT 10
```

---

## 🛠️ Troubleshooting

### **Erro: "developer token is not approved"**
- Solução: Aguardar aprovação Google (24-48h)
- Alternativa: Usar test account temporariamente

### **Erro: "customer not found"**
- Solução: Verificar formato Customer ID (com hífens: 123-456-7890)

### **Erro: "permission denied"**
- Solução: Adicionar scope `https://www.googleapis.com/auth/adwords` no OAuth2

### **Custo em "micros":**
- Google Ads retorna valores em micros (1/1.000.000)
- Dividir por 1.000.000 para obter valor real
- Exemplo: `cost_micros: 50000000` = R$ 50,00

---

## ✅ Checklist

- [ ] Customer ID obtido
- [ ] Developer Token solicitado/aprovado
- [ ] Google Ads API ativada no Cloud Console
- [ ] OAuth2 credentials configuradas (ou reutilizadas do GA4)
- [ ] n8n workflow importado
- [ ] Teste executado com sucesso
- [ ] Workflow ativado (diário 9:15h)
- [ ] Dados aparecem no Supabase

---

**🎉 Google Ads integrado!**

**Próximo:** `INTEGRACAO-YOUTUBE.md`

