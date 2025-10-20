# ⚡ QUICK START - Correções Críticas
## Comece AGORA com as 5 correções mais urgentes

**Tempo Total**: 3 horas
**Impacto**: Elimina 80% dos problemas críticos

---

## 🚨 CORREÇÃO #1: Rotação de Credenciais (30 minutos)

### Por que é crítico?
Credenciais REAIS estão expostas no arquivo `.env` que pode estar no git.

### Como corrigir AGORA:

```bash
# 1. Verificar se .env está no git
git ls-files .env

# Se retornar algo, REMOVER IMEDIATAMENTE:
git rm --cached .env
git commit -m "security: remove .env from git"
git push

# 2. Gerar novo SECRET_KEY
openssl rand -hex 32

# Copiar o resultado (ex: 8f3a2c1b9d4e7f6a...)

# 3. Editar .env e substituir SECRET_KEY
# Abrir com seu editor preferido e colar o novo SECRET_KEY

# 4. Rotacionar Notion Token
# Acesse: https://www.notion.so/my-integrations
# Encontre sua integração → "Refresh Token"
# Copie o novo token e atualize NOTION_API_TOKEN no .env

# 5. Rotacionar n8n API Key
# Acesse: https://fluxos.macspark.dev/settings/api
# Delete a key antiga → Crie nova
# Copie e atualize N8N_API_KEY no .env
```

### Validação:
```bash
# Verificar que não há credenciais no código
grep -r "ntn_" src/
grep -r "eyJhbGci" src/

# Resultado esperado: Nenhuma ocorrência
```

✅ **CHECKPOINT**: Credenciais rotacionadas e .env fora do git

---

## 🧪 CORREÇÃO #2: Corrigir Teste Falhando (15 minutos)

### Por que é crítico?
Suite de testes está quebrada, impossibilitando validar o código.

### Como corrigir AGORA:

```bash
# 1. Editar o arquivo de teste
# Abrir: tests/unit/test_facebook_agent.py

# 2. Na linha 10, trocar:
# DE:   from src.agents.facebook_agent import FacebookAdsAgent, CampaignInsight
# PARA: from src.agents.facebook_agent import FacebookAdsAgent

# 3. Salvar e testar
pytest tests/unit/test_facebook_agent.py -v

# Resultado esperado: All tests passing
```

### Código completo da correção:
```python
# tests/unit/test_facebook_agent.py - LINHA 10
# ANTES:
# from src.agents.facebook_agent import FacebookAdsAgent, CampaignInsight

# DEPOIS:
from src.agents.facebook_agent import FacebookAdsAgent
```

✅ **CHECKPOINT**: Testes unitários passando

---

## 🔒 CORREÇÃO #3: CORS Seguro (10 minutos)

### Por que é crítico?
CORS configurado como `*` permite ataques CSRF de qualquer origem.

### Como corrigir AGORA:

```bash
# 1. Editar main.py
# Localizar linhas 42-48 (seção CORS)
```

### Substituir por:
```python
# main.py - ATUALIZAR SEÇÃO CORS

# ANTES (INSEGURO):
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ❌ ACEITA QUALQUER ORIGEM!
#     ...
# )

# DEPOIS (SEGURO):
from src.utils.config import settings

# Definir origins permitidas
allowed_origins = []
if settings.ENVIRONMENT == "development":
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
elif settings.ENVIRONMENT == "production":
    allowed_origins = [
        "https://fbads.macspark.dev",
        "https://api.fbads.macspark.dev",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ✅ APENAS ORIGINS ESPECÍFICAS
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)
```

### Adicionar ao .env:
```bash
echo "ENVIRONMENT=development" >> .env
```

✅ **CHECKPOINT**: CORS restrito a domínios confiáveis

---

## 🛡️ CORREÇÃO #4: Implementar Autenticação JWT Básica (1 hora)

### Por que é crítico?
Todos endpoints estão desprotegidos, qualquer um pode acessar.

### Como corrigir AGORA:

#### Passo 1: Criar módulo de autenticação (20 min)
```bash
# Criar arquivo src/utils/auth.py
```

Copiar este código:
```python
"""Authentication utilities"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.utils.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Get current authenticated user - USE THIS IN PROTECTED ROUTES"""
    token = credentials.credentials
    return verify_token(token)
```

#### Passo 2: Criar endpoint de login (20 min)
```bash
# Criar arquivo src/api/auth.py
```

Copiar este código:
```python
"""Authentication endpoints"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from src.utils.auth import create_access_token, get_current_user
from src.utils.config import settings
from src.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Login endpoint

    Credenciais padrão (TROCAR EM PRODUÇÃO):
    - Email: admin@macspark.dev
    - Password: admin123
    """
    # ATENÇÃO: Isto é temporário! Implementar lookup em database
    if request.email == "admin@macspark.dev" and request.password == "admin123":
        token = create_access_token(data={"sub": request.email})
        logger.info(f"User {request.email} logged in")
        return LoginResponse(access_token=token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou senha incorretos"
    )


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    return {"email": current_user.get("sub")}
```

#### Passo 3: Adicionar ao main.py (5 min)
```python
# main.py - ADICIONAR estas linhas

# No topo, adicionar import:
from src.api import auth

# Depois dos outros routers, adicionar:
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
```

#### Passo 4: Proteger endpoint crítico (15 min)
```python
# src/api/automation.py - EXEMPLO DE PROTEÇÃO

# Adicionar import no topo:
from src.utils.auth import get_current_user
from fastapi import Depends

# Proteger endpoint:
@router.post("/pause-underperforming")
async def pause_underperforming(
    current_user: dict = Depends(get_current_user),  # ← ADICIONAR ESTA LINHA
    # ... resto dos parâmetros
):
    # ... código existente
```

### Testar autenticação:
```bash
# 1. Reiniciar servidor
# Ctrl+C e rodar novamente: uvicorn main:app --reload

# 2. Testar login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@macspark.dev","password":"admin123"}'

# Copiar o access_token retornado

# 3. Testar endpoint protegido
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"

# Deve retornar: {"email":"admin@macspark.dev"}
```

✅ **CHECKPOINT**: Autenticação JWT funcionando

---

## ⚡ CORREÇÃO #5: Rate Limiting (30 minutos)

### Por que é crítico?
Sem rate limiting, API pode ser sobrecarregada por abuso.

### Como corrigir AGORA:

```bash
# 1. Instalar dependência
pip install slowapi
pip freeze | grep slowapi >> requirements.txt

# 2. Criar arquivo src/utils/rate_limit.py
```

Copiar este código:
```python
"""Rate limiting utilities"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
```

### Adicionar ao main.py:
```python
# main.py - ADICIONAR

# Import no topo:
from src.utils.rate_limit import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

# Depois de criar app:
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### Proteger endpoints:
```python
# src/api/campaigns.py - EXEMPLO

# Import no topo:
from fastapi import Request
from src.utils.rate_limit import limiter

# Adicionar rate limit:
@router.get("/")
@limiter.limit("100/minute")  # ← ADICIONAR ESTA LINHA
async def list_campaigns(
    request: Request,  # ← ADICIONAR request como primeiro parâmetro
    # ... resto dos parâmetros
):
    # ... código existente
```

### Testar rate limiting:
```bash
# Fazer múltiplas requests rápidas (>100 em 1 minuto)
for i in {1..105}; do
  curl http://localhost:8000/api/v1/campaigns
done

# Deve retornar erro 429 (Too Many Requests) após 100 requests
```

✅ **CHECKPOINT**: Rate limiting ativo

---

## 📊 RESUMO DAS 5 CORREÇÕES

| # | Correção | Tempo | Impacto |
|---|----------|-------|---------|
| 1 | Rotação credenciais | 30 min | 🔴 Crítico |
| 2 | Corrigir testes | 15 min | 🔴 Crítico |
| 3 | CORS seguro | 10 min | 🔴 Crítico |
| 4 | Autenticação JWT | 60 min | 🔴 Crítico |
| 5 | Rate limiting | 30 min | ⚠️ Alto |
| **TOTAL** | **2h 25min** | **80% problemas resolvidos** |

---

## ✅ CHECKLIST FINAL

Ao completar estas 5 correções, você terá:

- [ ] ✅ Credenciais seguras (não expostas)
- [ ] ✅ Testes funcionando
- [ ] ✅ CORS restrito
- [ ] ✅ Autenticação JWT ativa
- [ ] ✅ Rate limiting configurado

**Nota de Segurança**: 4/10 → 7/10 ⬆️

---

## 🎯 PRÓXIMOS PASSOS

Após completar estas 5 correções críticas, continue com:

1. **Expandir testes** (ver PLANO-CORRECAO-COMPLETO.md - Fase 2)
2. **Refactoring** (Dependency Injection, LangChain)
3. **Deploy para produção** (Configurações finais)

Consulte o documento **PLANO-CORRECAO-COMPLETO.md** para o plano completo de 60 dias.

---

## 🆘 PROBLEMAS?

Se encontrar erros durante a execução:

1. Verifique logs: `tail -f logs/app.log`
2. Teste com: `pytest tests/unit -v`
3. Consulte documentação: `docs/`

**Contato**: marco@macspark.dev

---

**Última atualização**: 18 de Outubro de 2025
