# Marketing Shared Package

Pacote Python compartilhado entre Agent API e Analytics.

## Instalação

```bash
pip install -e .
```

## Uso

```python
from marketing_shared.schemas.facebook_metrics import CampaignMetricSchema
from marketing_shared.utils import AgentAPIClient, get_facebook_api_client

# Criar cliente
client = AgentAPIClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Buscar métricas
metrics = client.get_metrics(
    date_from="2025-10-18",
    date_until="2025-10-18"
)

# Reutilizar wrapper do Facebook Graph
facebook_client = get_facebook_api_client()
```

## Estrutura

```
marketing_shared/
├── schemas/
│   └── facebook_metrics.py    # Schemas Pydantic
├── utils/
│   ├── api_client.py          # Cliente HTTP (Agent API)
│   └── facebook_client.py     # Wrapper compartilhado do Facebook Graph
└── config/
    └── integration.py          # Configurações
```

