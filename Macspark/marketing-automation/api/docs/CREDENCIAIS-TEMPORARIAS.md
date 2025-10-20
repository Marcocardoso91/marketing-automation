# ⚠️ Credenciais Temporárias - SOMENTE PARA DESENVOLVIMENTO

## 🚨 ATENÇÃO: SEGURANÇA

Este documento lista os requisitos de credenciais para **desenvolvimento e testes**.  
As credenciais estáticas anteriormente embutidas no código foram removidas.

**⚠️ NUNCA USE EM PRODUÇÃO!**

---

## 🔑 Autenticação Local

### Login temporário removido

- `admin@macspark.dev / admin123` não existe mais.
- `/api/v1/auth/login` exige usuários persistidos na tabela `users` com senha **bcrypt**.

### Como criar um usuário local

1. Gere um hash seguro:
   ```bash
   python - <<'PY'
   from passlib.context import CryptContext
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   print(pwd_context.hash("trocar-essa-senha"))
   PY
   ```
2. Insira o registro no Postgres:
   ```sql
   INSERT INTO users (id, email, name, hashed_password, is_active)
   VALUES ('user-local-admin', 'admin@local.dev', 'Admin Local', '<hash_aqui>', true);
   ```
3. Faça login com POST `/api/v1/auth/login` usando o e-mail e a senha definidos.

> ⚠️ Gere hashes exclusivos por ambiente. Nunca reutilize exemplos.

### Rotação e revogação

- `/api/v1/auth/change-password` atualiza o hash e coloca o token atual na blacklist.
- Para ambientes produtivos, configure Redis para persistir tokens revogados (ver `src/utils/security.py`).

### Exportar usuário de teste

```sql
COPY (
    SELECT id, email, name, hashed_password, is_active
    FROM users WHERE email = 'admin@local.dev'
) TO STDOUT WITH CSV HEADER;
```

---

## 📋 Checklist de Produção

Antes do deploy:

- [ ] Garantir que não existam credenciais hardcoded no código.
- [ ] Criar usuários via migração/seed com senhas hashed.
- [ ] Gerar um novo `SECRET_KEY` (mínimo 64 chars).
- [ ] Renovar todos tokens de integrações externas.
- [ ] Ativar HTTPS obrigatório.
- [ ] Habilitar 2FA/OAuth se disponível.
- [ ] Validar que `.env` não está versionado.

---

## 🔒 Credenciais Reais Necessárias

### Facebook API
```bash
FACEBOOK_APP_ID=<obtido em developers.facebook.com>
FACEBOOK_APP_SECRET=<obtido em developers.facebook.com>
FACEBOOK_ACCESS_TOKEN=<gerado no Graph API Explorer>
FACEBOOK_AD_ACCOUNT_ID=act_<seu_id>
```

### Notion
```bash
NOTION_API_TOKEN=<renovar em notion.so/my-integrations>
NOTION_DATABASE_ID=<ID do database criado>
```

### n8n
```bash
N8N_API_KEY=<renovar em fluxos.macspark.dev/settings/api>
N8N_BASIC_AUTH_USER=<definir no .env>
N8N_BASIC_AUTH_PASSWORD=<senha forte>
```

### Slack
```bash
SLACK_WEBHOOK_URL=<webhook configurado no Slack>
```

---

## ⚠️ IMPORTANTE

1. Nunca commitar credenciais reais.
2. Sempre usar `.env` + secret manager.
3. Rotacionar credenciais periodicamente.
4. Auditar acessos (Git, CI/CD, servidores) após cada rotação.

---

**Última atualização:** 15/05/2024  
**Status:** ✅ Login hardcoded removido  
**Próximo passo:** Automatizar criação de usuários via seed/migração
