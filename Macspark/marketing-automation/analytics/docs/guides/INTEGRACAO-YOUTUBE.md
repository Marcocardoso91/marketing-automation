# Integração YouTube Analytics

**Tempo Estimado:** 10-15 minutos  
**Dificuldade:** Fácil  
**Custo:** Gratuito

---

## 🎯 Objetivo

Conectar **YouTube Data API v3** ao n8n para coletar métricas do canal (views, inscritos, watch time).

---

## 📋 Pré-requisitos

- ✅ Canal YouTube criado
- ✅ Conta Google com acesso ao canal
- ✅ n8n rodando

---

## 🔑 Passo 1: Obter Channel ID (2 min)

**Método 1: Via URL do Canal:**
- URL format: `youtube.com/channel/UCxxxxxxxxxxxxxxxxxx`
- O `UCxxxxxxxxxxxxxxxxxx` é seu Channel ID

**Método 2: Via YouTube Studio:**
1. Acesse: https://studio.youtube.com
2. **Settings** → **Channel** → **Advanced Settings**
3. Copie **"Channel ID"** (formato: `UCxxxxxxxxxxxxxxxxxx`)
4. ✅ Salve no `.env`:
   ```bash
   YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxx
   ```

---

## 🔐 Passo 2: Criar API Key (5 min)

1. **Google Cloud Console:**
   - https://console.cloud.google.com
   - Selecione projeto (ou use o mesmo do GA4/Google Ads)

2. **Ativar YouTube Data API v3:**
   - Menu **"APIs & Services"** → **"Library"**
   - Busque: `YouTube Data API v3`
   - Clique em **"Enable"**

3. **Criar API Key:**
   - **"APIs & Services"** → **"Credentials"**
   - **"Create Credentials"** → **"API key"**
   - ✅ Copie a key gerada: `AIzaSyxxxxxxxxxxxxxxxxxx`
   
4. **Restringir API Key (Segurança):**
   - Clique em **"Edit API key"**
   - **Application restrictions:** None (ou HTTP referrers se quiser)
   - **API restrictions:** Restrict key → Selecione **"YouTube Data API v3"**
   - Salve

5. **Adicionar ao `.env`:**
   ```bash
   YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxx
   ```

---

## 🔧 Passo 3: Configurar no n8n (3 min)

1. **Importar Workflow:**
   - n8n → **Import from File**
   - Arquivo: `n8n-workflows/youtube-supabase.json`

2. **Configurar Credential:**
   - Criar credential tipo **"YouTube OAuth2 API"**
   - OU usar API Key diretamente no node

3. **Testar:**
   - Execute workflow
   - ✅ Verificar estatísticas do canal

4. **Ativar:**
   - Toggle **"Active"** ON
   - ✅ Rodará diariamente às 9:30h

---

## 📊 Métricas Coletadas

### **Via Channel Statistics:**

| Métrica | Nome API | Descrição |
|---------|----------|-----------|
| **Views** | `statistics.viewCount` | Total de visualizações do canal |
| **Inscritos** | `statistics.subscriberCount` | Total de inscritos |
| **Vídeos** | `statistics.videoCount` | Total de vídeos publicados |

**⚠️ Limitação:** API básica retorna totais acumulados, não métricas diárias.

### **Para Métricas Diárias: YouTube Analytics API**

**Requer aprovação adicional:**

1. Ativar **"YouTube Analytics API"** (não "YouTube Data API v3")
2. Permite acessar:
   - Views por dia
   - Watch time
   - Taxa de retenção
   - Demografias

**Query exemplo:**
```
GET https://youtubeanalytics.googleapis.com/v2/reports
?ids=channel==MINE
&startDate=2025-10-17
&endDate=2025-10-17
&metrics=views,estimatedMinutesWatched,averageViewDuration,subscribersGained
&dimensions=day
```

---

## 🧮 Workaround para Métricas Diárias

Como a API básica retorna apenas totais, o workflow calcula **estimativas**:

```javascript
// No Code node do workflow:
const totalViews = parseInt(stats.viewCount);
const totalSubscribers = parseInt(stats.subscriberCount);

// Estimativa: ~1% das views são de ontem
const estimatedYesterdayViews = Math.round(totalViews * 0.01);

// Estimativa: ~0.1% dos inscritos são de ontem
const estimatedNewSubscribers = Math.round(totalSubscribers * 0.001);
```

**💡 Recomendação:** Para dados precisos, use YouTube Analytics API (aprovação necessária)

---

## 🛠️ Troubleshooting

### **Erro: "The request cannot be completed because you have exceeded your quota"**
- API Key tem quota diária (10.000 units)
- 1 request = ~3-5 units
- Solução: Reduzir frequência ou solicitar aumento de quota

### **Erro: "channel not found"**
- Verificar Channel ID (deve começar com UC)
- Testar no browser: `https://www.youtube.com/channel/UCxxxxxxxxxx`

### **API Key não funciona:**
- Verificar restrições (API restrictions devem incluir YouTube Data API v3)
- Regenerar key se necessário

---

## 📈 Melhorias Futuras

**Para dados mais precisos:**

1. **Solicitar YouTube Analytics API:**
   - Preencher formulário de audit/compliance
   - Justificativa: "Análise interna de performance"
   - Aprovação: 3-7 dias

2. **Usar YouTube Studio:**
   - Export manual de relatórios CSV
   - Importar no Supabase via script

3. **Scraping (não recomendado):**
   - Viola ToS do YouTube
   - Pode resultar em ban

---

## ✅ Checklist

- [ ] Channel ID obtido
- [ ] YouTube Data API v3 ativada
- [ ] API Key criada e restringida
- [ ] API Key testada (curl ou Postman)
- [ ] `.env` atualizado
- [ ] n8n workflow importado
- [ ] Teste executado
- [ ] Workflow ativado (9:30h diário)
- [ ] Dados no Supabase validados

---

**🎉 YouTube integrado!**

**Próximo:** `SETUP-APACHE-SUPERSET.md` (já criado)

