# 📊 Guia de Integração - Google Analytics 4

**Versão:** 1.0.0  
**Última Atualização:** 18/10/2025  
**Tempo Estimado:** 45 minutos

---

## 📋 Pré-requisitos

- ✅ Conta Google Analytics 4 ativa
- ✅ Propriedade GA4 criada e configurada
- ✅ Acesso de Administrador à propriedade
- ✅ Google Cloud Project criado
- ✅ Python 3.12+ instalado
- ✅ n8n instalado (opcional, mas recomendado)

---

## 🎯 Objetivo

Integrar Google Analytics 4 para coletar automaticamente:
- 📈 Sessões e usuários
- 🔍 Visualizações de página
- ⏱️ Tempo médio na página
- 📱 Dispositivos e navegadores
- 🌍 Localização geográfica
- 🎯 Eventos personalizados

---

## 📝 Passo 1: Configurar Google Cloud Project

### 1.1 Criar Projeto (se não existe)

1. Acesse https://console.cloud.google.com
2. Clique em **Select a project** → **New Project**
3. Nome: `Agente Facebook Marketing`
4. Clique em **Create**

### 1.2 Ativar Google Analytics Data API

1. No menu lateral, vá em **APIs & Services** → **Library**
2. Busque por `Google Analytics Data API`
3. Clique em **Enable**
4. Aguarde ativação (1-2 minutos)

### 1.3 Criar Service Account

1. Vá em **APIs & Services** → **Credentials**
2. Clique em **+ CREATE CREDENTIALS** → **Service Account**
3. Preencha:
   - **Service account name:** `ga4-data-collector`
   - **Service account ID:** (auto-preenchido)
   - **Description:** `Coleta de dados do GA4 para análise`
4. Clique em **CREATE AND CONTINUE**
5. Role: Selecione **Project** → **Viewer**
6. Clique em **CONTINUE** → **DONE**

### 1.4 Gerar Chave JSON

1. Na lista de Service Accounts, clique no email da conta criada
2. Vá na aba **KEYS**
3. Clique em **ADD KEY** → **Create new key**
4. Selecione **JSON**
5. Clique em **CREATE**
6. **IMPORTANTE:** Salve o arquivo `.json` em local seguro
7. Renomeie para `ga4-credentials.json`

---

## 📝 Passo 2: Configurar Acesso ao GA4

### 2.1 Obter Property ID

1. Acesse https://analytics.google.com
2. Vá em **Admin** (canto inferior esquerdo)
3. Em **Property**, clique na propriedade desejada
4. Clique em **Property Settings**
5. Copie o **PROPERTY ID** (formato: `123456789`)

### 2.2 Adicionar Service Account ao GA4

1. No **Admin**, vá em **Property Access Management**
2. Clique em **+** (Add users)
3. Cole o email da Service Account (ex: `ga4-data-collector@project-id.iam.gserviceaccount.com`)
4. Role: Selecione **Viewer**
5. Clique em **Add**

---

## 📝 Passo 3: Configurar Variáveis de Ambiente

### 3.1 Atualizar .env

Adicione ao arquivo `.env`:

```env
# Google Analytics 4
GA4_PROPERTY_ID=123456789
GOOGLE_APPLICATION_CREDENTIALS=./ga4-credentials.json
```

### 3.2 Mover Credenciais

```bash
# Copiar arquivo JSON para a raiz do projeto
cp ~/Downloads/ga4-credentials.json .
```

### 3.3 Validar Configuração

```bash
python scripts/validate-env.py
```

---

## 📝 Passo 4: Instalar Dependências Python

### 4.1 Atualizar requirements.txt

Adicione ao `scripts/requirements.txt`:

```txt
google-analytics-data==0.17.1
google-auth==2.23.4
google-api-python-client==2.108.0
```

### 4.2 Instalar

```bash
cd scripts
pip install -r requirements.txt
```

---

## 📝 Passo 5: Testar Conexão (Python)

### 5.1 Criar Script de Teste

Crie `scripts/test-ga4-connection.py`:

```python
#!/usr/bin/env python3
"""Testar conexão com Google Analytics 4"""

import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

def test_ga4_connection():
    """Testa conexão e coleta básica do GA4"""
    property_id = os.getenv("GA4_PROPERTY_ID")
    
    if not property_id:
        print("❌ GA4_PROPERTY_ID não configurado no .env")
        return False
    
    try:
        # Inicializar cliente
        client = BetaAnalyticsDataClient()
        
        # Request básico: usuários dos últimos 7 dias
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
            ],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )
        
        # Executar
        response = client.run_report(request)
        
        # Mostrar resultados
        print("✅ Conexão GA4 OK!")
        print(f"\n📊 Dados coletados dos últimos 7 dias:")
        
        for row in response.rows:
            date = row.dimension_values[0].value
            users = row.metric_values[0].value
            sessions = row.metric_values[1].value
            print(f"   {date}: {users} usuários, {sessions} sessões")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_ga4_connection()
    exit(0 if success else 1)
```

### 5.2 Executar Teste

```bash
python scripts/test-ga4-connection.py
```

**Resultado esperado:**
```
✅ Conexão GA4 OK!

📊 Dados coletados dos últimos 7 dias:
   20251012: 1234 usuários, 2345 sessões
   20251013: 1456 usuários, 2567 sessões
   ...
```

---

## 📝 Passo 6: Configurar Workflow n8n

### 6.1 Importar Workflow

1. Abra n8n: http://localhost:5678
2. Clique em **Workflows** → **Import from File**
3. Selecione `n8n-workflows/google-analytics-supabase.json`

### 6.2 Configurar Credenciais

1. Clique no nó **Google Analytics**
2. Em **Credentials**, clique em **Create New**
3. Preencha:
   - **Name:** `GA4 Service Account`
   - **Email:** (da Service Account)
   - **Private Key:** (copie do arquivo JSON, campo `private_key`)
4. Clique em **Save**

### 6.3 Configurar Property ID

1. No nó **Google Analytics**, configure:
   - **Property ID:** `123456789` (seu Property ID)
   - **Start Date:** `yesterday`
   - **End Date:** `today`

### 6.4 Testar Workflow

1. Clique em **Execute Workflow**
2. Verifique se dados são coletados
3. Confira se Supabase recebe os dados

---

## 📝 Passo 7: Métricas Recomendadas

### 7.1 Métricas de Usuários
- `activeUsers` - Usuários ativos
- `newUsers` - Novos usuários
- `totalUsers` - Total de usuários
- `userEngagementDuration` - Tempo de engajamento

### 7.2 Métricas de Sessões
- `sessions` - Total de sessões
- `sessionsPerUser` - Sessões por usuário
- `averageSessionDuration` - Duração média da sessão
- `bounceRate` - Taxa de rejeição

### 7.3 Métricas de Eventos
- `eventCount` - Total de eventos
- `conversions` - Conversões
- `screenPageViews` - Visualizações de página

### 7.4 Dimensões Úteis
- `date` - Data
- `deviceCategory` - Tipo de dispositivo
- `country` - País
- `city` - Cidade
- `browser` - Navegador
- `operatingSystem` - Sistema operacional

---

## 🔧 Troubleshooting

### Problema: "Permission denied"
**Solução:** Verifique se a Service Account tem permissão de Viewer no GA4

### Problema: "Property not found"
**Solução:** Confirme se o Property ID está correto (apenas números)

### Problema: "Invalid credentials"
**Solução:** Gere uma nova chave JSON para a Service Account

### Problema: "API not enabled"
**Solução:** Ative o Google Analytics Data API no Google Cloud Console

---

## ✅ Checklist de Validação

- [ ] Google Cloud Project criado
- [ ] Google Analytics Data API ativada
- [ ] Service Account criada
- [ ] Chave JSON baixada
- [ ] Property ID copiado
- [ ] Service Account adicionada ao GA4
- [ ] Variáveis de ambiente configuradas
- [ ] Dependências Python instaladas
- [ ] Teste de conexão passou
- [ ] Workflow n8n configurado
- [ ] Dados sendo coletados no Supabase

---

## 📚 Recursos Adicionais

- 📖 [Documentação Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)
- 📖 [Guia de Métricas e Dimensões](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- 🎥 [Tutorial em Vídeo](https://www.youtube.com/watch?v=xxx)
- 💬 [Suporte Google Analytics](https://support.google.com/analytics)

---

## 🔜 Próximos Passos

1. Configure **Google Ads** (`INTEGRACAO-GOOGLE-ADS.md`)
2. Configure **YouTube** (`INTEGRACAO-YOUTUBE.md`)
3. Teste integração completa end-to-end
4. Crie dashboards no Superset

---

**Dúvidas?** Consulte `GUIA-INSTALACAO-RAPIDA.md` ou abra uma issue no repositório.