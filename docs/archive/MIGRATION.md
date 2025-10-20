# Guia de Migração - Marketing Automation Platform

Para usuários que já usam os projetos separados.

## Pré-Migração

### 1. Backup

Os backups já foram criados automaticamente:
- `C:\Users\marco\Macspark\facebook-ads-ai-agent.backup\`
- `C:\Users\marco\Macspark\Agente Facebook.backup\`

### 2. Exportar configurações atuais

```bash
# Salvar .env atuais (se existirem)
cd C:\Users\marco\Macspark\facebook-ads-ai-agent
if (Test-Path .env) { Copy-Item .env .env.backup }

cd "C:\Users\marco\Macspark\Agente Facebook\scripts"
if (Test-Path .env) { Copy-Item .env .env.backup }
```

## Migração

### 1. Navegar para o novo projeto

```bash
cd C:\Users\marco\Macspark\marketing-automation
```

### 2. Configure credenciais

```bash
# Copie o template
Copy-Item env.template .env

# Edite com suas credenciais:
# - FACEBOOK_* (se tinha no projeto antigo)
# - SUPABASE_* (do Agente Facebook)
# - GOOGLE_* (do Agente Facebook)
# - Gere nova ANALYTICS_API_KEY
```

### 3. Gerar API Keys

```powershell
# PowerShell
function Generate-RandomKey {
    $bytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    [Convert]::ToBase64String($bytes) -replace '[/+=]', ''
}

Write-Host "ANALYTICS_API_KEY=$(Generate-RandomKey)"
Write-Host "SECRET_KEY=$(Generate-RandomKey)"
Write-Host "SUPERSET_SECRET_KEY=$(Generate-RandomKey)"
```

### 4. Execute setup

```bash
.\scripts\setup.ps1
```

### 5. Importar workflows n8n

- Acesse: https://fluxos.macspark.dev
- Importe workflows de `analytics/n8n-workflows/`
- Configure credenciais (AGENT_API_URL, ANALYTICS_API_KEY)
- Teste execução manual

### 6. Validar

```bash
# Health check
.\scripts\health-check.ps1

# Validação completa
python scripts\validate-integration.py
```

## Diferenças do Sistema Anterior

### Meta Ads

**Antes:**
- analytics/ chamava Facebook API diretamente
- Duplicação de coleta (se API também coletava)

**Agora:**
- Apenas API coleta do Facebook
- Analytics busca do endpoint /api/v1/metrics/export
- Dados consistentes entre sistemas

### Configuração

**Antes:**
- `META_ACCESS_TOKEN` e `META_AD_ACCOUNT_ID` em analytics/
- Credenciais em 2 lugares

**Agora:**
- `META_*` apenas em api/
- `ANALYTICS_API_KEY` para comunicação
- Centralizado

### Workflows n8n

**Antes:**
- Node: Facebook Graph API

**Agora:**
- Node: HTTP Request
- URL: Agent API
- Auth: X-API-Key

## Rollback (se necessário)

### Reverter para projetos antigos:

```bash
# Os projetos originais ainda existem em:
# - C:\Users\marco\Macspark\facebook-ads-ai-agent\
# - C:\Users\marco\Macspark\Agente Facebook\

# Para usar novamente:
cd C:\Users\marco\Macspark\facebook-ads-ai-agent
# Configure e execute como antes

cd "C:\Users\marco\Macspark\Agente Facebook"
# Workflows n8n continuam funcionando
```

## Pós-Migração

### 1. Monitorar por 24-48h

- Verificar logs do Agent API
- Confirmar que workflows n8n executam
- Validar dados no Supabase
- Verificar notificações Slack

### 2. Remover backups (após validação completa)

```bash
# Apenas após confirmar que tudo funciona por vários dias!
# Remove-Item -Recurse "C:\Users\marco\Macspark\facebook-ads-ai-agent.backup"
# Remove-Item -Recurse "C:\Users\marco\Macspark\Agente Facebook.backup"
```

### 3. Atualizar documentação interna

- URLs de acesso atualizados
- Procedimentos de deploy
- Runbooks

## Suporte

Se encontrar problemas:
1. Consulte [INTEGRATION-GUIDE.md](docs/INTEGRATION-GUIDE.md)
2. Verifique logs
3. Execute `python scripts/validate-integration.py`

---

**Versão:** 1.0.0  
**Data:** 2025-10-18

