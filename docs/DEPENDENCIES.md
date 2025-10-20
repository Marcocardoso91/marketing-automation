# Dependências e Requirements

Este documento consolida os arquivos de dependências existentes no monorepo e explica quando utilizar cada um.

## Visão Geral

| Caminho | Uso | Observações |
|---------|-----|-------------|
| `api/requirements.txt` | Ambiente da Agent API (FastAPI + Celery + tests). | Necessário para rodar os serviços web e as tasks. |
| `analytics/scripts/requirements.txt` | Scripts Python (ex.: `metrics-to-supabase.py`). | Install apenas quando for executar os scripts localmente. |
| `analytics/scripts/requirements-dev.txt` | Dependências adicionais de desenvolvimento para os scripts. | Opcional. |
| `shared/pyproject.toml` | Pacote `marketing_shared` (instalável via `pip install -e shared`). | Fornece schemas/utilitários compartilhados. |
| `analytics/scripts/env.example.txt` | Modelo de variáveis de ambiente para os scripts. | Copiar para `.env` e ajustar tokens. |

## Recomendações

1. **Isolar ambientes**: crie virtualenvs separados para `api/` e `analytics/` quando precisar trabalhar nos dois componentes simultaneamente.
2. **Instalação local do pacote compartilhado**:
   ```bash
   pip install -e shared
   ```
3. **Documentar versões**: atualizações nas dependências devem ser refletidas no changelog ou nos PRDs relevantes.

## Próximos Passos

Futuramente, se desejado, é possível agrupar os arquivos em uma pasta `requirements/` ou gerar `requirements.lock` para pipelines. Por enquanto, os arquivos permanecem em seus subprojetos para manter a compatibilidade com os scripts e serviços existentes.
