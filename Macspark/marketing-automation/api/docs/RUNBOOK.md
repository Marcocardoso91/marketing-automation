# Facebook Ads AI Agent - RUNBOOK

Guia operacional para emergências e operações em produção.

## Informações Básicas

- **Aplicação:** Facebook Ads AI Agent
- **Versão:** 1.0.0
- **Servidor:** VPS Ubuntu 22.04
- **Localização:** /opt/facebook-ads-ai-agent

## Contatos de Emergência

| Papel | Nome | Telefone | Email |
|-------|------|----------|-------|
| Tech Lead | [Nome] | [Telefone] | [Email] |
| DevOps | [Nome] | [Telefone] | [Email] |
| On-Call | [Nome] | [Telefone] | [Email] |

## Procedimentos de Emergência

### Aplicação Não Responde

```bash
# 1. Verificar status dos containers
docker-compose ps

# 2. Verificar logs
docker-compose logs -f app --tail=100

# 3. Reiniciar serviço específico
docker-compose restart app

# 4. Se persistir, reiniciar stack completa
docker-compose down
docker-compose up -d
```

### Database Corrompido

```bash
# 1. Parar aplicação
docker-compose stop app celery_worker celery_beat

# 2. Restaurar último backup
./scripts/restore.sh backups/backup_YYYYMMDD_HHMMSS.sql.gz

# 3. Rodar migrations
docker-compose exec app alembic upgrade head

# 4. Reiniciar aplicação
docker-compose start app celery_worker celery_beat
```

### Rate Limit Facebook API

```bash
# 1. Verificar logs de erro
docker-compose logs app | grep "Rate limit"

# 2. Aumentar intervalo de coleta temporariamente
# Editar src/tasks/celery_app.py:
# 'schedule': 3600.0,  # Mudar de 1800 para 3600 (1h)

# 3. Rebuild e restart
docker-compose restart celery_beat
```

### Disco Cheio

```bash
# 1. Verificar uso
df -h

# 2. Limpar logs antigos
docker-compose exec app find /app/logs -name "*.log" -mtime +7 -delete

# 3. Limpar dados antigos
docker-compose exec postgres psql -U postgres facebook_ads_ai -c "DELETE FROM insights WHERE date < NOW() - INTERVAL '365 days';"

# 4. Vacuum database
docker-compose exec postgres psql -U postgres facebook_ads_ai -c "VACUUM FULL;"
```

### SSL Certificado Expirado

```bash
# Traefik renova automaticamente, mas se falhar:

# 1. Verificar logs Traefik
docker-compose logs traefik | grep "acme"

# 2. Forçar renovação (deletar certificado)
rm letsencrypt/acme.json
docker-compose restart traefik

# 3. Aguardar emissão (pode levar 5min)
```

## Operações Rotineiras

### Deploy de Nova Versão

```bash
cd /opt/facebook-ads-ai-agent
./scripts/deploy.sh
```

### Backup Manual

```bash
./scripts/backup.sh
```

### Verificar Saúde do Sistema

```bash
# Health check
curl https://fbads.example.com/health

# Métricas Prometheus
curl https://fbads.example.com/metrics

# Status containers
docker-compose ps

# Uso de recursos
docker stats --no-stream
```

### Escalar Workers Celery

```bash
# Aumentar concorrência
docker-compose up -d --scale celery_worker=3

# Ou editar docker-compose.prod.yml:
# command: celery -A src.tasks.celery_app worker --concurrency=8
```

### Ver Logs em Tempo Real

```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f app
docker-compose logs -f celery_worker
docker-compose logs -f postgres
```

## Rollback

### Reverter para Versão Anterior

```bash
# 1. Identificar commit anterior
git log --oneline -n 5

# 2. Checkout versão anterior
git checkout <commit-hash>

# 3. Deploy
./scripts/deploy.sh

# 4. Se migration causou problema, reverter
docker-compose exec app alembic downgrade -1
```

### Restaurar Backup

```bash
# Listar backups disponíveis
ls -lh backups/

# Restaurar backup específico
./scripts/restore.sh backups/backup_20251018_080000.sql.gz
```

## Monitoramento

### Dashboards

- **Grafana:** https://grafana.fbads.example.com
  - System Health
  - Facebook Ads Performance
  - Agent Activity
  - API Metrics

- **Flower:** https://flower.fbads.example.com
  - Celery tasks monitor

- **Prometheus:** https://prometheus.fbads.example.com
  - Raw metrics

### Alertas Configurados

| Alerta | Threshold | Ação |
|--------|-----------|------|
| CPU > 80% | 5 minutos | Investigar, escalar se necessário |
| Error rate > 5% | 2 minutos | Verificar logs, rollback se necessário |
| FB API latency > 3s | 5 minutos | Verificar rate limit |
| Daily spend > threshold | Instant | Notificar via Slack |

## Troubleshooting

### Container não inicia

```bash
# Ver erro específico
docker-compose logs <service_name>

# Verificar configuração
docker-compose config

# Reconstruir imagem
docker-compose build --no-cache <service_name>
docker-compose up -d <service_name>
```

### Performance degradada

```bash
# 1. Verificar uso de recursos
docker stats

# 2. Verificar queries lentas no PostgreSQL
docker-compose exec postgres psql -U postgres facebook_ads_ai -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# 3. Analisar slow queries
docker-compose logs app | grep "duration>"

# 4. Considerar adicionar índices
```

### Memória alta

```bash
# 1. Identificar container
docker stats --no-stream

# 2. Reiniciar container problemático
docker-compose restart <service_name>

# 3. Limpar cache Redis
docker-compose exec redis redis-cli FLUSHDB
```

## Maintenance Windows

### Backup Programado

- **Frequência:** Diário às 02:00 UTC
- **Retenção:** 7 dias
- **Localização:** `/opt/facebook-ads-ai-agent/backups/`
- **Cron:** Configurado no VPS

```cron
0 2 * * * cd /opt/facebook-ads-ai-agent && ./scripts/backup.sh >> /var/log/fbads-backup.log 2>&1
```

### Cleanup Programado

- **Conversações:** Deletar > 90 dias (Domingo 02:00)
- **Insights:** Deletar > 365 dias (Domingo 02:00)
- **Logs:** Deletar > 30 dias (Diário via logrotate)

## Security

### Rotação de Secrets

```bash
# 1. Gerar novo SECRET_KEY
openssl rand -hex 32

# 2. Atualizar .env
nano .env

# 3. Reiniciar aplicação
docker-compose restart app
```

### Atualizar Facebook Token

```bash
# 1. Obter novo token em: https://developers.facebook.com/tools/accesstoken/

# 2. Atualizar .env
nano .env  # Editar FACEBOOK_ACCESS_TOKEN

# 3. Reiniciar workers (não precisa reiniciar app)
docker-compose restart celery_worker celery_beat
```

## Referencias

- **Documentação:** `/docs`
- **Logs:** `./logs/`
- **Backups:** `./backups/`
- **Repositório:** https://github.com/your-org/facebook-ads-ai-agent

---

**Última atualização:** Outubro 2025  
**Próxima revisão:** Mensal

