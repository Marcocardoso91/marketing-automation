# Setup Banco de Dados - Marketing Automation

## 🎯 Objetivo

Configurar banco de dados PostgreSQL e executar migrations para o projeto `marketing-automation`.

---

## ⚠️ Problema Atual (P0 #6)

**Status**: Banco de dados **NÃO configurado**
- ❌ Banco `facebook_ads_ai` não existe
- ❌ Tabela `users` não existe
- ❌ Migrations nunca foram executadas
- ❌ Projeto não está em produção

---

## 🔧 Setup Desenvolvimento Local

### 1. Instalar PostgreSQL

```bash
# Opção A: Docker (Recomendado)
docker run -d \
  --name postgres-marketing \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=facebook_ads_ai \
  -p 5432:5432 \
  postgres:15-alpine

# Opção B: Instalação nativa
# Windows: https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt install postgresql
```

### 2. Criar banco de dados

```bash
# Via Docker
docker exec -it postgres-marketing psql -U postgres -c "CREATE DATABASE facebook_ads_ai;"

# Via psql nativo
psql -U postgres -c "CREATE DATABASE facebook_ads_ai;"
```

### 3. Configurar variáveis de ambiente

Edite [api/.env](api/.env):

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/facebook_ads_ai

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your_secret_key_here  # Gere com: python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Instalar dependências Python

```bash
cd api
pip install -r requirements.txt
```

### 5. Executar migrations

```bash
cd api

# Verificar migrations disponíveis
alembic history

# Executar todas migrations
alembic upgrade head

# Verificar status
alembic current
```

**Saída esperada**:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_schema, initial schema
INFO  [alembic.runtime.migration] Running upgrade 001_initial_schema -> 002_add_user_auth_fields, add hashed password and active flag to users
```

### 6. Verificar tabelas criadas

```bash
# Via Docker
docker exec -it postgres-marketing psql -U postgres -d facebook_ads_ai -c "\dt"

# Deve listar:
# - users
# - conversation_memory
# - alembic_version
```

---

## 🚀 Setup Produção (VPS)

### 1. Criar banco no PostgreSQL de produção

```bash
# SSH no VPS
ssh marcocardoso@217.196.62.130

# Criar banco
docker exec postgres-prd psql -U postgres -c "CREATE DATABASE facebook_ads_marketing;"

# Criar usuário específico (recomendado)
docker exec postgres-prd psql -U postgres <<SQL
CREATE USER marketing_app WITH ENCRYPTED PASSWORD 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON DATABASE facebook_ads_marketing TO marketing_app;
SQL
```

### 2. Configurar .env de produção

```bash
# No servidor VPS
DATABASE_URL=postgresql+asyncpg://marketing_app:senha_forte@postgres-prd:5432/facebook_ads_marketing
REDIS_URL=redis://redis-prd:6379/1  # Use DB 1 para separar do n8n
SECRET_KEY=<gere_uma_chave_nova_e_secreta>
ENVIRONMENT=production
DEBUG=False
```

### 3. Executar migrations em produção

```bash
# Via container do app (quando fizer deploy)
docker exec marketing-api alembic upgrade head

# Ou via SSH tunnel
ssh -L 5433:postgres-prd:5432 marcocardoso@217.196.62.130
DATABASE_URL=postgresql+asyncpg://marketing_app:senha@localhost:5433/facebook_ads_marketing alembic upgrade head
```

---

## 📋 Migrations Disponíveis

### 001_initial_schema
Cria estrutura inicial:
- Tabela `users` (id, email, name, created_at, updated_at)
- Tabela `conversation_memory`
- Índices e constraints

### 002_add_user_auth_fields
Adiciona autenticação:
- Coluna `hashed_password` (NOT NULL)
- Coluna `is_active` (Boolean, default=True)
- Migration segura (adiciona como nullable, popula, altera para NOT NULL)

---

## 🧪 Testar Setup

### 1. Verificar conexão

```bash
cd api
python -c "
import asyncio
from src.utils.database import get_async_session
from sqlalchemy import text

async def test():
    async for session in get_async_session():
        result = await session.execute(text('SELECT version()'))
        print(result.scalar())
        break

asyncio.run(test())
"
```

### 2. Criar usuário de teste

```bash
python -c "
import asyncio
from src.models.user import User
from src.utils.database import get_async_session
from src.utils.auth import get_password_hash

async def create_test_user():
    async for session in get_async_session():
        user = User(
            email='test@example.com',
            name='Test User',
            hashed_password=get_password_hash('Test123!')
        )
        session.add(user)
        await session.commit()
        print(f'User created: {user.id}')
        break

asyncio.run(create_test_user())
"
```

### 3. Testar API

```bash
# Iniciar servidor
cd api
uvicorn src.main:app --reload

# Em outro terminal, testar endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "New User",
    "password": "SecurePass123!"
  }'
```

---

## 🔄 Criar Nova Migration

Quando adicionar/modificar modelos:

```bash
cd api

# Gerar migration automaticamente
alembic revision --autogenerate -m "descrição da mudança"

# Revisar arquivo gerado em alembic/versions/
# Editar se necessário

# Aplicar migration
alembic upgrade head

# Se errou, voltar
alembic downgrade -1
```

---

## ⚡ Troubleshooting

### Erro: "could not connect to server"

```bash
# Verificar se PostgreSQL está rodando
docker ps | grep postgres

# Verificar logs
docker logs postgres-marketing

# Testar conexão
psql -U postgres -h localhost -p 5432
```

### Erro: "database does not exist"

```bash
# Criar banco manualmente
docker exec -it postgres-marketing psql -U postgres -c "CREATE DATABASE facebook_ads_ai;"
```

### Erro: "ModuleNotFoundError: No module named 'asyncpg'"

```bash
# Instalar dependências
cd api
pip install -r requirements.txt

# Ou instalar apenas asyncpg
pip install asyncpg
```

### Erro: "target database is not up to date"

```bash
# Verificar versão atual
alembic current

# Ver histórico
alembic history

# Executar pending migrations
alembic upgrade head
```

---

## 📊 Checklist de Setup

### Desenvolvimento
- [ ] PostgreSQL instalado e rodando
- [ ] Banco `facebook_ads_ai` criado
- [ ] Redis instalado e rodando
- [ ] Dependências Python instaladas
- [ ] arquivo `.env` configurado
- [ ] Migrations executadas (`alembic upgrade head`)
- [ ] Tabelas criadas (`users`, `conversation_memory`)
- [ ] Usuário de teste criado
- [ ] API inicializando sem erros

### Produção
- [ ] Banco `facebook_ads_marketing` criado no VPS
- [ ] Usuário `marketing_app` criado com permissões
- [ ] `.env` de produção configurado
- [ ] Migrations executadas via SSH ou container
- [ ] Backup configurado
- [ ] Monitoring configurado
- [ ] SSL/TLS habilitado

---

## 🔗 Referências

- Issue P0 #6: [Migration hashed_password](https://github.com/Marcocardoso91/mcp-orchestrator/issues/6)
- Alembic Docs: https://alembic.sqlalchemy.org/en/latest/
- FastAPI + Databases: https://fastapi.tiangolo.com/tutorial/sql-databases/
- PostgreSQL Docker: https://hub.docker.com/_/postgres
