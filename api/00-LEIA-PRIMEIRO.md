# 📖 LEIA PRIMEIRO - Facebook Ads AI Agent

## 👋 Bem-vindo!

Você está no projeto **Facebook Ads AI Agent** - um sistema de IA para análise e otimização automática de campanhas do Facebook Ads.

---

## ⚡ EXECUÇÃO SUPER RÁPIDA (2 minutos)

```bash
# Passo 1: Configure credenciais Facebook
cp .env.example .env
# Edite .env com suas credenciais

# Passo 2: Inicie tudo
docker-compose up -d

# Passo 3: Acesse a API
# http://localhost:8000/docs
```

✅ **Pronto!** Sua aplicação está rodando.

---

## 📚 DOCUMENTAÇÃO - POR ONDE COMEÇAR

### 🚀 Quero EXECUTAR
1. **[START-HERE.md](START-HERE.md)** - Ponto de entrada principal
2. **[COMO-EXECUTAR.md](COMO-EXECUTAR.md)** - Guia detalhado de execução
3. **[README.md](README.md)** - Documentação principal do código

### 📊 Quero VER STATUS
1. **[CONCLUSAO-IMPLEMENTACAO.md](CONCLUSAO-IMPLEMENTACAO.md)** - Conclusão final ⭐
2. **[SUMMARY-FINAL.md](SUMMARY-FINAL.md)** - Sumário com estatísticas
3. **[STATUS-PROJETO.md](STATUS-PROJETO.md)** - Status detalhado por sprint
4. **[IMPLEMENTACAO-COMPLETA.md](IMPLEMENTACAO-COMPLETA.md)** - O que foi implementado

### 🏗️ Quero ENTENDER ARQUITETURA
1. **[docs/auditoria/ARCHITECTURE-BLUEPRINT.md](docs/auditoria/ARCHITECTURE-BLUEPRINT.md)** - Diagramas completos
2. **[README-AUDITORIA.md](README-AUDITORIA.md)** - Resumo executivo da auditoria

### 🚀 Quero FAZER DEPLOY
1. **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guia de deploy em produção
2. **[docs/RUNBOOK.md](docs/RUNBOOK.md)** - Operações e emergências

### 🔧 Quero CONFIGURAR
1. **[docs/n8n-setup.md](docs/n8n-setup.md)** - Workflows n8n
2. **[docs/GUIA-COMPLETO-TESTES-CICD.md](docs/GUIA-COMPLETO-TESTES-CICD.md)** - Testes e CI/CD

---

## ✅ O QUE ESTÁ PRONTO

- ✅ **Infraestrutura completa** (Docker, 9 serviços)
- ✅ **API REST funcional** (13 endpoints)
- ✅ **Agente IA operante** (Facebook Ads)
- ✅ **Analytics com ML** (scoring, anomalias)
- ✅ **Automação inteligente** (sugestões)
- ✅ **Observabilidade** (Prometheus + Grafana)
- ✅ **Deploy pronto** (Traefik + SSL)
- ✅ **Documentação excelente** (300+ páginas)

**Status:** ✅ 70% completo | Core 100% funcional

---

## 🎯 ESTRUTURA DO PROJETO

```
facebook-ads-ai-agent/
├── src/                   ✅ Código principal (38 arquivos)
├── tests/                 ⏳ Testes (a atualizar)
├── config/                ✅ Configurações
├── scripts/               ✅ Deploy, backup, restore
├── docs/                  ✅ Documentação (15 docs)
├── alembic/               ✅ Migrations
├── main.py                ✅ Entry point FastAPI
├── docker-compose.yml     ✅ Dev environment
├── docker-compose.prod.yml ✅ Production
├── requirements.txt       ✅ Dependências
└── README.md              ✅ Docs principal
```

---

## 🔥 COMANDOS ESSENCIAIS

```bash
# Executar localmente
python main.py

# Docker
docker-compose up -d        # Iniciar
docker-compose ps           # Ver status
docker-compose logs -f app  # Ver logs
docker-compose down         # Parar

# Testes
make test                   # Todos
make test-unit              # Unitários
make lint                   # Verificar código
make format                 # Formatar código

# Deploy produção
./scripts/deploy.sh

# Backup
./scripts/backup.sh
```

---

## 🆘 AJUDA RÁPIDA

### Erro ao rodar?
➡️ Veja [COMO-EXECUTAR.md](COMO-EXECUTAR.md) seção **Troubleshooting**

### Preciso fazer deploy?
➡️ Siga [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) passo-a-passo

### Dúvidas técnicas?
➡️ Consulte [docs/RUNBOOK.md](docs/RUNBOOK.md) ou [README.md](README.md)

### Quer entender tudo?
➡️ Leia [INDICE-COMPLETO.md](INDICE-COMPLETO.md) - índice de toda documentação

---

## 📞 SUPORTE

**Documentação:** 24 docs em `/docs/` e raiz  
**Issues:** GitHub Issues  
**Código:** Bem comentado em `src/`  

---

## 🎉 COMEÇE AGORA!

```bash
# 1. Configure
cp .env.example .env

# 2. Execute
docker-compose up -d

# 3. Teste
curl http://localhost:8000/health

# 4. Explore
# http://localhost:8000/docs
```

**Pronto! Você tem uma API de IA rodando! 🚀**

---

**Próximo passo:** Leia [START-HERE.md](START-HERE.md) para mais detalhes.


