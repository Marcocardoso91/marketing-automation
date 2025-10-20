# 🎯 START HERE - Facebook Ads AI Agent

**Bem-vindo ao projeto Facebook Ads AI Agent!**

Este documento é seu **ponto de entrada** para todo o projeto.

---

## ⚡ EXECUÇÃO RÁPIDA (5 minutos)

```bash
# 1. Configure credenciais
cp .env.example .env
# Edite .env com suas credenciais Facebook

# 2. Inicie stack Docker
docker-compose up -d

# 3. Acesse Swagger UI
# http://localhost:8000/docs
```

**Pronto!** Sua API está rodando 🚀

---

## 📚 DOCUMENTAÇÃO POR OBJETIVO

### 🏃 "Quero rodar o projeto AGORA"
➡️ **[COMO-EXECUTAR.md](COMO-EXECUTAR.md)** (5 min)
- Instruções passo-a-passo
- Sem Docker e com Docker
- Testes rápidos
- Troubleshooting

### 📊 "Quero entender o status do projeto"
➡️ **[STATUS-PROJETO.md](STATUS-PROJETO.md)** (10 min)
- O que está implementado
- O que falta fazer
- Estatísticas
- Próximos passos

### 📋 "Quero ver detalhes da implementação"
➡️ **[IMPLEMENTACAO-COMPLETA.md](IMPLEMENTACAO-COMPLETA.md)** (15 min)
- Todos os 6 sprints detalhados
- Arquivos criados por sprint
- Como usar cada componente

### 🎉 "Quero ver o sumário final"
➡️ **[SUMMARY-FINAL.md](SUMMARY-FINAL.md)** (10 min)
- Estatísticas gerais
- Conquistas
- Próximas ações
- Validação

### 🏗️ "Quero entender a arquitetura"
➡️ **[docs/auditoria/ARCHITECTURE-BLUEPRINT.md](docs/auditoria/ARCHITECTURE-BLUEPRINT.md)** (45 min)
- 12 diagramas Mermaid
- Fluxos de dados
- Modelo de dados
- Stack tecnológica

### 📖 "Quero ler a auditoria completa"
➡️ **[README-AUDITORIA.md](README-AUDITORIA.md)** (15 min)
- Resumo executivo da auditoria
- Gaps identificados
- Plano de 8 semanas
- ROI e investimento

### 🚀 "Quero fazer deploy em produção"
➡️ **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** (30 min)
- Provisioning VPS
- Configuração DNS
- Deploy com Traefik
- SSL automático

### 🆘 "Preciso resolver um problema"
➡️ **[docs/RUNBOOK.md](docs/RUNBOOK.md)** (conforme necessário)
- Procedimentos de emergência
- Troubleshooting
- Rollback
- Comandos úteis

### 🔧 "Quero configurar n8n"
➡️ **[docs/n8n-setup.md](docs/n8n-setup.md)** (20 min)
- Importar workflows
- Configurar credentials
- Testar alertas

---

## 📂 ESTRUTURA DE DOCUMENTOS

```
📚 DOCUMENTAÇÃO
│
├── 🚀 EXECUÇÃO
│   ├── START-HERE.md (você está aqui)
│   ├── COMO-EXECUTAR.md
│   └── README.md
│
├── 📊 STATUS
│   ├── STATUS-PROJETO.md
│   ├── IMPLEMENTACAO-COMPLETA.md
│   ├── SUMMARY-FINAL.md
│   ├── CHANGELOG.md
│   └── INDICE-COMPLETO.md
│
├── 📋 AUDITORIA (docs/auditoria/)
│   ├── INDEX-AUDITORIA.md
│   ├── README-AUDITORIA.md (resumo executivo)
│   ├── AUDIT-REPORT-TECNICO.md (análise completa)
│   ├── ARCHITECTURE-BLUEPRINT.md (diagramas)
│   ├── PLANO-EXECUCAO-SPRINTS.md (cronograma)
│   ├── GAPS-E-RECOMENDACOES.md (gaps)
│   └── QUICK-START-GUIDE.md (tutorial)
│
├── 🔧 OPERACIONAL (docs/)
│   ├── RUNBOOK.md (emergências)
│   ├── DEPLOYMENT.md (deploy)
│   ├── n8n-setup.md (n8n)
│   └── GUIA-COMPLETO-TESTES-CICD.md
│
└── 📖 PRD ORIGINAL (docs/prd/facebook-ads-agent/)
    ├── PRD.en-US.md
    ├── decisions.md (ADRs)
    ├── backlog.csv
    ├── coerencia.md
    └── system-map.md
```

---

## 🎬 PRIMEIROS PASSOS

### 1. Executar Localmente (Recomendado)

```bash
# Configure .env
cp .env.example .env
# Edite .env com credenciais Facebook

# Inicie Docker
docker-compose up -d

# Acesse Swagger
# http://localhost:8000/docs
```

### 2. Explorar Código

```bash
# Ver estrutura
tree src/ -L 2

# Principais arquivos:
# main.py - Entry point FastAPI
# src/agents/facebook_agent.py - Agente principal
# src/api/campaigns.py - Router de campanhas
# src/analytics/performance_analyzer.py - Análise de performance
```

### 3. Ler Documentação

```bash
# Ordem recomendada:
1. README.md
2. COMO-EXECUTAR.md
3. STATUS-PROJETO.md
4. docs/RUNBOOK.md
```

---

## 🎯 PERGUNTAS FREQUENTES

### "O projeto funciona?"
✅ **SIM!** A aplicação FastAPI roda e responde em `http://localhost:8000`

### "Posso testar sem credenciais Facebook?"
⚠️ **Parcialmente.** Os endpoints /health e / funcionam, mas endpoints de campaigns/analytics precisam de credenciais válidas do Facebook.

### "Como obter credenciais Facebook?"
➡️ https://developers.facebook.com/apps/
1. Criar app
2. Adicionar produto "Marketing API"
3. Gerar Access Token
4. Obter Ad Account ID

### "Preciso rodar todos os 9 serviços Docker?"
⚠️ **Para funcionalidade completa, SIM.** Mas você pode começar só com app + postgres + redis:
```bash
docker-compose up app postgres redis
```

### "Como fazer deploy em produção?"
➡️ Leia [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - guia completo de deploy em VPS com SSL.

### "Onde estão os testes?"
➡️ `tests/unit/` e `tests/integration/`  
⚠️ **Nota:** Testes precisam ser atualizados para nova estrutura (ver STATUS-PROJETO.md)

### "Como contribuir?"
➡️ Veja seção "Contributing" no [README.md](README.md)

---

## ✅ VALIDAÇÃO RÁPIDA

Execute estes comandos para validar instalação:

```bash
# 1. Docker rodando?
docker-compose ps
# Esperado: 9 serviços UP

# 2. API respondendo?
curl http://localhost:8000/health
# Esperado: {"status":"healthy",...}

# 3. Swagger acessível?
# Abrir: http://localhost:8000/docs
# Esperado: Interface Swagger com endpoints

# 4. Prometheus coletando?
curl http://localhost:8000/metrics
# Esperado: Métricas em formato Prometheus

# 5. Grafana acessível?
# Abrir: http://localhost:3000
# Login: admin/admin
```

Se **TODOS passaram** ✅ - Você está pronto! 🎉

---

## 🎓 GLOSSÁRIO RÁPIDO

| Termo | O que é |
|-------|---------|
| **FastAPI** | Framework web Python para APIs REST |
| **Celery** | Sistema de filas para tarefas assíncronas |
| **n8n** | Ferramenta de automação (workflows) |
| **Traefik** | Proxy reverso com SSL automático |
| **Prometheus** | Sistema de coleta de métricas |
| **Grafana** | Plataforma de visualização de dados |
| **Alembic** | Ferramenta de migrations de banco |
| **SQLAlchemy** | ORM Python para banco de dados |

---

## 🏁 PRÓXIMO PASSO

**Escolha um caminho:**

### Path A: Desenvolvedor
1. ✅ Executar: `docker-compose up -d`
2. ✅ Explorar: http://localhost:8000/docs
3. ✅ Ler: [STATUS-PROJETO.md](STATUS-PROJETO.md)
4. ✅ Desenvolver features pendentes

### Path B: DevOps
1. ✅ Ler: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. ✅ Provisionar VPS
3. ✅ Configurar DNS
4. ✅ Deploy: `./scripts/deploy.sh`

### Path C: Gestor/PO
1. ✅ Ler: [README-AUDITORIA.md](README-AUDITORIA.md)
2. ✅ Revisar: [SUMMARY-FINAL.md](SUMMARY-FINAL.md)
3. ✅ Planejar: Próximas features
4. ✅ Aprovar: Deploy em produção

---

**Escolha seu caminho e bora começar! 🚀**

**Dúvidas?** Consulte [INDICE-COMPLETO.md](INDICE-COMPLETO.md) para navegar toda documentação.


