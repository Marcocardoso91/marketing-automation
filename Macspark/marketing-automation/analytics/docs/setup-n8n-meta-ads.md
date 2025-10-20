# 🛠️ Setup N8n - Meta Ads → Notion

## Pré-requisitos

- ✅ N8n instalado e rodando (você já tem em n8n.macspark.dev)
- ✅ Conta Meta Business Manager
- ✅ Conta Notion com workspace ativo
- ✅ Campanhas de ads rodando no Meta

---

## PASSO 1: Obter Access Token do Meta

### 1.1 Criar App no Meta for Developers

1. Acesse: https://developers.facebook.com/apps
2. Clique em **"Criar App"**
3. Escolha tipo: **"Empresa"**
4. Preencha:
   - Nome do app: `N8n Meta Ads Integration`
   - Email de contato: seu email
5. Clique em **"Criar App"**

### 1.2 Adicionar Marketing API

1. No painel do app, clique em **"Adicionar Produto"**
2. Selecione **"Marketing API"**
3. Clique em **"Configurar"**

### 1.3 Gerar Access Token

1. No menu lateral, vá em **"Ferramentas" → "Graph API Explorer"**
2. Selecione seu App no dropdown
3. Em **"Permissões"**, adicione:
   - `ads_read`
   - `ads_management`
   - `business_management`
4. Clique em **"Gerar Token de Acesso"**
5. Faça login com sua conta Facebook Business
6. Autorize as permissões
7. **COPIE O TOKEN** (começa com `EAA...`)

⚠️ **IMPORTANTE:** 
- Token de usuário expira em 1-2 horas
- Você precisa gerar um **Token de Longa Duração** ou **Token de Sistema**

### 1.4 Converter para Token de Longa Duração

Execute esta URL no navegador (substitua os valores):

```
https://graph.facebook.com/v21.0/oauth/access_token?
  grant_type=fb_exchange_token&
  client_id=SEU_APP_ID&
  client_secret=SEU_APP_SECRET&
  fb_exchange_token=SEU_TOKEN_CURTO
```

Resposta:
```json
{
  "access_token": "EAAxxxxx...",
  "token_type": "bearer",
  "expires_in": 5184000
}
```

**COPIE** o novo `access_token` (válido por 60 dias)

### 1.5 Obter Ad Account ID

1. Acesse: https://business.facebook.com/adsmanager
2. No menu superior, você verá: `Conta de anúncios: 123456789`
3. O ID é o número (sem prefixo `act_`)
4. **Formato completo:** `act_123456789`

---

## PASSO 2: Obter Credenciais do Notion

### 2.1 Criar Integration no Notion

1. Acesse: https://www.notion.so/my-integrations
2. Clique em **"+ Nova integração"**
3. Preencha:
   - Nome: `N8n Meta Ads Integration`
   - Workspace: Selecione seu workspace
   - Tipo: Internal Integration
4. Clique em **"Enviar"**
5. **COPIE** o token (começa com `secret_...`)

### 2.2 Compartilhar Database com Integration

1. Abra o database "📊 Métricas & KPIs Diários" no Notion
2. Clique nos **3 pontinhos** (⋯) no canto superior direito
3. Clique em **"Connections"** ou **"Adicionar conexões"**
4. Selecione **"N8n Meta Ads Integration"**
5. Confirme

### 2.3 Obter Database ID

1. Abra o database no Notion
2. Copie a URL completa:
   ```
   https://www.notion.so/e344b2ff2ded4418b93413b9dbd2e131?v=...
   ```
3. O Database ID é: `e344b2ff2ded4418b93413b9dbd2e131`

---

## PASSO 3: Configurar N8n

### 3.1 Acessar N8n

1. Acesse: https://n8n.macspark.dev
2. Faça login

### 3.2 Adicionar Credenciais Meta Ads

1. No menu lateral, clique em **"Credentials"**
2. Clique em **"+ Add Credential"**
3. Busque e selecione: **"Facebook Graph API"**
4. Preencha:
   - Name: `Meta Ads API`
   - Access Token: `SEU_TOKEN_LONGA_DURAÇÃO`
5. Clique em **"Save"**
6. Teste a conexão

### 3.3 Adicionar Credenciais Notion

1. Em **"Credentials"**, clique em **"+ Add Credential"**
2. Busque e selecione: **"Notion API"**
3. Preencha:
   - Name: `Notion API`
   - API Key: `secret_...` (token da integration)
4. Clique em **"Save"**

### 3.4 Configurar Variáveis de Ambiente

1. No N8n, vá em **"Settings" → "Environment Variables"**
2. Adicione:
   ```
   META_AD_ACCOUNT_ID=act_123456789
   NOTION_DATABASE_ID=e344b2ff2ded4418b93413b9dbd2e131
   ```
3. Salve

### 3.5 Importar Workflow

1. No N8n, clique em **"+ Add workflow"**
2. Clique no menu (⋯) → **"Import from File"**
3. Selecione o arquivo: `meta-ads-notion.json`
4. Clique em **"Import"**

### 3.6 Ajustar Credenciais no Workflow

1. Clique no node **"Meta Ads - Buscar Métricas"**
2. Em **"Credential to connect with"**, selecione: `Meta Ads API`
3. Clique no node **"Notion - Criar Registro"**
4. Em **"Credential to connect with"**, selecione: `Notion API`
5. Salve o workflow (Ctrl+S)

---

## PASSO 4: Testar Workflow

### 4.1 Execução Manual

1. Clique em **"Execute Workflow"** (botão play)
2. Aguarde execução
3. Verifique se aparece ✅ verde em todos os nodes
4. Se houver erro ❌, clique no node para ver detalhes

### 4.2 Verificar no Notion

1. Abra o database "📊 Métricas & KPIs Diários"
2. Deve aparecer um novo registro com data de hoje
3. Verifique se os valores fazem sentido

### 4.3 Ativar Schedule

1. No workflow, clique em **"Active"** (toggle no canto superior)
2. Agora roda automaticamente todo dia às 9h

---

## PASSO 5: Monitoramento

### Verificar Execuções

1. No N8n, vá em **"Executions"**
2. Veja histórico de execuções
3. Verde ✅ = sucesso
4. Vermelho ❌ = erro

### Logs

- Cada execução mostra:
  - Horário
  - Status
  - Dados processados
  - Erros (se houver)

---

## 🔧 Troubleshooting

### Erro: "Invalid Access Token"
**Solução:** Token expirou. Gerar novo token de longa duração.

### Erro: "Database not found"
**Solução:** Compartilhar database com a integration no Notion.

### Erro: "No data returned"
**Solução:** 
- Verificar se campanhas estão ativas
- Verificar Ad Account ID correto
- Verificar permissões do token

### Erro: "Rate limit exceeded"
**Solução:** Meta tem limite de requisições. Aguardar 1 hora e tentar novamente.

### Dados não aparecem no Notion
**Solução:**
- Verificar Database ID correto
- Verificar nomes dos campos (case-sensitive)
- Checar se integration tem permissão de escrita

---

## 📝 Manutenção

### Token Meta Ads

- **Validade:** 60 dias
- **Renovar:** A cada 50 dias
- **Como:** Repetir Passo 1.4

### Workflow

- **Backup:** Exportar workflow mensalmente
- **Versão:** Manter cópia do JSON
- **Updates:** Atualizar nodes do N8n regularmente

---

## 🎯 Próximos Passos

Após configurar:

1. ✅ Deixar rodar por 7 dias
2. ✅ Verificar dados diariamente
3. ✅ Ajustar se necessário
4. ✅ Adicionar mais métricas se quiser
5. ✅ Criar alertas no N8n (opcional)

---

## 📞 Suporte

**Documentação Meta Ads API:**
https://developers.facebook.com/docs/marketing-api

**Documentação Notion API:**
https://developers.notion.com

**Documentação N8n:**
https://docs.n8n.io

**Community N8n:**
https://community.n8n.io

---

**Criado:** 18 de Outubro, 2025
**Versão:** 1.0

