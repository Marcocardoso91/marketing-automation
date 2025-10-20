# Checklist de Validação - Marketing Automation Platform

## Pré-Deploy

- [ ] env.template copiado para .env
- [ ] Todas as credenciais configuradas no .env
- [ ] Pacote shared instalado: `pip install -e ./shared`
- [ ] Docker e Docker Compose instalados
- [ ] Portas livres: 8000, 5432, 6379, 8088

## Instalação

- [ ] Setup executado: `.\scripts\setup.ps1`
- [ ] Redes Docker criadas: `docker network ls | grep marketing-net`
- [ ] Containers buildados: `docker images | grep marketing`
- [ ] API keys geradas e adicionadas no .env

## Serviços

- [ ] PostgreSQL UP: `docker ps | grep marketing-postgres`
- [ ] Redis UP: `docker ps | grep marketing-redis`
- [ ] Agent API UP: `docker ps | grep marketing-agent-api`
- [ ] Celery Worker UP: `docker ps | grep marketing-celery-worker`
- [ ] Superset UP: `docker ps | grep marketing-superset`

## Health Checks

- [ ] Agent API health: `curl http://localhost:8000/health`
- [ ] Metrics endpoint: `curl http://localhost:8000/api/v1/metrics/health`
- [ ] Swagger UI acessível: http://localhost:8000/docs
- [ ] Superset acessível: http://localhost:8088

## Integração

- [ ] Endpoint requer auth: `curl http://localhost:8000/api/v1/metrics/export` (retorna 401 ou 422)
- [ ] Auth com API key válida funciona
- [ ] Schema validation funciona (Pydantic)
- [ ] Cliente Python importa: `from marketing_shared.utils.api_client import AgentAPIClient`
- [ ] Validação passa: `python scripts/validate-integration.py`

## Analytics

- [ ] Script Python consegue buscar do Agent API
- [ ] Supabase recebe dados (verificar no SQL Editor)
- [ ] Workflows n8n importados
- [ ] Workflows n8n executam sem erro
- [ ] OpenAI gera insights
- [ ] Slack recebe notificações

## Testes

- [ ] Script de validação passa: `python scripts/validate-integration.py`
- [ ] Testes unitários passam (se aplicável)
- [ ] Nenhum erro crítico nos logs

## Documentação

- [ ] README.md revisado
- [ ] INTEGRATION-GUIDE.md consultado
- [ ] ARCHITECTURE.md entendido
- [ ] Procedimentos documentados

## Produção (Quando Aplicável)

- [ ] Variáveis de ambiente em produção configuradas
- [ ] SSL/TLS configurado
- [ ] Backups automáticos configurados
- [ ] Monitoramento configurado (Prometheus + Grafana)
- [ ] Alertas configurados

---

**Data de Validação:** ____/____/________  
**Responsável:** ___________________  
**Resultado:** [ ] Aprovado [ ] Reprovado

