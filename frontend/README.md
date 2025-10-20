# Frontend - Marketing Automation Platform

**Status:** Em planejamento

## Visão Geral

Este diretório está reservado para o frontend da plataforma quando for desenvolvido.

## Interfaces Atuais

No momento, o projeto utiliza interfaces prontas:

- **FastAPI Swagger UI** (http://localhost:8000/docs) - Documentação interativa da API
- **Apache Superset** (http://localhost:8088) - Dashboards de BI
- **Grafana** (http://localhost:3000) - Monitoramento (opcional)

## Planejamento Futuro

Quando houver necessidade de uma interface customizada, este será o local para:

- Dashboard personalizado para gestão de campanhas
- Interface de configuração simplificada
- Visualizações customizadas de métricas
- Gerenciamento de usuários e permissões

## Stack Sugerido

- **Framework:** Next.js ou React
- **UI Components:** shadcn/ui ou Material-UI
- **State Management:** Zustand ou Redux Toolkit
- **Charts:** Recharts ou Chart.js
- **API Client:** Axios com React Query

## Integração

O frontend consumirá a API REST do backend disponível em `/api/v1/`.

Para desenvolvimento local:
```bash
# Backend já rodando em http://localhost:8000
# Frontend poderá rodar em http://localhost:3000
```

