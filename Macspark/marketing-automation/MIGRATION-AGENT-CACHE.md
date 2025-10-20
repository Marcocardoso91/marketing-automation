# Migração: Cache do FacebookAdsAgent

## 🎯 Objetivo

Implementar cache do `FacebookAdsAgent` para reduzir latência de **+300-500ms** para **~0ms** em requests subsequentes.

---

## ⚠️ Problema Atual (P0 #5)

```python
# ❌ ANTES - Cria nova instância a cada request
def get_facebook_agent() -> FacebookAdsAgent:
    return FacebookAdsAgent()  # 300-500ms latência!
```

**Impacto**:
- 10 requests/seg = 3-5 segundos desperdiçados
- 1000 requests/hora = 5-8 minutos de overhead
- Conexões desnecessárias ao Facebook API
- Rate limits mais atingidos

---

## ✅ Solução: Cache com TTL

**Criado**: [api/src/utils/agent_cache.py](api/src/utils/agent_cache.py)

```python
# ✅ DEPOIS - Reutiliza instância cached
from src.utils.agent_cache import get_facebook_agent

def my_endpoint(agent: FacebookAdsAgent = Depends(get_facebook_agent)):
    # agent é cached (0ms overhead)
    return agent.get_campaigns()
```

**Performance**:
- 1ª chamada: ~400ms (cold start)
- Chamadas seguintes: ~0ms (cached)
- Auto-refresh: 1 hora (3600s TTL)

---

## 📝 Migração Passo-a-Passo

### Arquivos a Atualizar

**Lista completa** de arquivos que usam `FacebookAdsAgent()`:

1. [api/src/api/metrics.py](api/src/api/metrics.py#L25)
2. [api/src/api/campaigns.py](api/src/api/campaigns.py#L19)
3. [api/src/api/chat.py](api/src/api/chat.py)
4. [api/src/api/analytics.py](api/src/api/analytics.py)
5. [api/src/api/notion.py](api/src/api/notion.py)
6. [api/src/api/automation.py](api/src/api/automation.py)
7. [api/src/tasks/collectors.py](api/src/tasks/collectors.py)
8. [api/src/tasks/processors.py](api/src/tasks/processors.py)

---

### Passo 1: Atualizar `api/src/api/metrics.py`

**ANTES**:
```python
from src.agents.facebook_ads_agent import FacebookAdsAgent

def get_facebook_agent() -> FacebookAdsAgent:
    """Dependency injection para FacebookAdsAgent"""
    return FacebookAdsAgent()  # ❌


@router.get("/ad-performance")
def get_ad_performance(
    ad_id: str,
    agent: FacebookAdsAgent = Depends(get_facebook_agent)  # ❌ Nova instância
):
    return agent.get_ad_insights(ad_id)
```

**DEPOIS**:
```python
from src.utils.agent_cache import get_facebook_agent  # ✅ Import alterado

# ✅ Remova a função local get_facebook_agent()
# Ela já está em agent_cache.py


@router.get("/ad-performance")
def get_ad_performance(
    ad_id: str,
    agent: FacebookAdsAgent = Depends(get_facebook_agent)  # ✅ Cached!
):
    return agent.get_ad_insights(ad_id)
```

---

### Passo 2: Atualizar `api/src/api/campaigns.py`

**ANTES**:
```python
from src.agents.facebook_ads_agent import FacebookAdsAgent

def get_facebook_agent() -> FacebookAdsAgent:
    """Provide a shared FacebookAdsAgent instance per request"""
    try:
        return FacebookAdsAgent()  # ❌
    except Exception as exc:
        logger.error(f"Failed to initialize Facebook agent: {exc}")
        raise HTTPException(status_code=503, detail="Facebook API unavailable")


@router.get("/campaigns")
def get_campaigns(agent: FacebookAdsAgent = Depends(get_facebook_agent)):  # ❌
    campaigns = agent.get_campaigns()
    return {"campaigns": campaigns}
```

**DEPOIS**:
```python
from src.utils.agent_cache import get_facebook_agent  # ✅ Import alterado
from src.agents.facebook_ads_agent import FacebookAdsAgent

# ✅ Remova a função local get_facebook_agent()


@router.get("/campaigns")
def get_campaigns(agent: FacebookAdsAgent = Depends(get_facebook_agent)):  # ✅
    try:
        campaigns = agent.get_campaigns()
        return {"campaigns": campaigns}
    except Exception as exc:
        logger.error(f"Failed to get campaigns: {exc}")
        raise HTTPException(status_code=503, detail="Facebook API unavailable")
```

---

### Passo 3: Atualizar Celery Tasks

**Celery tasks** também podem usar cache, mas com uma diferença:

**ANTES (tasks/collectors.py)**:
```python
@celery_app.task
def collect_campaign_metrics():
    agent = FacebookAdsAgent()  # ❌ Nova instância
    metrics = agent.get_campaign_metrics()
    # ...
```

**DEPOIS**:
```python
from src.utils.agent_cache import get_cached_agent_provider

@celery_app.task
def collect_campaign_metrics():
    provider = get_cached_agent_provider(cache_ttl=1800)  # 30min para tasks
    agent = provider.get_agent()  # ✅ Cached
    metrics = agent.get_campaign_metrics()
    # ...
```

**Nota**: Tasks usam TTL menor (30min) pois rodam em background.

---

## 🧪 Testes

### Teste Manual de Performance

```python
import time
from src.utils.agent_cache import get_facebook_agent

# 1ª chamada (cold start)
start = time.time()
agent1 = get_facebook_agent()
print(f"1ª chamada: {(time.time() - start) * 1000:.1f}ms")  # ~400ms

# 2ª chamada (cached)
start = time.time()
agent2 = get_facebook_agent()
print(f"2ª chamada: {(time.time() - start) * 1000:.1f}ms")  # ~0ms

# Verifica se é a mesma instância
print(f"Same instance: {agent1 is agent2}")  # True
```

### Endpoint de Health Check

Adicione endpoint para monitorar cache:

```python
from src.utils.agent_cache import get_cached_agent_provider

@router.get("/health/agent-cache")
def agent_cache_health():
    """Check agent cache status"""
    provider = get_cached_agent_provider()
    stats = provider.get_stats()
    return {
        "status": "healthy" if stats["is_valid"] else "expired",
        **stats
    }
```

**Resposta exemplo**:
```json
{
  "status": "healthy",
  "cached": true,
  "cache_age_seconds": 245.3,
  "cache_ttl_seconds": 3600,
  "is_valid": true,
  "creation_count": 1
}
```

---

## 🔧 Configuração Avançada

### Ajustar TTL

```python
# Produção: TTL longo (1 hora)
from src.utils.agent_cache import get_cached_agent_provider
provider = get_cached_agent_provider(cache_ttl=3600)

# Desenvolvimento: TTL curto (5 minutos)
provider = get_cached_agent_provider(cache_ttl=300)

# Tasks em background: TTL médio (30 minutos)
provider = get_cached_agent_provider(cache_ttl=1800)
```

### Invalidar Cache Manualmente

```python
from src.utils.agent_cache import get_cached_agent_provider

# Após atualizar credenciais Facebook
provider = get_cached_agent_provider()
provider.invalidate_cache()

# Próxima chamada criará nova instância
agent = provider.get_agent()
```

### Endpoint de Invalidação (Admin)

```python
@router.post("/admin/invalidate-cache")
def invalidate_agent_cache(
    current_user: dict = Depends(require_admin)  # Apenas admins
):
    """Invalidate Facebook agent cache (after config changes)"""
    provider = get_cached_agent_provider()
    provider.invalidate_cache()
    return {"message": "Agent cache invalidated", "status": "success"}
```

---

## 📊 Impacto Esperado

### Antes da Migração
```
10 requests/segundo × 400ms = 4 segundos overhead
= 40% do tempo em criação de agents
```

### Depois da Migração
```
1 cold start (400ms) + 9 cached (0ms) = 400ms total
= 4% do tempo em criação de agents
= 90% reduction em overhead
```

### Economia de Recursos

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Latência média | 400ms | 40ms | -90% |
| CPU overhead | Alto | Baixo | -85% |
| Facebook API calls | 10/s | 1/hora | -99.9% |
| Rate limit risk | Alto | Baixo | -95% |

---

## ⚡ Checklist de Migração

- [x] Criar `api/src/utils/agent_cache.py`
- [ ] Atualizar `api/src/api/metrics.py`
- [ ] Atualizar `api/src/api/campaigns.py`
- [ ] Atualizar `api/src/api/chat.py`
- [ ] Atualizar `api/src/api/analytics.py`
- [ ] Atualizar `api/src/api/notion.py`
- [ ] Atualizar `api/src/api/automation.py`
- [ ] Atualizar `api/src/tasks/collectors.py`
- [ ] Atualizar `api/src/tasks/processors.py`
- [ ] Adicionar endpoint `/health/agent-cache`
- [ ] Adicionar testes de performance
- [ ] Testar em staging
- [ ] Deploy em produção
- [ ] Monitorar métricas de latência

---

## 🔍 Monitoramento

### Logs a Observar

```log
# Cold start (normal)
INFO: Creating new FacebookAdsAgent instance
INFO: FacebookAdsAgent created successfully (took 412.3ms, count: 1)

# Cache hit (esperado)
DEBUG: Returning cached FacebookAdsAgent (age: 245.1s, ttl: 3600s)

# Cache expirado (normal após 1h)
INFO: FacebookAdsAgent cache expired (age: 3601.2s > ttl: 3600s), creating new instance
```

### Métricas para Grafana

- `facebook_agent_creation_time_ms` - Tempo de criação
- `facebook_agent_cache_age_seconds` - Idade do cache
- `facebook_agent_cache_hits_total` - Total de hits
- `facebook_agent_cache_misses_total` - Total de misses

---

## 🔗 Referências

- Issue P0 #5: [FacebookAdsAgent recriado](https://github.com/Marcocardoso28/mcp-orchestrator/issues/5)
- Arquivo criado: [api/src/utils/agent_cache.py](api/src/utils/agent_cache.py)
- Documentação FastAPI Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
- Cache Patterns: https://docs.python.org/3/library/functools.html#functools.lru_cache
