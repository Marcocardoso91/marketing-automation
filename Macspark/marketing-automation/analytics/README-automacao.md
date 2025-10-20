# 🤖 Automação Meta Ads → Notion

## Visão Geral

Sistema de automação para coletar métricas do Meta Ads Manager e adicionar automaticamente no Notion, eliminando trabalho manual diário.

---

## 🎯 O Que Foi Criado

### 1. Workflow N8n
- **Arquivo:** `n8n-workflows/meta-ads-notion.json`
- **Função:** Busca métricas diariamente às 9h
- **Destino:** Database "Métricas & KPIs Diários" no Notion
- **Status:** ✅ Pronto para importar

### 2. Script Python Backup
- **Arquivo:** `scripts/meta-to-notion.py`
- **Função:** Mesmo que N8n, mas executável manualmente
- **Uso:** Caso N8n falhe
- **Status:** ✅ Pronto para usar

### 3. Documentação Completa
- **Setup N8n:** `docs/setup-n8n-meta-ads.md`
- **Guia Screenshots:** `docs/screenshots-guide.md`
- **Status:** ✅ Passo a passo completo

### 4. Páginas Notion (Importar)
- **Dashboard Campanhas:** `notion-pages/dashboard-campanhas-ativas.md`
- **Template Manual:** `notion-pages/template-metricas-manuais.md`
- **Status:** ✅ Prontas para importar

---

## 🚀 Como Começar

### Opção A: Automação Completa (Recomendado)

**Tempo:** ~40 minutos setup inicial

1. **Configurar Credenciais:**
   - Seguir: `docs/setup-n8n-meta-ads.md`
   - Obter tokens do Meta e Notion
   - Tempo: 20 min

2. **Importar Workflow no N8n:**
   - Abrir https://n8n.macspark.dev
   - Importar `n8n-workflows/meta-ads-notion.json`
   - Configurar credenciais
   - Tempo: 10 min

3. **Testar:**
   - Executar workflow manualmente
   - Verificar dados no Notion
   - Ativar schedule
   - Tempo: 10 min

4. **Pronto!**
   - Métricas coletadas automaticamente todo dia
   - Trabalho zero

---

### Opção B: Script Python

**Tempo:** ~30 minutos setup + 2 min/dia execução

1. **Instalar Python:**
   ```bash
   # Verificar se tem Python
   python --version
   ```

2. **Configurar:**
   ```bash
   cd scripts
   pip install -r requirements.txt
   cp env.example.txt .env
   # Editar .env com seus tokens
   ```

3. **Executar:**
   ```bash
   python meta-to-notion.py
   ```

4. **Agendar (opcional):**
   - Windows: Task Scheduler
   - Linux/Mac: Cron job

---

### Opção C: Manual (Sem Automação)

**Tempo:** 3-5 min/dia

1. Seguir template: `notion-pages/template-metricas-manuais.md`
2. Copiar dados do Ads Manager
3. Adicionar no Notion
4. Simples e funcional

---

## 📁 Estrutura de Arquivos

```
Agente Facebook/
├── n8n-workflows/
│   ├── meta-ads-notion.json        ← Workflow N8n
│   └── README.md
├── docs/
│   ├── setup-n8n-meta-ads.md       ← Guia setup completo
│   └── screenshots-guide.md        ← Como tirar prints
├── scripts/
│   ├── meta-to-notion.py           ← Script Python
│   ├── requirements.txt
│   ├── env.example.txt             ← Template variáveis
│   └── README.md
├── notion-pages/
│   ├── dashboard-campanhas-ativas.md  ← Importar no Notion
│   └── template-metricas-manuais.md   ← Importar no Notion
└── README-automacao.md             ← Este arquivo
```

---

## 🔑 Credenciais Necessárias

### Meta Ads API:
- **Access Token:** Token de longa duração (60 dias)
- **Ad Account ID:** Formato `act_123456789`
- **Permissões:** `ads_read`, `ads_management`

### Notion API:
- **Integration Token:** Começa com `secret_`
- **Database ID:** `e344b2ff2ded4418b93413b9dbd2e131`
- **Permissões:** Read + Write no database

### Como Obter:
Ver guia completo: `docs/setup-n8n-meta-ads.md`

---

## 📊 Métricas Coletadas Automaticamente

### Do Meta Ads API:
- Gasto total (R$)
- Alcance
- Impressões
- Cliques
- CTR (%)
- CPC (R$)
- CPE (R$)
- Frequência
- Conversões (seguidores)

### Calculadas Automaticamente:
- Custo por Seguidor
- CTR médio
- Performance vs metas
- Alertas (🟢🟡🔴)

### Adicionadas no Notion:
- Todos campos do database "Métricas & KPIs Diários"
- Nota automática identificando fonte (N8n ou Script)

---

## ⚙️ Configurações do N8n

### Schedule:
- **Frequência:** Diário
- **Horário:** 9h da manhã
- **Timezone:** America/Sao_Paulo
- **Dias:** Segunda a Domingo

### Nodes do Workflow:
1. **Schedule Trigger** - Dispara diariamente
2. **Facebook Graph API** - Busca métricas
3. **Code (JavaScript)** - Processa e agrega dados
4. **Notion API** - Cria registro no database

### Dados Processados:
- Soma métricas de todas campanhas ativas
- Calcula médias (CTR, Frequência)
- Calcula custos derivados
- Formata para Notion

---

## 🔧 Manutenção

### Renovar Token Meta (A cada 50 dias):
1. Seguir Passo 1.4 do guia setup
2. Atualizar token no N8n
3. Testar workflow

### Verificar Execuções (Semanalmente):
1. Abrir N8n > Executions
2. Ver se todas execuções estão ✅ verde
3. Se houver erro ❌, investigar

### Backup (Mensal):
1. Exportar workflow do N8n
2. Salvar JSON em `n8n-workflows/backup/`
3. Commit no Git

---

## 📞 Suporte

### Documentação:
- Setup N8n: `docs/setup-n8n-meta-ads.md`
- Screenshots: `docs/screenshots-guide.md`
- Scripts: `scripts/README.md`

### APIs:
- Meta Ads API: https://developers.facebook.com/docs/marketing-api
- Notion API: https://developers.notion.com
- N8n Docs: https://docs.n8n.io

### Troubleshooting:
- Ver seção completa em: `docs/setup-n8n-meta-ads.md`

---

## ✅ Próximos Passos

### Imediato:
1. [ ] Escolher método (N8n / Script / Manual)
2. [ ] Seguir guia de setup
3. [ ] Testar primeira execução
4. [ ] Verificar dados no Notion

### Depois:
1. [ ] Deixar rodar automaticamente
2. [ ] Verificar logs semanalmente
3. [ ] Ajustar se necessário

---

## 🎁 Bônus

### Páginas para Importar no Notion:
1. `notion-pages/dashboard-campanhas-ativas.md` - Dashboard visual
2. `notion-pages/template-metricas-manuais.md` - Backup manual

**Como importar:**
1. Abrir Notion
2. Criar nova página
3. Colar conteúdo do arquivo .md
4. Formatar se necessário

---

**Criado:** 18 de Outubro, 2025
**Versão:** 1.0
**Autor:** Agente IA via Cursor

