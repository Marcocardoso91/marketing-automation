# Backlog - Marketing Automation Platform

**Versão:** 1.0.0
**Data:** 18 de Outubro, 2025
**Status (histórico):** Roadmap planejado para 18/10/2025. Consulte `RELATORIO-CORRECOES-PENDENTES.md` antes de priorizar novas entregas.
**Método:** Priorização MoSCoW

---

## Q4 2025 (ATUAL)

### Must Have ✅ (COMPLETO)
- [x] Integração Agent API ↔ Analytics
- [x] Pacote Python compartilhado
- [x] Endpoint /api/v1/metrics/export
- [x] Docker Compose integrado
- [x] Documentação completa (3 PRDs + ADRs)
- [x] Testes de integração

### Should Have ⚠️ (EM PROGRESSO)
- [ ] HTTPS em produção (Traefik/Nginx)
- [ ] Cobertura de testes 80%+
- [ ] Alertas automáticos (Slack)
- [ ] Backup automático Supabase

### Could Have 📅 (PLANEJADO)
- [ ] Dashboard Grafana customizado
- [ ] API rate limiting por usuário individual
- [ ] Webhooks bidirecionais

### Won't Have (Adiado para Q1 2026)
- ❌ GraphQL API
- ❌ Kubernetes
- ❌ Machine Learning

---

## Q1 2026

### Must Have
- [ ] Horizontal scaling Agent API (load balancer)
- [ ] PostgreSQL read replicas
- [ ] HTTPS em todos os ambientes
- [ ] Backup/restore automatizado

### Should Have
- [ ] TikTok Analytics integration
- [ ] LinkedIn Ads integration
- [ ] Streaming de métricas (SSE)
- [ ] Cache compartilhado Redis

### Could Have
- [ ] GraphQL API
- [ ] gRPC para alta performance
- [ ] ML básico (previsão de CTR)

---

## Q2 2026

### Must Have
- [ ] Multi-tenant (10+ clientes)
- [ ] Billing e uso por cliente
- [ ] API pública para terceiros
- [ ] Marketplace de automações

### Should Have
- [ ] WhatsApp Business API
- [ ] Dashboard mobile (PWA)
- [ ] Export automático PDF/Excel
- [ ] A/B testing framework

### Could Have
- [ ] Kubernetes deployment
- [ ] ML avançado (creative optimization)
- [ ] Integrações premium (Salesforce, HubSpot)

---

## Q3 2026

### Must Have
- [ ] Open-source do framework
- [ ] Documentação para desenvolvedores externos
- [ ] Programa de contributors

### Should Have
- [ ] Certificações (SOC 2, ISO 27001)
- [ ] Compliance LGPD/GDPR automatizado
- [ ] Disaster recovery < 1h

---

## Backlog Técnico

### Performance
- [ ] Implementar caching agressivo (Redis)
- [ ] Otimizar queries PostgreSQL (EXPLAIN ANALYZE)
- [ ] Connection pooling otimizado
- [ ] Compressão de responses (gzip)

### Segurança
- [ ] Rotação automática de API keys
- [ ] 2FA para usuários
- [ ] Auditoria de acessos (SOC 2)
- [ ] Penetration testing

### DevOps
- [ ] Blue-green deployment
- [ ] Canary releases
- [ ] Chaos engineering (testes de resiliência)
- [ ] Auto-scaling baseado em CPU/memória

### Observabilidade
- [ ] Distributed tracing (Jaeger)
- [ ] APM (Application Performance Monitoring)
- [ ] Error tracking (Sentry)
- [ ] Logs centralizados (ELK Stack)

---

## Features Solicitadas por Usuários

| Feature | Solicitante | Prioridade | Sprint |
|---------|-------------|------------|--------|
| Export PDF relatórios | Sabrina | Alta | Q1 2026 |
| WhatsApp notifications | Sabrina | Média | Q2 2026 |
| TikTok integration | Sabrina | Alta | Q1 2026 |
| Mobile app | Marco | Baixa | Q3 2026 |
| Instagram API | Sabrina | Alta | Q1 2026 |

---

## Tech Debt

| Item | Esforço | Impacto | Prazo |
|------|---------|---------|-------|
| Aumentar cobertura testes (70% → 80%) | 3 dias | Alto | Q4 2025 |
| Refatorar FacebookAdsAgent | 5 dias | Médio | Q1 2026 |
| Migrar para Pydantic V2 | 2 dias | Baixo | Q1 2026 |
| Documentar API interna | 2 dias | Médio | Q4 2025 |
| Limpar código duplicado | 3 dias | Médio | Q1 2026 |

---

## Referências

- [PRD-AGENT-API.md](PRD-AGENT-API.md)
- [PRD-ANALYTICS.md](PRD-ANALYTICS.md)
- [ADR-CONSOLIDATED.md](ADR-CONSOLIDATED.md)

---

**Atualizado:** 18 de Outubro, 2025
