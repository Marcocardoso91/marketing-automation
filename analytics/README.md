# Analytics (Projeto Sabrina) – Visão Atual

Este diretório reúne scripts Python, workflows n8n e documentação que foram produzidos para o “Projeto Sabrina”. Parte do material descreve metas e resultados planejados; mantivemos os arquivos originais para consulta histórica, mas nem tudo está automatizado end-to-end.

## Componentes principais

| Caminho | Descrição | Status |
|---------|-----------|--------|
| `scripts/metrics-to-supabase.py` | Script Python que consome o Agent API (`/api/v1/metrics/export`) e grava métricas no Supabase. | ✅ Funcional |
| `n8n-workflows/` | Workflows n8n (JSON) usados como template. Dependem de uma instância n8n configurada. | ⚠️ Necessário ajustar endpoints/tokens |
| `docs/` | Guias, PRDs e relatórios do Projeto Sabrina (v3.0). | ⚠️ Mistura conteúdo conceitual e prático |
| `README`s auxiliares (`🚀-COMECE-AQUI`, `IMPLEMENTACAO-...`) | Tutoriais para setup completo (≈90 min) | ⚠️ Planejamento histórico |
| `tests/` | Casos de teste básicos para scripts. | ✅ |

## Como usar o script principal

```bash
cd analytics/scripts
pip install -r requirements.txt
cp env.example.txt .env  # editar tokens Agent API / Supabase
python metrics-to-supabase.py
```

> O script espera que o Agent API esteja rodando e que a chave `X-API-Key` esteja configurada em `.env`.

## Sobre a documentação histórica

Os arquivos como `RESUMO-EXECUTIVO-v3.0.md`, `IMPLEMENTACAO-v3.0-COMPLETA.md` e PRDs descrevem a visão completa do projeto (metas de seguidores, ROI, automações multi-fonte etc.). Use-os como material de referência, mas verifique o status real antes de executar:

- **Notion Workspace / Supabase / Slack**: requerem criação manual das credenciais.  
- **MCP (Notion/n8n)**: ver `api/docs/MCP-INTEGRATION.md` para um guia atualizado sobre como disponibilizar essas integrações para agentes.

## Próximos passos sugeridos

1. Ajustar os workflows n8n ao ambiente atual (URLs, tokens, frequência).  
2. Revisar os guias de setup (`docs/`) e marcar o que está 100% automatizado vs. o que ainda demanda intervenção manual.  
3. Consolidar resultados reais em `RESUMO-EXECUTIVO` e `Linha de Base` quando houver dados atualizados.  
4. Avaliar a migração de ROTINAS para MCP conforme a necessidade do agente.

## Recursos úteis

- `IMPLEMENTACAO-v3.0-COMPLETA.md` – passo a passo detalhado do Projeto Sabrina (histórico).  
- `VALIDACAO-COMPLETA-v3.0.md` – relatório de validação original.  
- `api/docs/MCP-INTEGRATION.md` – integração com agentes via MCP (atual).  
- `shared/README.md` – como instalar/utilizar o pacote `marketing_shared`.

---

> Em caso de dúvidas, priorize a documentação em `docs/` e o guia de MCP no diretório da API. As seções de resultados/ROI representam o estudo original do projeto, ainda útil como material de referência.
