# Índice Mestre - Marketing Automation Platform

Guia de navegação completo da documentação.

## 🚀 Início Rápido

| Documento | Descrição | Tempo |
|-----------|-----------|-------|
| [QUICK-START.md](QUICK-START.md) | Guia rápido de 15 minutos | 15 min |
| [README.md](README.md) | Visão geral do projeto | 10 min |
| [INTEGRATION-SUMMARY.md](INTEGRATION-SUMMARY.md) | Resumo executivo da integração | 5 min |

## 📖 Documentação Técnica

### Integração

| Documento | Conteúdo |
|-----------|----------|
| [docs/INTEGRATION-GUIDE.md](docs/INTEGRATION-GUIDE.md) | Como a integração funciona |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Arquitetura detalhada |
| [MIGRATION.md](MIGRATION.md) | Como migrar dos projetos antigos |

### Operacional

| Documento | Conteúdo |
|-----------|----------|
| [VALIDATION-CHECKLIST.md](VALIDATION-CHECKLIST.md) | Checklist de validação |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de mudanças |
| [env.template](env.template) | Template de configuração |

## 🔧 Scripts

| Script | Função | Como usar |
|--------|--------|-----------|
| `scripts/setup.ps1` | Setup inicial automatizado | `.\scripts\setup.ps1` |
| `scripts/health-check.ps1` | Verificar saúde dos serviços | `.\scripts\health-check.ps1` |
| `scripts/validate-integration.py` | Validar integração | `python scripts\validate-integration.py` |

## 📁 Estrutura de Pastas

```
marketing-automation/
├── api/                          # Agent API (FastAPI)
│   ├── src/api/metrics.py       # ⭐ NOVO: Endpoint de exportação
│   ├── main.py                   # ⭐ MODIFICADO: Registra metrics router
│   └── requirements.txt          # ⭐ MODIFICADO: + slowapi
│
├── analytics/                    # Analytics (Python + n8n)
│   ├── scripts/
│   │   ├── metrics-to-supabase.py    # ⭐ MODIFICADO: Usa AgentAPIClient
│   │   ├── env.example.txt           # ⭐ MODIFICADO: + AGENT_API_URL
│   │   └── requirements.txt          # ⭐ MODIFICADO: + shared package
│   └── n8n-workflows/
│       └── meta-ads-supabase.json    # ⭐ MODIFICADO: HTTP Request node
│
├── shared/                       # ⭐ NOVO: Pacote compartilhado
│   ├── marketing_shared/
│   │   ├── schemas/
│   │   │   └── facebook_metrics.py   # Schemas Pydantic
│   │   └── utils/
│   │       └── api_client.py         # Cliente HTTP
│   └── pyproject.toml
│
├── docs/                         # ⭐ NOVO: Documentação integrada
│   ├── INTEGRATION-GUIDE.md
│   └── ARCHITECTURE.md
│
├── tests/integration/            # ⭐ NOVO: Testes de integração
│   └── test_api_integration.py
│
├── scripts/                      # ⭐ NOVO: Scripts de automação
│   ├── setup.ps1
│   ├── health-check.ps1
│   └── validate-integration.py
│
├── .github/workflows/            # ⭐ NOVO: CI/CD
│   └── ci-integration.yml
│
├── docker-compose.integrated.yml # ⭐ NOVO: Stack completo
├── README.md                     # ⭐ NOVO: Docs principal
├── QUICK-START.md                # ⭐ NOVO: Início rápido
├── INTEGRATION-SUMMARY.md        # ⭐ NOVO: Resumo executivo
├── VALIDATION-CHECKLIST.md       # ⭐ NOVO: Checklist
├── MIGRATION.md                  # ⭐ NOVO: Guia de migração
├── CHANGELOG.md                  # ⭐ NOVO: Histórico
└── INDEX.md                      # ⭐ Este arquivo
```

⭐ = Arquivos novos ou modificados pela integração

## 🎯 Por Caso de Uso

### "Quero entender a integração"
1. [INTEGRATION-SUMMARY.md](INTEGRATION-SUMMARY.md)
2. [docs/INTEGRATION-GUIDE.md](docs/INTEGRATION-GUIDE.md)
3. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

### "Quero começar a usar agora"
1. [QUICK-START.md](QUICK-START.md)
2. Execute: `.\scripts\setup.ps1`
3. Execute: `docker-compose -f docker-compose.integrated.yml up -d`

### "Estou migrando dos projetos antigos"
1. [MIGRATION.md](MIGRATION.md)
2. [VALIDATION-CHECKLIST.md](VALIDATION-CHECKLIST.md)
3. Execute: `python scripts\validate-integration.py`

### "Quero desenvolver/contribuir"
1. [README.md](README.md) seção Desenvolvimento
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. `.github/workflows/ci-integration.yml`

### "Preciso fazer troubleshooting"
1. [docs/INTEGRATION-GUIDE.md](docs/INTEGRATION-GUIDE.md) seção Troubleshooting
2. [README.md](README.md) seção Troubleshooting
3. Execute: `.\scripts\health-check.ps1`

## 📊 Componentes Principais

### Agent API
- **Localização:** `api/`
- **Função:** API REST + Automação Meta Ads
- **Novo:** Endpoint `/api/v1/metrics/export`
- **Docs:** http://localhost:8000/docs

### Analytics
- **Localização:** `analytics/`
- **Função:** Coleta multi-canal + Dashboards
- **Modificado:** Busca Meta Ads do Agent API
- **Workflows:** `n8n-workflows/*.json`

### Shared
- **Localização:** `shared/`
- **Função:** Código compartilhado
- **Instalação:** `pip install -e ./shared`
- **Import:** `from marketing_shared.*`

## 🔑 Credenciais Necessárias

| Credencial | Obrigatória? | Onde obter |
|------------|--------------|------------|
| FACEBOOK_ACCESS_TOKEN | ✅ Sim | developers.facebook.com |
| FACEBOOK_AD_ACCOUNT_ID | ✅ Sim | business.facebook.com |
| ANALYTICS_API_KEY | ✅ Sim | Gere com script |
| SECRET_KEY | ✅ Sim | Gere com script |
| SUPABASE_URL | ⚠️  Recomendado | supabase.com |
| SLACK_WEBHOOK_URL | ⚠️  Opcional | api.slack.com |
| OPENAI_API_KEY | ⚠️  Opcional | platform.openai.com |

## 🧪 Testes

```bash
# Validação de integração
python scripts\validate-integration.py

# Testes unitários (Agent API)
cd api
pytest tests/ -v

# Testes unitários (Analytics)
cd analytics
pytest tests/ -v

# Testes de integração
pytest tests/integration/ -v
```

## 📞 Comandos Úteis

```powershell
# Ver logs
docker-compose -f docker-compose.integrated.yml logs -f

# Parar tudo
docker-compose -f docker-compose.integrated.yml down

# Restart um serviço
docker restart marketing-agent-api

# Ver status
docker-compose -f docker-compose.integrated.yml ps

# Limpar tudo (cuidado!)
docker-compose -f docker-compose.integrated.yml down -v
```

## 🎓 Ordem de Leitura Recomendada

Para novos usuários:

1. **[QUICK-START.md](QUICK-START.md)** - Comece aqui! ⭐
2. **[README.md](README.md)** - Visão geral
3. **[INTEGRATION-SUMMARY.md](INTEGRATION-SUMMARY.md)** - O que foi feito
4. **[docs/INTEGRATION-GUIDE.md](docs/INTEGRATION-GUIDE.md)** - Como funciona
5. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura detalhada
6. **[VALIDATION-CHECKLIST.md](VALIDATION-CHECKLIST.md)** - Validar setup

Para desenvolvedores:

1. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**
2. **[README.md](README.md)** seção Desenvolvimento
3. **Código em `shared/marketing_shared/`**
4. **Código em `api/src/api/metrics.py`**
5. **Testes em `tests/integration/`**

---

**Atualizado:** 2025-10-18  
**Versão:** 1.0.0  
**Total de documentos:** 15+

