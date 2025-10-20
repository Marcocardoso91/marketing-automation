<!-- 57136b43-78a3-4dd0-a61f-8b5c8f697daa 6baad430-e763-4982-b1ea-c655802f189f -->
# Plano: Facebook API + Correções Críticas de Segurança

## FASE 1: CONECTAR FACEBOOK API (HOJE - 30 min)

### Objetivo

Sistema funcionando end-to-end com alertas reais de campanhas do Facebook

### 1.1 Obter Credenciais Facebook (15 min)

**Você precisa obter 4 credenciais:**

1. **App ID e App Secret**

   - Acesse: https://developers.facebook.com/apps
   - Se não tem app, crie novo: "Create App" → "Business" → Nome: "Facebook Ads AI Agent"
   - Vá em "Settings" → "Basic"
   - Copie: App ID e App Secret

2. **Access Token**

   - No mesmo app, vá em "Tools" → "Graph API Explorer"
   - Permissões necessárias: `ads_read`, `ads_management`, `business_management`
   - Clique "Generate Access Token"
   - IMPORTANTE: Token de teste expira em 1h. Para produção, gere User Token de longa duração
   - Copie o token

3. **Ad Account ID**

   - Acesse: https://business.facebook.com/settings/ad-accounts
   - Copie o ID da conta (formato: `act_123456789`)

### 1.2 Configurar Credenciais no .env (5 min)

Adicionar ao arquivo `.env` (que já existe com outras configs):

```bash
# Facebook API - CONFIGURAÇÃO REAL
FACEBOOK_APP_ID=seu_app_id_aqui
FACEBOOK_APP_SECRET=seu_app_secret_aqui
FACEBOOK_ACCESS_TOKEN=seu_token_aqui
FACEBOOK_AD_ACCOUNT_ID=act_123456789
```

### 1.3 Testar Conexão (10 min)

Criar script de teste: `scripts/test_facebook_connection.py`

```python
#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Carregar .env
env_file = project_root / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

from src.agents.facebook_agent import FacebookAdsAgent

async def test():
    print("Testando conexão com Facebook API...")
    
    agent = FacebookAdsAgent()
    
    # Testar listagem de campanhas
    campaigns = await agent.get_campaigns()
    print(f"[OK] Encontradas {len(campaigns)} campanhas")
    
    if campaigns:
        # Testar insights da primeira campanha
        first = campaigns[0]
        print(f"Campanha: {first['name']} (ID: {first['id']})")
        
        insights = await agent.get_campaign_insights(first['id'])
        if insights:
            print(f"[OK] Insights: CTR={insights.get('ctr')}%, CPA=R${insights.get('cpa')}")
    
    print("[OK] Facebook API funcionando!")

if __name__ == "__main__":
    asyncio.run(test())
```

Executar: `python scripts/test_facebook_connection.py`

**Resultado esperado:** Lista de campanhas + insights

---

## FASE 2: CORREÇÕES CRÍTICAS DE SEGURANÇA (2 DIAS - 10h)

### DIA 1 - Manhã (2h)

#### 2.1 Rotação de Credenciais (30 min)

**Problema:** Credenciais expostas no código/git

**Ações:**

1. Verificar se `.env` está no git: `git ls-files .env`
2. Se sim, remover: `git rm --cached .env` + commit
3. Gerar novo SECRET_KEY: `openssl rand -hex 32`
4. Atualizar `.env` com novo SECRET_KEY
5. Renovar Notion token: https://notion.so/my-integrations
6. Renovar n8n API key: https://fluxos.macspark.dev/settings/api

**Arquivo:** `.env`

```bash
SECRET_KEY=<resultado_do_openssl>
NOTION_API_TOKEN=<novo_token>
N8N_API_KEY=<nova_key>
```

**Validação:**

```bash
grep -r "ntn_44266321668" src/  # Deve retornar vazio
grep -r "change-me-in-production" src/  # Deve retornar vazio
```

#### 2.2 Corrigir Testes Falhando (15 min)

**Problema:** Import de classe inexistente quebra suite

**Arquivo:** `tests/unit/test_facebook_agent.py` linha 10

Trocar:

```python
from src.agents.facebook_agent import FacebookAdsAgent, CampaignInsight
```

Por:

```python
from src.agents.facebook_agent import FacebookAdsAgent
```

**Validação:** `pytest tests/unit/test_facebook_agent.py -v` → Todos passando

#### 2.3 CORS Seguro (15 min)

**Problema:** `allow_origins=["*"]` permite qualquer origem

**Arquivo:** `main.py` linhas 42-48

Substituir seção CORS por:

```python
from src.utils.config import settings

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
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)
```

**Validação:** Verificar que `allow_origins` não é mais `["*"]`

---

### DIA 1 - Tarde (4h)

#### 2.4 Implementar Autenticação JWT (4h)

**Problema:** Endpoints desprotegidos

**2.4.1 Criar módulo de autenticação (1h)**

**Arquivo:** `src/utils/auth.py` (novo)

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
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    return verify_token(credentials.credentials)
```

**2.4.2 Criar endpoints de auth (1h)**

**Arquivo:** `src/api/auth.py` (novo)

```python
"""Authentication endpoints"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from src.utils.auth import create_access_token, get_current_user
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
    # Temporário - trocar por lookup em database
    if request.email == "admin@macspark.dev" and request.password == "admin123":
        token = create_access_token(data={"sub": request.email})
        logger.info(f"User {request.email} logged in")
        return LoginResponse(access_token=token)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user.get("sub")}
```

**2.4.3 Adicionar ao main.py (30 min)**

**Arquivo:** `main.py`

Adicionar import:

```python
from src.api import campaigns, analytics, automation, chat, notion, n8n_admin, auth
```

Adicionar router:

```python
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
```

**2.4.4 Proteger endpoints críticos (1h30min)**

**Arquivos:** `src/api/automation.py`, `src/api/analytics.py`

Adicionar em cada endpoint crítico:

```python
from src.utils.auth import get_current_user
from fastapi import Depends

@router.post("/pause-underperforming")
async def pause_underperforming(
    current_user: dict = Depends(get_current_user),  # ADICIONAR
    # ... resto
):
```

Endpoints a proteger:

- `/api/v1/automation/*` - todos
- `/api/v1/analytics/performance` 
- `/api/v1/analytics/trends`

**Validação:**

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@macspark.dev","password":"admin123"}'

# Copiar token

# 2. Testar sem token (deve retornar 401)
curl http://localhost:8000/api/v1/automation/pause-underperforming

# 3. Testar com token (deve funcionar)
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

### DIA 2 - Manhã (2h)

#### 2.5 Rate Limiting (2h)

**Problema:** Sem proteção contra abuso

**2.5.1 Instalar dependência (10 min)**

```bash
pip install slowapi
pip freeze | grep slowapi >> requirements.txt
```

**2.5.2 Criar módulo (20 min)**

**Arquivo:** `src/utils/rate_limit.py` (novo)

```python
"""Rate limiting utilities"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
```

**2.5.3 Configurar no main.py (10 min)**

**Arquivo:** `main.py`

Adicionar:

```python
from src.utils.rate_limit import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

**2.5.4 Aplicar em endpoints (1h20min)**

**Arquivos:** `src/api/campaigns.py`, `src/api/automation.py`, etc

Adicionar em cada router:

```python
from fastapi import Request
from src.utils.rate_limit import limiter

@router.get("/")
@limiter.limit("100/minute")
async def list_campaigns(request: Request, ...):
```

Limites recomendados:

- GET endpoints: 100/minuto
- POST/PUT/DELETE: 10/minuto
- Login: 5/minuto

**Validação:**

```bash
# Fazer 105 requests em 1 minuto - deve retornar 429 após 100
for i in {1..105}; do curl http://localhost:8000/api/v1/campaigns; done
```

---

### DIA 2 - Tarde (2h)

#### 2.6 Testes de Segurança (2h)

**2.6.1 Executar Bandit (30 min)**

```bash
pip install bandit
bandit -r src/ -ll -f json -o security-report-bandit.json
bandit -r src/ -ll  # Ver no terminal
```

Corrigir issues ALTA prioridade encontrados

**2.6.2 Executar Safety (30 min)**

```bash
pip install safety
safety check --json > security-report-safety.json
```

Atualizar pacotes vulneráveis se houver

**2.6.3 Validação Final (1h)**

Criar checklist de validação:

```bash
# 1. Credenciais
[ ] SECRET_KEY diferente de "change-me-in-production"
[ ] Nenhuma credencial hardcoded no código
[ ] .env não está no git

# 2. Testes
[ ] pytest tests/unit -v → All passing
[ ] pytest tests/integration -v → All passing

# 3. CORS
[ ] allow_origins não é ["*"]
[ ] Apenas domínios específicos permitidos

# 4. Autenticação
[ ] POST /api/v1/auth/login retorna token
[ ] Endpoints protegidos retornam 401 sem token
[ ] Endpoints protegidos funcionam com token

# 5. Rate Limiting
[ ] Requests acima do limite retornam 429
[ ] Header "Retry-After" presente

# 6. Security Scans
[ ] Bandit: 0 HIGH issues
[ ] Safety: 0 vulnerabilidades críticas
```

---

## FASE 3: DOCUMENTAR MELHORIAS FUTURAS (1h)

### 3.1 Criar arquivo de roadmap

**Arquivo:** `ROADMAP-MELHORIAS.md` (novo)

Documentar melhorias do plano original da IA que ficaram para depois:

- Dependency Injection (Fase 3.1 do plano original)
- LangChain para NLP (Fase 3.2)
- Circuit Breakers (Fase 3.3)
- Caching Redis (Fase 3.4)
- Expandir cobertura de testes para 85% (Fase 2.2)
- Testes E2E (Fase 2.4)
- Features: Auto-apply, PDFs (Fase 5)
- Backup automatizado (Fase 4.2)
- Monitoring avançado (Fase 4.3)

Para cada item:

- Prioridade (Alta/Média/Baixa)
- Tempo estimado
- Dependências
- Link para seção específica do PLANO-CORRECAO-COMPLETO.md

---

## RESUMO DO PLANO

### Tempo Total: ~13.5 horas distribuídas em 2-3 dias

**HOJE (30 min):**

- Conectar Facebook API
- Testar campanhas reais
- Sistema funcionando end-to-end

**DIA 1 (6h):**

- Manhã: Rotação credenciais + Corrigir testes + CORS (1h)
- Tarde: Implementar JWT completo (4h)

**DIA 2 (4h):**

- Manhã: Rate Limiting (2h)
- Tarde: Testes de segurança (2h)

**Depois (1h):**

- Documentar roadmap de melhorias futuras

### Resultado Esperado

**Após HOJE:**

- ✅ Facebook API conectado
- ✅ Alertas reais funcionando
- ✅ WhatsApp + Slack + Notion + Facebook integrados

**Após 2 dias:**

- ✅ Segurança: 4/10 → 8/10
- ✅ Credenciais seguras
- ✅ Autenticação JWT ativa
- ✅ CORS restrito
- ✅ Rate limiting ativo
- ✅ 0 vulnerabilidades críticas

**Melhorias futuras documentadas para implementar conforme necessário**

### To-dos

- [ ] Conectar Facebook API e testar conexão
- [ ] Implementar correções críticas de segurança (10h em 2 dias)
- [ ] Documentar melhorias futuras do plano original