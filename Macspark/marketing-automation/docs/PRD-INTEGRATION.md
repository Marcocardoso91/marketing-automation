# PRD - Integração Agent API ↔ Analytics

**Versão:** 1.0.0
**Data:** 18 de Outubro, 2025
**Status (histórico):** Documento de 18/10/2025. Verifique `README.md` e o relatório de pendências para o panorama atual.
**Owner:** Marco @ Macspark

---

## 1. Visão Geral da Integração

### 1.1 Problema

**Antes da Integração:**
- ❌ **Agent API** e **Analytics** coletavam Meta Ads **independentemente**
- ❌ Duas conexões simultâneas com Facebook API
- ❌ Código duplicado para parsing de métricas
- ❌ Inconsistência de dados entre sistemas
- ❌ Desperdício de requests API do Facebook

### 1.2 Solução

**Após Integração:**
- ✅ **Agent API** é **fonte única** de dados Meta Ads
- ✅ **Analytics** busca do Agent API via HTTP (não direto do Facebook)
- ✅ **Código compartilhado** (marketing_shared package)
- ✅ **Dados consistentes** entre sistemas
- ✅ **Economiza** requests API do Facebook

### 1.3 Princípios da Integração

1. **Minimal Coupling:** Projetos mantêm independência
2. **Single Source of Truth:** Agent API é dono dos dados Meta Ads
3. **Shared Code:** Schemas e cliente HTTP compartilhados
4. **Backward Compatible:** Não quebra funcionalidades existentes
5. **Production Ready:** Rate limiting, retry logic, autenticação

---

## 2. Arquitetura de Integração

### 2.1 Diagrama de Componentes

```mermaid
graph TB
    subgraph "Agent API"
        FB[Facebook API] --> AGENT[FacebookAdsAgent]
        AGENT --> PG[PostgreSQL]
        AGENT --> EXPORT[/api/v1/metrics/export]
    end

    subgraph "Shared Package"
        SCHEMAS[Schemas Pydantic]
        CLIENT[AgentAPIClient]
    end

    subgraph "Analytics"
        N8N[n8n Workflow 9:45h]
        SCRIPT[Python Fallback Script]
    end

    EXPORT --> |HTTP GET| N8N
    EXPORT --> |HTTP GET| SCRIPT
    N8N --> SUPABASE[Supabase DW]
    SCRIPT --> SUPABASE

    EXPORT -.uses.-> SCHEMAS
    N8N -.uses.-> CLIENT
    SCRIPT -.uses.-> CLIENT
```

### 2.2 Fluxo de Dados

```
1. Facebook API → Agent API (coleta Meta Ads)
2. Agent API → PostgreSQL (armazena internamente)
3. Analytics → Agent API (GET /api/v1/metrics/export)
4. Agent API → Analytics (JSON response)
5. Analytics → Supabase (armazena no data warehouse)
6. Supabase → Superset (dashboards)
```

**Frequência:**
- Agent API coleta do Facebook: Contínua (Celery Beat)
- Analytics busca do Agent API: Diária às 9:45h (n8n)

---

## 3. Componentes da Integração

### 3.1 Shared Package (marketing_shared)

**Localização:** `marketing-automation/shared/`

**Instalação:**
```bash
pip install -e ./shared
```

**Conteúdo:**

#### 3.1.1 Schemas Pydantic

**Arquivo:** `marketing_shared/schemas/facebook_metrics.py`

```python
class CampaignMetricSchema(BaseModel):
    """Schema padronizado para métricas de campanha Meta Ads"""

    campaign_id: str = Field(..., min_length=1)
    campaign_name: str
    date: date

    # Métricas principais
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    spend: float = Field(ge=0)
    reach: int = Field(ge=0)
    frequency: float = Field(ge=0)

    # Métricas calculadas
    ctr: float = Field(ge=0, le=100)
    cpc: float = Field(ge=0)
    cpe: Optional[float] = Field(None, ge=0)
    cpm: Optional[float] = Field(None, ge=0)

    # Conversões
    conversions: int = Field(ge=0)
    conversion_rate: Optional[float] = Field(None, ge=0, le=100)
    roas: Optional[float] = None

    @field_validator('date')
    @classmethod
    def validate_date_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Data não pode estar no futuro')
        return v


class ExportedMetricsResponse(BaseModel):
    """Response do endpoint de exportação"""

    campaigns: List[CampaignMetricSchema]
    total_campaigns: int = Field(ge=0)
    date_from: date
    date_until: date
    exported_at: datetime
    data_source: str = Field(default="facebook-ads-ai-agent")
    version: str = Field(default="1.0.0")

    @field_validator('total_campaigns')
    @classmethod
    def validate_total_matches_list(cls, v: int, info) -> int:
        campaigns = info.data.get('campaigns', [])
        if v != len(campaigns):
            raise ValueError(f'total_campaigns ({v}) != len(campaigns) ({len(campaigns)})')
        return v
```

**Benefícios:**
- ✅ Validação automática de dados
- ✅ Type hints para IDE autocomplete
- ✅ Documentação inline (descriptions)
- ✅ Conversão automática de tipos
- ✅ Validadores customizados (data não pode ser futuro)

---

#### 3.1.2 Cliente HTTP

**Arquivo:** `marketing_shared/utils/api_client.py`

```python
class AgentAPIClient:
    """Cliente HTTP para comunicação com Agent API"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = self._create_session(max_retries)

    def _create_session(self, max_retries: int) -> requests.Session:
        """Cria sessão com retry logic"""
        session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,  # 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def get_metrics(
        self,
        date_from: str | date,
        date_until: str | date
    ) -> Dict:
        """Busca métricas do Agent API"""

        # Converter dates para string se necessário
        if isinstance(date_from, date):
            date_from = date_from.isoformat()
        if isinstance(date_until, date):
            date_until = date_until.isoformat()

        logger.info(f"Buscando métricas de {date_from} até {date_until}")

        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/metrics/export",
                headers={"X-API-Key": self.api_key},
                params={"date_from": date_from, "date_until": date_until},
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            logger.info(f"✅ Recebidas {data.get('total_campaigns', 0)} campanhas")
            return data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AgentAPIError("API key inválida ou expirada")
            elif e.response.status_code == 429:
                raise AgentAPIError("Rate limit excedido")
            else:
                raise AgentAPIError(f"HTTP {e.response.status_code}: {e.response.text}")

        except requests.exceptions.Timeout:
            raise AgentAPIError(f"Timeout após {self.timeout}s")

        except requests.exceptions.ConnectionError:
            raise AgentAPIError(f"Erro de conexão. Servidor rodando em {self.base_url}?")

        except Exception as e:
            raise AgentAPIError(f"Erro inesperado: {str(e)}")

    def health_check(self) -> bool:
        """Verifica se API está saudável"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
```

**Features:**
- ✅ Retry logic (3 tentativas com backoff exponencial)
- ✅ Timeout configurável (default 30s)
- ✅ Health check antes de buscar dados
- ✅ Tratamento robusto de erros
- ✅ Logging detalhado

---

### 3.2 Agent API - Endpoint de Exportação

**Arquivo:** `api/src/api/metrics.py`

**Endpoint:**
```http
GET /api/v1/metrics/export
Headers:
  X-API-Key: {ANALYTICS_API_KEY}
Query Params:
  date_from: YYYY-MM-DD (required)
  date_until: YYYY-MM-DD (required)
Response:
  200 OK - ExportedMetricsResponse (JSON)
  401 Unauthorized - API key inválida
  422 Validation Error - Parâmetros inválidos
  429 Too Many Requests - Rate limit excedido
  500 Internal Server Error - Erro no servidor
```

**Código:**
```python
from slowapi import Limiter
from marketing_shared.schemas.facebook_metrics import ExportedMetricsResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def verify_analytics_api_key(api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Verifica se API key é válida"""
    if api_key != settings.ANALYTICS_API_KEY:
        logger.warning("Tentativa de acesso com API key inválida")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


@router.get("/export", response_model=ExportedMetricsResponse)
@limiter.limit("1000/hour")  # Rate limit generoso para analytics
async def export_metrics(
    date_from: str = Query(..., pattern=r'^\d{4}-\d{2}-\d{2}$'),
    date_until: str = Query(..., pattern=r'^\d{4}-\d{2}-\d{2}$'),
    api_key: str = Depends(verify_analytics_api_key),
    agent: FacebookAdsAgent = Depends(get_facebook_agent)
):
    """Exporta métricas Meta Ads para sistema de analytics"""

    logger.info(f"Exportando métricas de {date_from} até {date_until}")

    try:
        # Buscar métricas do Facebook (via agent)
        raw_metrics = await agent.get_campaign_insights(date_from, date_until)

        # Converter para schema padronizado
        campaigns = [
            CampaignMetricSchema(
                campaign_id=str(m['campaign_id']),
                campaign_name=m['campaign_name'],
                date=datetime.strptime(m['date_start'], '%Y-%m-%d').date(),
                # ... demais campos
            )
            for m in raw_metrics
        ]

        return ExportedMetricsResponse(
            campaigns=campaigns,
            total_campaigns=len(campaigns),
            date_from=datetime.strptime(date_from, '%Y-%m-%d').date(),
            date_until=datetime.strptime(date_until, '%Y-%m-%d').date(),
            exported_at=datetime.utcnow(),
            data_source="facebook-ads-ai-agent",
            version="1.0.0"
        )

    except Exception as e:
        logger.error(f"❌ Erro ao exportar métricas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Features:**
- ✅ Autenticação via API Key (Header `X-API-Key`)
- ✅ Rate limiting: 1000 requests/hora (SlowAPI)
- ✅ Validação de parâmetros (regex pattern)
- ✅ Dependency injection (FacebookAdsAgent)
- ✅ Response padronizado (ExportedMetricsResponse)
- ✅ Logging detalhado

---

### 3.3 Analytics - Consumo do Agent API

#### 3.3.1 Workflow n8n

**Arquivo:** `analytics/n8n-workflows/meta-ads-supabase.json`

**Node: HTTP Request**
```json
{
  "parameters": {
    "url": "={{$env.AGENT_API_URL}}/api/v1/metrics/export",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-API-Key",
          "value": "={{$env.ANALYTICS_API_KEY}}"
        }
      ]
    },
    "sendQuery": true,
    "queryParameters": {
      "parameters": [
        {
          "name": "date_from",
          "value": "={{$today.minus({days: 1}).toFormat('yyyy-MM-dd')}}"
        },
        {
          "name": "date_until",
          "value": "={{$today.minus({days: 1}).toFormat('yyyy-MM-dd')}}"
        }
      ]
    },
    "options": {
      "timeout": 30000,
      "retry": {
        "maxRetries": 3,
        "waitBetweenRetries": 1000
      }
    }
  },
  "name": "Get from Agent API",
  "type": "n8n-nodes-base.httpRequest"
}
```

**Node: Validate Source**
```json
{
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{$json.data_source}}",
          "operation": "equals",
          "value2": "facebook-ads-ai-agent"
        }
      ]
    }
  },
  "name": "Validate Source",
  "type": "n8n-nodes-base.if"
}
```

---

#### 3.3.2 Script Python Fallback

**Arquivo:** `analytics/scripts/metrics-to-supabase.py`

**Mudança:**
```python
# ANTES (coletava direto do Facebook):
# def get_meta_ads_metrics():
#     fb_api = FacebookAPI(access_token=os.getenv('META_ACCESS_TOKEN'))
#     return fb_api.get_insights(...)

# AGORA (busca do Agent API):
from marketing_shared.utils.api_client import AgentAPIClient, AgentAPIError

def get_meta_ads_from_agent() -> List[Dict]:
    """Busca métricas Meta Ads do Agent API"""

    logger.info("🔄 Buscando métricas Meta Ads do Agent API...")

    # Configurar cliente
    client = AgentAPIClient(
        base_url=os.getenv('AGENT_API_URL', 'http://localhost:8000'),
        api_key=os.getenv('ANALYTICS_API_KEY'),
        timeout=30,
        max_retries=3
    )

    # Verificar health
    if not client.health_check():
        logger.error("❌ Agent API não está respondendo")
        raise AgentAPIError("Agent API indisponível")

    # Calcular datas (ontem)
    yesterday = (datetime.now() - timedelta(days=1)).date()

    try:
        # Buscar métricas
        response = client.get_metrics(
            date_from=yesterday,
            date_until=yesterday
        )

        campaigns = response['campaigns']
        logger.info(f"✅ Recebidas {len(campaigns)} campanhas do Agent API")
        logger.info(f"   Fonte: {response.get('data_source')}")
        logger.info(f"   Exportado em: {response.get('exported_at')}")

        return campaigns

    except AgentAPIError as e:
        logger.error(f"❌ Erro ao buscar métricas: {str(e)}")
        raise
```

---

## 4. Autenticação e Segurança

### 4.1 API Key Authentication

**Configuração:**

**Agent API** (`api/.env`):
```bash
ANALYTICS_API_KEY=your_secure_analytics_api_key_here_min_32_chars
```

**Analytics** (`analytics/scripts/.env`):
```bash
AGENT_API_URL=http://localhost:8000
ANALYTICS_API_KEY=your_secure_analytics_api_key_here_min_32_chars
```

**Geração de API Key:**
```bash
# Gerar com OpenSSL
openssl rand -hex 32

# Ou com Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4.2 Rate Limiting

**Configuração Agent API:**
- **Analytics:** 1000 requests/hora
- **Usuários internos (JWT):** 100 requests/minuto

**Motivo:**
- Analytics só coleta 1x/dia (1 request)
- Limite generoso para evitar erros
- Proteção contra abuse

**Headers de Resposta:**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1697652000
```

### 4.3 HTTPS (Produção)

**Recomendação:**
- ✅ Usar Traefik ou Nginx como reverse proxy
- ✅ Certificado SSL/TLS (Let's Encrypt)
- ✅ Redirecionar HTTP → HTTPS
- ✅ HSTS header habilitado

---

## 5. Tratamento de Erros

### 5.1 Cenários de Erro

| Erro | Causa | Mitigação |
|------|-------|-----------|
| **401 Unauthorized** | API key inválida | Verificar .env, regenerar key |
| **429 Too Many Requests** | Rate limit excedido | Aguardar reset, reduzir frequência |
| **500 Internal Server Error** | Erro no Agent API | Ver logs Agent API, debug |
| **Connection Error** | Agent API offline | Health check antes, fallback |
| **Timeout** | Resposta lenta | Aumentar timeout (30s → 60s) |

### 5.2 Retry Logic

**AgentAPIClient:**
```python
Retry Strategy:
  - Total retries: 3
  - Backoff factor: 1 (1s, 2s, 4s)
  - Status codes: 429, 500, 502, 503, 504
  - Methods: GET, POST
  - Timeout: 30s por tentativa
```

**Exemplo:**
```
Tentativa 1: ERRO 500 → Aguarda 1s
Tentativa 2: ERRO 500 → Aguarda 2s
Tentativa 3: ERRO 500 → Aguarda 4s
Tentativa 4: ERRO 500 → Lança AgentAPIError
```

### 5.3 Fallback

**Se Agent API falhar:**
1. ✅ **n8n workflow:** Marca execução como erro, tenta próximo dia
2. ✅ **Script Python:** Pode ser executado manualmente
3. ⚠️ **Não há coleta direta do Facebook** (não é fallback automático)

**Motivo:**
- Evitar duplicação de coleta
- Agent API deve ser restaurado, não bypassado

---

## 6. Monitoramento e Observabilidade

### 6.1 Logs

**Agent API:**
```bash
docker logs marketing-agent-api | grep "Exportando métricas"

# Output:
2025-10-18 09:45:12 INFO Exportando métricas de 2025-10-17 até 2025-10-17
2025-10-18 09:45:14 INFO ✅ Exportadas 15 campanhas com sucesso
```

**Analytics:**
```bash
docker logs marketing-celery-worker | grep "Agent API"

# Output:
2025-10-18 09:45:10 INFO 🔄 Buscando métricas Meta Ads do Agent API...
2025-10-18 09:45:11 INFO ✅ Recebidas 15 campanhas do Agent API
2025-10-18 09:45:11 INFO    Fonte: facebook-ads-ai-agent
```

### 6.2 Métricas Prometheus

**Agent API:**
```
# Requests ao endpoint de exportação
http_requests_total{endpoint="/api/v1/metrics/export", status="200"}

# Latência do endpoint
http_request_duration_seconds{endpoint="/api/v1/metrics/export", quantile="0.95"}

# Rate limit hits
rate_limit_hits_total{endpoint="/api/v1/metrics/export"}
```

### 6.3 Alertas (Planejado)

**Slack Alerts:**
- ⚠️ Rate limit excedido (> 900 requests/hora)
- ❌ Endpoint com taxa de erro > 1%
- ⏱️ Latência P95 > 2s
- 🔴 Agent API offline (health check failed)

---

## 7. Testes de Integração

**Arquivo:** `tests/integration/test_api_integration.py`

```python
def test_export_endpoint_with_valid_key(api_config, test_dates):
    """Testa exportação com API key válida"""
    response = requests.get(
        f"{api_config['base_url']}/api/v1/metrics/export",
        headers={'X-API-Key': api_config['api_key']},
        params=test_dates,
        timeout=30
    )

    assert response.status_code == 200

    data = response.json()

    # Validar estrutura
    assert 'campaigns' in data
    assert 'total_campaigns' in data
    assert 'data_source' in data

    # Validar valores
    assert data['data_source'] == 'facebook-ads-ai-agent'
    assert isinstance(data['campaigns'], list)
    assert data['total_campaigns'] == len(data['campaigns'])

    # Validar schema Pydantic
    validated = ExportedMetricsResponse(**data)
    assert validated.data_source == 'facebook-ads-ai-agent'


def test_client_library_integration(api_config, test_dates):
    """Testa integração usando biblioteca cliente"""
    from marketing_shared.utils.api_client import AgentAPIClient

    client = AgentAPIClient(
        base_url=api_config['base_url'],
        api_key=api_config['api_key'],
        timeout=30
    )

    # Test health check
    assert client.health_check() == True

    # Test get_metrics
    response = client.get_metrics(
        date_from=test_dates['date_from'],
        date_until=test_dates['date_until']
    )

    assert 'campaigns' in response
    assert 'total_campaigns' in response
```

---

## 8. Critérios de Aceitação

### ✅ Fase 1: Integração Básica (COMPLETO)

- [x] Shared package instalável
- [x] Schemas Pydantic validados
- [x] Cliente HTTP com retry logic
- [x] Endpoint /api/v1/metrics/export funcional
- [x] Autenticação via API Key
- [x] Rate limiting configurado (1000/h)
- [x] Analytics usa Agent API (não Facebook direto)
- [x] n8n workflow atualizado
- [x] Script Python atualizado
- [x] Testes de integração passando
- [x] Documentação completa

### 📅 Fase 2: Produção (Próximo)

- [ ] Agent API em produção com HTTPS
- [ ] Analytics em produção consumindo Agent API via HTTPS
- [ ] Monitoramento Prometheus + Grafana
- [ ] Alertas Slack configurados
- [ ] Backups automáticos

---

## 9. Troubleshooting

### Problema: Analytics não recebe dados

**Diagnóstico:**
```bash
# 1. Verificar Agent API está UP
curl http://localhost:8000/health

# 2. Testar endpoint manualmente
curl -H "X-API-Key: your_key" \
     "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-17&date_until=2025-10-17"

# 3. Verificar API key
cat analytics/scripts/.env | grep ANALYTICS_API_KEY
cat api/.env | grep ANALYTICS_API_KEY
# Devem ser iguais!

# 4. Ver logs Agent API
docker logs marketing-agent-api | tail -50

# 5. Ver logs Analytics
docker logs marketing-celery-worker | tail -50
```

### Problema: Rate limit excedido

**Solução:**
```python
# Aumentar limite em api/src/api/metrics.py
@limiter.limit("2000/hour")  # Era 1000/hour
```

### Problema: Timeout

**Solução:**
```python
# Aumentar timeout no cliente
client = AgentAPIClient(
    base_url=os.getenv('AGENT_API_URL'),
    api_key=os.getenv('ANALYTICS_API_KEY'),
    timeout=60  # Era 30s
)
```

---

## 10. Roadmap

### Q4 2025
- [x] Integração básica implementada
- [x] Testes passando
- [x] Documentação completa
- [ ] Produção com HTTPS

### Q1 2026
- [ ] Webhook reverso (Agent API → Analytics)
- [ ] Streaming de métricas (SSE/WebSocket)
- [ ] Cache compartilhado (Redis)

### Q2 2026
- [ ] GraphQL API (alternativa REST)
- [ ] gRPC para alta performance

---

## 11. Referências

- [PRD-AGENT-API.md](PRD-AGENT-API.md) - PRD do Agent API
- [PRD-ANALYTICS.md](PRD-ANALYTICS.md) - PRD do Analytics
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada
- [INTEGRATION-GUIDE.md](INTEGRATION-GUIDE.md) - Guia técnico
- [../README.md](../README.md) - Documentação principal

---

**Última atualização:** 18 de Outubro, 2025
**Versão:** 1.0.0
**Status (histórico):** Reflete a integração conforme 18/10/2025. Consulte `README.md` e `RELATORIO-CORRECOES-PENDENTES.md` para a situação corrente.
