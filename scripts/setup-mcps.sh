#!/usr/bin/env bash
set -euo pipefail

# Setup de MCPs via Claude CLI, sem remover os existentes.
# Lê variáveis de .env.mcp se existir.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env.mcp"

if [[ -f "$ENV_FILE" ]]; then
  echo "[setup-mcps] Carregando variáveis de $ENV_FILE"
  # shellcheck disable=SC1090
  source "$ENV_FILE"
else
  echo "[setup-mcps] Aviso: $ENV_FILE não encontrado. Algumas integrações podem falhar sem chaves."
fi

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "[erro] Comando requerido não encontrado: $1"; exit 1; }
}

need_cmd claude

echo "[setup-mcps] Adicionando MCPs HTTP (Smithery/Remotos)"

# Exa Search (HTTP)
claude mcp add --transport http exa-search "https://server.smithery.ai/exa/mcp?api_key=${SMITHERY_API_KEY:-}" || true

# Context7 (HTTP)
claude mcp add --transport http context7 "https://server.smithery.ai/@upstash/context7-mcp/mcp?api_key=${SMITHERY_API_KEY:-}" || true

# Github (HTTP)
claude mcp add --transport http github "https://server.smithery.ai/@smithery-ai/github/mcp?api_key=${SMITHERY_API_KEY:-}" || true

# Docker (HTTP)
claude mcp add --transport http docker "https://server.smithery.ai/docker-mcp/mcp?api_key=${SMITHERY_API_KEY:-}" || true

# Sequential Thinking (HTTP)
claude mcp add --transport http sequential-thinking "https://server.smithery.ai/@smithery-ai/server-sequential-thinking/mcp?api_key=${SMITHERY_API_KEY:-}&profile=${SMITHERY_PROFILE:-}" || true

echo "[setup-mcps] Adicionando MCPs STDIO (npx)"

# Playwright Automation (STDIO via Smithery CLI)
claude mcp add --transport stdio playwright-automation -- \
  npx -y @smithery/cli@latest run @microsoft/playwright-mcp --key "${SMITHERY_API_KEY:-}" || true

# TestSprite (STDIO)
if [[ -n "${TESTSPRITE_API_KEY:-}" ]]; then
  claude mcp add --transport stdio testsprite --env API_KEY="${TESTSPRITE_API_KEY}" -- \
    npx -y @testsprite/testsprite-mcp@latest || true
else
  echo "[setup-mcps] Pulando TestSprite: TESTSPRITE_API_KEY ausente"
fi

echo "[setup-mcps] Notion MCP"

# Preferimos o servidor oficial STDIO (mais confiável para tokens locais)
if [[ -n "${NOTION_TOKEN:-}" ]]; then
  claude mcp add --transport stdio notion --env NOTION_TOKEN="${NOTION_TOKEN}" -- \
    npx -y @notionhq/notion-mcp-server || true
else
  echo "[setup-mcps] NOTION_TOKEN ausente; tentando endpoint HTTP público (pode exigir auth adicional)"
  claude mcp add --transport http notion "https://mcp.notion.com/mcp" || true
fi

echo "[setup-mcps] Supabase MCP (HTTP com Authorization header)"
if [[ -n "${SUPABASE_BEARER:-}" && -n "${SUPABASE_PROJECT_REF:-}" ]]; then
  claude mcp add --transport http -H "Authorization: Bearer ${SUPABASE_BEARER}" supabase \
    "https://mcp.supabase.com/mcp?project_ref=${SUPABASE_PROJECT_REF}" || true
else
  echo "[setup-mcps] Pulando Supabase: SUPABASE_BEARER/PROJECT_REF ausentes"
fi

echo "[setup-mcps] n8n MCP (STDIO)"
if [[ -n "${N8N_API_URL:-}" && -n "${N8N_API_KEY:-}" ]]; then
  claude mcp add --transport stdio n8n-mcp \
    --env MCP_MODE="${MCP_MODE:-stdio}" \
    --env LOG_LEVEL="${LOG_LEVEL:-info}" \
    --env N8N_API_URL="${N8N_API_URL}" \
    --env N8N_API_KEY="${N8N_API_KEY}" -- \
    npx -y n8n-mcp || true
else
  echo "[setup-mcps] Pulando n8n: N8N_API_URL/N8N_API_KEY ausentes"
fi

echo "[setup-mcps] Lista atual de MCPs registrados:"
claude mcp list || true

echo "[setup-mcps] Concluído."

