# 🚀 Guia de Instalação Rápida - Agente Facebook v3.0.0

## **Pré-requisitos**

- ✅ Python 3.12+
- ✅ Node.js 18+ (para n8n)
- ✅ Docker e Docker Compose (para Superset)
- ✅ Git

## **1. Clone o Repositório**

```bash
git clone <seu-repositorio>
cd "Agente Facebook"
```

## **2. Configurar Ambiente Python**

### 2.1 Criar Virtual Environment

```bash
python -m venv .venv
```

### 2.2 Ativar Virtual Environment

**Windows:**
```powershell
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 2.3 Instalar Dependências

```bash
cd scripts
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## **3. Configurar Variáveis de Ambiente**

### 3.1 Copiar Arquivo de Exemplo

```bash
cp scripts/env.example.txt .env
```

### 3.2 Preencher Credenciais Obrigatórias

Edite `.env` e configure:

```env
# OBRIGATÓRIO (P0)
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_KEY=sua-service-key-aqui
META_ACCESS_TOKEN=seu-token-meta-ads
META_AD_ACCOUNT_ID=act_1234567890

# OPCIONAL (P1/P2)
GA4_PROPERTY_ID=123456789
GOOGLE_ADS_CUSTOMER_ID=123-456-7890
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxx
YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3.3 Validar Configuração

```bash
python scripts/validate-env.py
```

Deve retornar:
```
✓ OK: Todas variaveis obrigatorias configuradas!
```

## **4. Configurar Supabase**

### 4.1 Criar Conta Supabase

1. Acesse https://supabase.com
2. Crie uma conta gratuita
3. Crie um novo projeto

### 4.2 Executar SQL de Setup

1. Abra o **SQL Editor** no Supabase
2. Copie todo o conteúdo de `SQL-PARA-SUPABASE.sql`
3. Cole e execute no editor
4. Verifique se a tabela `daily_metrics` foi criada

### 4.3 Testar Conexão

```bash
python test-supabase-connection.py
```

## **5. Configurar n8n (Opcional mas Recomendado)**

### 5.1 Instalar n8n

```bash
npm install -g n8n
```

### 5.2 Iniciar n8n

```bash
n8n start
```

Acesse: http://localhost:5678

### 5.3 Importar Workflows

1. Acesse **Workflows** → **Import from File**
2. Importe cada arquivo de `n8n-workflows/`:
   - `meta-ads-supabase.json`
   - `google-analytics-supabase.json`
   - `google-ads-supabase.json`
   - `youtube-supabase.json`
   - `consolidate-analyze-notify.json`

### 5.4 Configurar Credenciais

Para cada workflow, configure:
- **Supabase:** URL + Service Key
- **Meta Ads:** Access Token + Account ID
- **Google APIs:** OAuth2 ou API Key
- **OpenAI:** API Key
- **Slack:** Webhook URL

## **6. Executar Testes**

### 6.1 Testes Unitários

```bash
pytest tests/test_validate_env.py -v
```

### 6.2 Testes Completos (quando implementados)

```bash
pytest tests/ -v --cov=scripts --cov-report=html
```

### 6.3 Visualizar Coverage

```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

## **7. Executar Script Principal**

### 7.1 Coletar Métricas Manualmente

```bash
python scripts/metrics-to-supabase.py
```

### 7.2 Backup para Notion (se configurado)

```bash
python scripts/meta-to-notion.py
```

## **8. Configurar Apache Superset (Opcional)**

### 8.1 Iniciar com Docker Compose

```bash
docker-compose -f docker-compose.superset.yml up -d
```

### 8.2 Acessar Interface

Acesse: http://localhost:8088

**Credenciais padrão:**
- Username: `admin`
- Password: `admin`

### 8.3 Conectar ao Supabase

1. **Settings** → **Database Connections**
2. **+ Database**
3. Selecione **PostgreSQL**
4. Preencha:
   - Host: `db.seu-projeto.supabase.co`
   - Port: `5432`
   - Database: `postgres`
   - Username: `postgres`
   - Password: (sua senha do Supabase)

## **9. Configurar Slack (Opcional)**

### 9.1 Criar Webhook

1. Acesse https://api.slack.com/apps
2. Crie um novo App
3. Ative **Incoming Webhooks**
4. Adicione novo webhook ao workspace
5. Copie a URL do webhook

### 9.2 Testar

```bash
python test-slack-webhook.py
```

## **10. Validação Final**

### 10.1 Checklist de Validação

```bash
# Validar ambiente
python scripts/validate-env.py

# Testar conexão Supabase
python test-supabase-connection.py

# Testar Slack (se configurado)
python test-slack-webhook.py

# Executar testes
pytest tests/test_validate_env.py -v

# Verificar formatação
black scripts/ --check

# Coletar métricas
python scripts/metrics-to-supabase.py
```

### 10.2 Tudo OK? ✅

Se todos os comandos acima passaram, você está pronto para usar o sistema!

## **11. Próximos Passos**

1. **Configure n8n workflows** para automação completa
2. **Crie dashboards no Superset** para visualização
3. **Configure alertas no Slack** para monitoramento
4. **Agende execução diária** dos scripts (cron/Task Scheduler)
5. **Revise a documentação completa** em `docs/`

## **Troubleshooting**

### Problema: "Module not found"
**Solução:** Certifique-se de estar no virtual environment ativado

### Problema: "Supabase connection failed"
**Solução:** Verifique se a URL e Service Key estão corretas no `.env`

### Problema: "Meta Ads API error"
**Solução:** Verifique se o token tem as permissões corretas (ads_read)

### Problema: "Tests failing"
**Solução:** Execute `pip install -r scripts/requirements-dev.txt` novamente

## **Documentação Completa**

Para documentação detalhada, consulte:
- 📄 `README.md` - Visão geral do projeto
- 📄 `docs/prd/agente-facebook/PRD.pt-BR.md` - Especificação completa
- 📄 `docs/setup-*.md` - Guias de configuração específicos
- 📄 `RELATORIO-CORRECOES-v3.0.md` - Changelog e melhorias

## **Suporte**

Para dúvidas e suporte:
- 📧 Consulte a documentação em `docs/`
- 🐛 Reporte bugs no repositório
- 💬 Revise o `backlog.csv` para features futuras

---
**Versão:** 3.0.0  
**Última Atualização:** 18/10/2025  
**Status:** ✅ Produção
