# Migração: TokenBlacklist Memória → Redis

## 🎯 Objetivo

Migrar `TokenBlacklist` de armazenamento **em memória** (volátil) para **Redis** (persistente).

## ⚠️ Problema Atual

```python
# api/src/utils/security.py (ANTIGO)
class TokenBlacklist:
    def __init__(self):
        self._blacklist = set()  # ❌ Perde ao reiniciar!
```

**Impacto**: Tokens revogados voltam a funcionar após restart do servidor.

---

## ✅ Solução: Redis

Criado novo módulo: [api/src/utils/redis_blacklist.py](api/src/utils/redis_blacklist.py)

### Versão Redis (Async)

```python
from src.utils.redis_blacklist import get_redis_blacklist

# Em função async
async def my_endpoint():
    blacklist = await get_redis_blacklist()
    await blacklist.add(token, expiry)
    is_blocked = await blacklist.is_blacklisted(token)
```

### Versão Híbrida (Temporária - Sync/Async)

Para código que ainda não foi migrado para async:

```python
from src.utils.redis_blacklist import token_blacklist_redis

# Sync (temporário - tem overhead)
token_blacklist_redis.add_sync(token, expiry)
is_blocked = token_blacklist_redis.is_blacklisted_sync(token)

# Async (recomendado)
await token_blacklist_redis.add(token, expiry)
is_blocked = await token_blacklist_redis.is_blacklisted(token)
```

---

## 📝 Passos de Migração

### Passo 1: Instalar dependência (JÁ INSTALADO ✅)

```bash
# Já está em requirements.txt
redis==5.0.1
```

### Passo 2: Atualizar imports

**ANTES**:
```python
from src.utils.security import token_blacklist
```

**DEPOIS**:
```python
# Opção A: Async (recomendado)
from src.utils.redis_blacklist import get_redis_blacklist

# Opção B: Hybrid (temporário)
from src.utils.redis_blacklist import token_blacklist_redis as token_blacklist
```

### Passo 3: Atualizar chamadas

#### Arquivo: `api/src/utils/auth.py`

**ANTES** (sync):
```python
def verify_token(token: str) -> dict:
    if token_blacklist.is_blacklisted(token):  # ❌ Em memória
        raise HTTPException(...)
```

**OPÇÃO A - Converter para async** (recomendado):
```python
async def verify_token(token: str) -> dict:
    blacklist = await get_redis_blacklist()
    if await blacklist.is_blacklisted(token):  # ✅ Redis
        raise HTTPException(...)
```

**OPÇÃO B - Usar wrapper sync** (temporário):
```python
from src.utils.redis_blacklist import token_blacklist_redis

def verify_token(token: str) -> dict:
    if token_blacklist_redis.is_blacklisted_sync(token):  # ⚠️ Overhead
        raise HTTPException(...)
```

#### Arquivo: `api/src/api/auth.py`

**ANTES**:
```python
@router.post("/change-password")
async def change_password(...):
    # ...
    token_blacklist.add(credentials.credentials, expiry_dt)  # ❌
```

**DEPOIS** (já é async ✅):
```python
@router.post("/change-password")
async def change_password(...):
    # ...
    blacklist = await get_redis_blacklist()
    await blacklist.add(credentials.credentials, expiry_dt)  # ✅
```

---

## 🔄 Migração Completa (Recomendado)

### 1. Atualizar `api/src/utils/auth.py`

```python
# Converter verify_token() para async
async def verify_token(token: str) -> dict:
    """Decode JWT token and ensure it hasn't been revoked"""
    blacklist = await get_redis_blacklist()
    if await blacklist.is_blacklisted(token):
        logger.warning("Attempt to use blacklisted token")
        raise HTTPException(status_code=401, detail="Token has been revoked")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```

### 2. Atualizar dependency em `get_current_user()`

```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> dict:
    """Get current user from JWT token"""
    payload = await verify_token(credentials.credentials)  # ✅ await
    return payload
```

### 3. Atualizar `api/src/api/auth.py`

```python
from src.utils.redis_blacklist import get_redis_blacklist

@router.post("/change-password")
async def change_password(...):
    # ... código existente ...

    # Revogar token atual
    payload = await verify_token(credentials.credentials)  # ✅ await
    expiry_ts = payload.get("exp")
    expiry_dt = datetime.utcfromtimestamp(expiry_ts) if expiry_ts else datetime.utcnow()

    blacklist = await get_redis_blacklist()
    await blacklist.add(credentials.credentials, expiry_dt)  # ✅ await

    logger.info("Password changed for %s", user.email)
```

---

## 🧪 Testes

### Teste Manual (Redis Local)

```bash
# 1. Inicie Redis
docker run -d -p 6379:6379 redis:7-alpine

# 2. Teste com Python
python -c "
import asyncio
from api.src.utils.redis_blacklist import RedisTokenBlacklist
from datetime import datetime, timedelta

async def test():
    bl = RedisTokenBlacklist()

    token = 'test_token_123'
    expiry = datetime.utcnow() + timedelta(hours=1)

    # Adicionar
    await bl.add(token, expiry)
    print(f'Added: {token}')

    # Verificar
    is_blocked = await bl.is_blacklisted(token)
    print(f'Is blacklisted: {is_blocked}')  # True

    # Limpar
    await bl.close()

asyncio.run(test())
"
```

### Teste de Persistência

```bash
# Terminal 1: Adicionar token
python -c "..."  # adiciona token

# Terminal 2: Reiniciar app e verificar
# Token ainda deve estar blacklisted ✅
```

---

## 📊 Comparação

| Aspecto | Memória (Antigo) | Redis (Novo) |
|---------|------------------|--------------|
| **Persistência** | ❌ Perde ao reiniciar | ✅ Persistente |
| **Performance** | ⚡ Rápido (local) | ⚡ Rápido (rede local) |
| **Escalabilidade** | ❌ Não escalável | ✅ Multi-instância |
| **Auto-expiration** | ⚠️ Manual | ✅ TTL nativo |
| **Complexidade** | ✅ Simples | ⚠️ Requer Redis |

---

## ⚡ Checklist de Migração

- [x] Criar `redis_blacklist.py` com implementação Redis
- [ ] Atualizar imports em `api/src/utils/auth.py`
- [ ] Converter `verify_token()` para async
- [ ] Atualizar `get_current_user()` dependency
- [ ] Atualizar `api/src/api/auth.py` (change_password)
- [ ] Testar localmente com Redis
- [ ] Adicionar testes automatizados
- [ ] Atualizar documentação
- [ ] Deploy em staging
- [ ] Validar em produção

---

## 🔗 Referências

- Issue: [#3 - TokenBlacklist em memória](https://github.com/Marcocardoso28/mcp-orchestrator/issues/3)
- Arquivo criado: [api/src/utils/redis_blacklist.py](api/src/utils/redis_blacklist.py)
- Documentação Redis: https://redis.io/docs/manual/keyspace/
- Redis Python Async: https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html
