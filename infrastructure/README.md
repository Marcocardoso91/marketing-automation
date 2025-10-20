# Infrastructure - Marketing Automation Platform

**Propósito:** Configurações centralizadas de infraestrutura (Docker, Monitoring, CI/CD)

---

## 📁 Estrutura

```
infrastructure/
├── docker/
│   ├── backend.Dockerfile              # Dockerfile do backend
│   └── docker-compose.integrated.yml   # Compose integrado (cópia)
└── monitoring/
    └── prometheus.yml                   # Config Prometheus
```

---

## 🐳 Docker

### `docker/backend.Dockerfile`

**Propósito:** Build image do backend (FastAPI + Celery)

**Características:**
- Multi-stage build (otimizado)
- Python 3.11-slim
- User não-root para segurança
- Health checks incluídos

**Uso:**
```bash
# Build direto
docker build -f infrastructure/docker/backend.Dockerfile -t marketing-backend ./backend

# Ou via docker-compose (usa backend/Dockerfile original)
docker-compose -f docker-compose.integrated.yml build
```

**Nota:** Esta é uma **cópia** do `backend/Dockerfile` original. O source of truth é `backend/Dockerfile`.

### `docker/docker-compose.integrated.yml`

**Propósito:** Stack completo com todos os serviços

**Serviços incluídos:**
1. **agent-api** - Backend FastAPI (port 8000)
2. **postgres** - Database PostgreSQL 15 (port 5432)
3. **redis** - Cache + Celery broker (port 6380)
4. **celery-worker** - Worker para tarefas assíncronas
5. **celery-beat** - Scheduler
6. **superset** - BI dashboards (port 8088)
7. **prometheus** - Monitoring (port 9090) - opcional
8. **grafana** - Visualização (port 3000) - opcional

**Uso:**
```bash
# Subir stack completa
docker-compose -f docker-compose.integrated.yml up -d

# Ver logs
docker-compose -f docker-compose.integrated.yml logs -f

# Parar tudo
docker-compose -f docker-compose.integrated.yml down
```

**Nota:** Esta é uma **cópia** do `docker-compose.integrated.yml` da raiz. Use aquele como source of truth.

---

## 📊 Monitoring

### `monitoring/prometheus.yml`

**Propósito:** Configuração do Prometheus para monitoramento de métricas

**Scrape configs:**
1. **agent-api** - Coleta métricas da API em `/metrics`
2. **postgres** - Monitoramento do database

**Intervalo:** 15 segundos

**Uso:**
```bash
# Via docker-compose (profile monitoring)
docker-compose -f docker-compose.integrated.yml --profile monitoring up -d

# Acessar Prometheus
http://localhost:9090
```

**Métricas disponíveis:**
- Request duration
- Request count
- Error rate
- Custom business metrics

---

## 🚀 CI/CD

**Status:** 📋 Planejado (não implementado ainda)

**Quando implementar, adicionar:**
```
infrastructure/ci-cd/
└── .github/workflows/
    ├── ci.yml              # Testes automatizados
    ├── cd.yml              # Deploy automático
    └── docker-build.yml    # Build de imagens
```

---

## 📋 Checklist de Uso

### Para Deploy Local
- [x] docker-compose.integrated.yml configurado
- [x] prometheus.yml configurado
- [ ] .env com todas credenciais
- [ ] Volumes Docker criados

### Para Deploy Produção
- [x] Dockerfiles multi-stage
- [ ] CI/CD configurado
- [ ] Secrets em vault (não .env)
- [ ] Health checks configurados

---

## 🔗 Arquivos Relacionados

- **Source of truth Docker:** `../docker-compose.integrated.yml` (raiz)
- **Source of truth Dockerfile:** `../backend/Dockerfile`
- **Documentação operacional:** `../docs/operations/`
- **Guia de deploy:** `../docs/operations/INTEGRATION-GUIDE.md`

---

## ⚠️ Notas Importantes

1. **Duplicação:** Os arquivos aqui são **cópias** dos originais na raiz e em backend/
2. **Source of truth:** Sempre edite os arquivos originais, não as cópias
3. **Sincronia:** Se mudar Dockerfile original, atualize a cópia aqui

---

**Última atualização:** 20 de Outubro, 2025

