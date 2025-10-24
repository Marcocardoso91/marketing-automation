# 🚀 Primeiros Passos - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 🎯 O Que Fazer Após a Instalação

Parabéns! Você instalou com sucesso o Marketing Automation Platform. Agora vamos configurar tudo para começar a usar o sistema.

---

## ✅ Checklist de Validação

### 1. Verificar Saúde do Sistema

```powershell
# Executar health check
.\scripts\health-check.ps1
```

**Resultado esperado:**
```
✅ Agent API (http://localhost:8000)
✅ Metrics Endpoint (http://localhost:8000/api/v1/metrics/export)
✅ Superset (http://localhost:8088)
✅ Prometheus (http://localhost:9090)
```

### 2. Testar Coleta de Métricas

```powershell
# Testar coleta básica
cd analytics\scripts
python metrics-to-supabase.py
```

**Resultado esperado:**
```
✅ Conectado ao Supabase
✅ Coletando métricas do Facebook
✅ Salvando no Supabase
✅ Processo concluído com sucesso
```

---

## 🎨 Configurar Primeiro Dashboard

### 1. Acessar Superset

1. **Abrir:** http://localhost:8088
2. **Login:** 
   - Usuário: `admin`
   - Senha: `admin` (ou a senha configurada no docker-compose)

### 2. Conectar ao Supabase

1. **Data → Databases → + Database**
2. **SQLAlchemy URI:** 
   ```
   postgresql://postgres:password@host.docker.internal:5432/postgres
   ```
3. **Test Connection** → **Connect**

### 3. Criar Primeiro Dashboard

1. **Dashboards → + Dashboard**
2. **Nome:** "Marketing Overview"
3. **Adicionar Chart:**
   - **Dataset:** `campaigns` (tabela do Supabase)
   - **Chart Type:** "Line Chart"
   - **X-axis:** `date`
   - **Y-axis:** `spend`
   - **Filters:** Últimos 30 dias

### 4. Métricas Essenciais

**Charts recomendados:**
- **Spend Over Time** (Line Chart)
- **CTR by Campaign** (Bar Chart)
- **ROAS Distribution** (Histogram)
- **Top Performing Campaigns** (Table)

---

## 🤖 Criar Primeira Automação

### 1. Configurar N8N

1. **Acessar:** http://localhost:5678
2. **Criar conta** (primeira vez)
3. **Settings → Credentials → Add Credential**
   - **Facebook API:** Configurar token
   - **Supabase:** Configurar URL e chave

### 2. Importar Workflow Básico

1. **Workflows → Import from File**
2. **Selecionar:** `analytics/n8n-workflows/daily-metrics-collection.json`
3. **Configure credentials** nos nós
4. **Save & Activate**

### 3. Testar Workflow

1. **Execute Manual** → Verificar logs
2. **Verificar dados** no Superset
3. **Configurar schedule** (diário às 20h)

---

## 📊 Testar Fluxo End-to-End

### 1. Coleta Manual de Métricas

```powershell
# Via API
curl -X GET "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-20&date_until=2025-10-23" -H "X-API-Key: your_api_key"
```

### 2. Verificar Dados no Supabase

1. **Supabase Dashboard** → Table Editor
2. **Tabela:** `campaigns`
3. **Verificar:** Dados recentes aparecem

### 3. Visualizar no Superset

1. **Refresh dataset** no Superset
2. **Verificar charts** mostram dados
3. **Testar filtros** por data/campanha

---

## 🔔 Configurar Alertas Básicos

### 1. Alertas de Performance

**No N8N, criar workflow:**
- **Trigger:** Schedule (diário às 9h)
- **Action:** Verificar campanhas com CTR < 1%
- **Notification:** Email/Slack

### 2. Alertas de Orçamento

**Workflow para:**
- **Spend diário** > 80% do orçamento
- **CPA** > threshold configurado
- **Campanhas pausadas** inesperadamente

### 3. Configurar Notificações

**Slack Integration:**
1. **N8N → Credentials → Slack**
2. **Webhook URL:** Do seu workspace Slack
3. **Test message** para verificar

---

## 🎯 Próximos Passos Recomendados

### Semana 1: Configuração Básica
- [ ] ✅ Dashboard principal funcionando
- [ ] ✅ Coleta automática de métricas
- [ ] ✅ Alertas básicos configurados
- [ ] ✅ Teste de todos os endpoints da API

### Semana 2: Otimização
- [ ] **Criar dashboards específicos** por objetivo
- [ ] **Configurar automações avançadas** (pause/optimize)
- [ ] **Integrar Notion** para relatórios
- [ ] **Configurar backup** dos dados

### Semana 3: Automação Avançada
- [ ] **Workflows N8N complexos** (multi-step)
- [ ] **Integração com outras plataformas** (Google Ads, etc.)
- [ ] **Alertas inteligentes** baseados em IA
- [ ] **Relatórios automáticos** por email

### Semana 4: Produção
- [ ] **Monitoramento completo** (Prometheus + Grafana)
- [ ] **Backup e recovery** testados
- [ ] **Documentação da equipe** atualizada
- [ ] **Treinamento** dos usuários finais

---

## 🔧 Configurações Avançadas

### 1. Configurar Backup Automático

```powershell
# Script de backup diário
# Criar: scripts/backup-daily.ps1
```

### 2. Monitoramento com Prometheus

1. **Acessar:** http://localhost:9090
2. **Verificar métricas** da API
3. **Configurar alertas** no Grafana (se instalado)

### 3. Logs e Debugging

```powershell
# Ver logs em tempo real
docker-compose logs -f api

# Filtrar por erro
docker-compose logs api | Select-String "ERROR"
```

---

## 🆘 Problemas Comuns

### ❌ Superset Não Carrega
**Solução:** Aguardar 3-5 minutos (inicialização lenta)

### ❌ Dados Não Aparecem
**Solução:** 
1. Verificar coleta funcionando
2. Refresh dataset no Superset
3. Verificar credenciais Facebook

### ❌ N8N Workflow Falha
**Solução:**
1. Verificar credentials configuradas
2. Testar conexões individualmente
3. Verificar logs do workflow

---

## 📚 Recursos Adicionais

### Documentação Completa
- **User Guide:** [docs/USER-GUIDE.md](../../USER-GUIDE.md)
- **API Reference:** [docs/api/agent-api/API-REFERENCE.md](../api/agent-api/API-REFERENCE.md)
- **Troubleshooting:** [docs/reference/troubleshooting/TROUBLESHOOTING.md](../../reference/troubleshooting/TROUBLESHOOTING.md)

### Links Úteis
- **Swagger UI:** http://localhost:8000/docs
- **Superset:** http://localhost:8088
- **N8N:** http://localhost:5678
- **Prometheus:** http://localhost:9090

### Suporte
- **GitHub Issues:** [Criar issue](https://github.com/your-repo/issues)
- **Documentação:** [docs/INDEX.md](../../INDEX.md)

---

## ✅ Checklist Final

Após completar todos os passos, você deve ter:

- [ ] ✅ Sistema funcionando (health check OK)
- [ ] ✅ Dashboard principal no Superset
- [ ] ✅ Coleta automática de métricas
- [ ] ✅ Primeiro workflow N8N ativo
- [ ] ✅ Alertas básicos configurados
- [ ] ✅ Dados aparecendo nos dashboards
- [ ] ✅ API respondendo corretamente
- [ ] ✅ Logs sem erros críticos

**🎉 Parabéns! Seu Marketing Automation Platform está pronto para uso!**

---

**💡 Próximo passo:** Explore a [documentação completa](../../INDEX.md) para recursos avançados e personalizações.
