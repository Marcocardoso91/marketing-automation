# Guia de Segurança - Ecossistema Macspark

Este documento descreve as práticas de segurança implementadas e recomendações para manter o ecossistema Macspark seguro.

## 🛡️ Visão Geral de Segurança

O ecossistema Macspark implementa segurança em múltiplas camadas:
- **Frontend**: Content Security Policy (CSP), headers de segurança
- **Backend**: Autenticação JWT, validação de entrada, rate limiting
- **Infraestrutura**: Docker Swarm, Traefik SSL, Cloudflare Tunnel
- **Dados**: Criptografia, backup seguro, gestão de secrets

## 🔐 Gestão de Secrets e Credenciais

### Variáveis de Ambiente
```bash
# NUNCA commitar estas variáveis:
CLAUDE_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
SUPABASE_ANON_KEY=eyJ...
DATABASE_PASSWORD=...
```

### Docker Secrets (Produção)
```bash
# Criar secrets no Swarm
echo "super_secure_password" | docker secret create db_password -
echo "sk-ant-api-key" | docker secret create claude_api_key -
```

### Arquivos .env
- ✅ Use `.env.example` como template
- ✅ Adicione `.env` ao `.gitignore` 
- ❌ NUNCA commite arquivos `.env`

## 🐳 Segurança de Containers

### Dockerfile Hardening
```dockerfile
# ✅ Usuário não-root implementado
USER nginx-user

# ✅ Multi-stage builds para imagens menores
FROM node:18-alpine AS builder
# ... build stage ...
FROM nginx:alpine AS production

# ✅ Health checks obrigatórios
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost/health || exit 1
```

### Docker Compose Segurança
```yaml
# ✅ Networks isoladas
networks:
  frontend:
    driver: overlay
  backend:
    driver: overlay
    internal: true  # Sem acesso externo

# ✅ Recursos limitados
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

## 🌐 Segurança Web Frontend

### Content Security Policy (CSP)
```nginx
# Implementado no nginx.conf
add_header Content-Security-Policy "
  default-src 'self';
  script-src 'self' https://cdn.jsdelivr.net;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  connect-src 'self' https: wss: https://*.supabase.co;
" always;
```

### Headers de Segurança
- `X-Frame-Options: DENY` - Previne clickjacking
- `X-XSS-Protection: 1; mode=block` - Proteção XSS
- `X-Content-Type-Options: nosniff` - Previne MIME sniffing
- `Strict-Transport-Security` - Force HTTPS
- `Referrer-Policy: strict-origin-when-cross-origin`

## 🔒 Autenticação e Autorização

### Supabase Auth
```typescript
// Row Level Security (RLS) habilitado
CREATE POLICY "Users can only see own data" ON profiles
  FOR ALL USING (auth.uid() = user_id);

// JWT tokens com expiração
const { data, error } = await supabase.auth.signInWithPassword({
  email,
  password
});
```

### Rate Limiting
```yaml
# Traefik middleware
middlewares:
  rate-limit:
    rateLimit:
      burst: 100
      average: 50
```

## 🔍 Monitoramento de Segurança

### Logs de Segurança
```yaml
# Prometheus alerts para eventos suspeitos
- alert: HighFailedLoginRate
  expr: rate(failed_logins_total[5m]) > 10
  annotations:
    summary: "Taxa alta de logins falhados"
```

### Scanning de Vulnerabilidades
```bash
# Executar regularmente
npm audit                    # Frontend
pip-audit                   # Backend  
docker scan macspark-app:latest  # Containers
```

## 🛠️ Práticas de Desenvolvimento Seguro

### Code Review Checklist
- [ ] Secrets hardcoded verificados
- [ ] Validação de entrada implementada
- [ ] Escape de output realizado
- [ ] Permissões mínimas aplicadas
- [ ] Logs de segurança adicionados

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    hooks:
      - id: detect-secrets
  - repo: https://github.com/PyCQA/bandit
    hooks:
      - id: bandit
```

## 🚨 Resposta a Incidentes

### Procedimento de Emergência
1. **Detecção**: Alertas automáticos via Grafana/Prometheus
2. **Contenção**: Isolar serviços afetados
3. **Avaliação**: Determinar escopo do incidente
4. **Recuperação**: Restaurar serviços seguros
5. **Lições**: Post-mortem e melhorias

### Contatos de Emergência
- **Administrador**: marco@macspark.dev
- **Equipe DevOps**: devops@macspark.dev
- **Suporte 24/7**: +55 11 9xxxx-xxxx

## 📊 Compliance e Auditoria

### LGPD/GDPR
- Consentimento explícito para coleta de dados
- Direito ao esquecimento implementado
- Portabilidade de dados via API
- Logs de acesso mantidos por 1 ano

### Auditoria Regular
- **Semanal**: Scan de vulnerabilidades
- **Mensal**: Review de permissões
- **Trimestral**: Teste de recuperação
- **Anual**: Auditoria completa de segurança

## 🔧 Configurações por Componente

### Macspark-App (Frontend)
- CSP hardening implementado ✅
- HTTPS redirect obrigatório ✅
- Headers de segurança configurados ✅
- Authentication flows seguros ✅

### Macspark-MCPs (Backend)
- API keys em variáveis de ambiente ✅
- Validação Pydantic nas entradas ✅
- Rate limiting por provider ✅
- Logs estruturados para auditoria ✅

### Macspark-Setup (Infraestrutura)
- Docker secrets para senhas ✅
- Traefik com SSL automático ✅
- Cloudflare Tunnel para exposição ✅
- Monitoring com alertas ✅

## 📚 Recursos e Referências

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Nginx Security Guide](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)
- [Supabase Security](https://supabase.com/docs/guides/platform/going-into-prod)

---

## ⚠️ Vulnerabilidades Conhecidas e Mitigações

### ✅ Resolvidas (Sprint Atual)
- **CVE-DOCKER-ROOT**: Container executando como root → Usuário não-root implementado
- **DEP-OUTDATED**: Dependências sem versão fixa → Versões fixadas em requirements.txt
- **CSP-UNSAFE**: CSP com unsafe-inline → Será corrigido na Fase 2

### 🔄 Em Andamento
- **MCP-STATEFUL**: Orquestrador com estado local → Migração para Redis (Fase 2)
- **MONITORING-BASIC**: Monitoring básico → Dashboards e alertas customizados (Fase 3)

### 📋 Roadmap de Segurança
1. **Fase 1 (Concluída)**: Correções críticas imediatas
2. **Fase 2 (Sprint 2-3)**: Hardening arquitetural  
3. **Fase 3 (Contínuo)**: Monitoramento avançado e compliance

---

**Última atualização**: 2025-01-13  
**Próxima revisão**: 2025-02-13  
**Responsável**: Marco / Equipe DevSecOps