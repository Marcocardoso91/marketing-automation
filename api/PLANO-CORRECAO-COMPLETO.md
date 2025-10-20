# 🎯 PLANO DE CORREÇÃO COMPLETO
## Facebook Ads AI Agent - Roadmap de Correções

**Data**: 18 de Outubro de 2025
**Versão**: 1.0
**Responsável**: Equipe de Desenvolvimento
**Prazo Total**: 60 dias úteis (12 semanas)

---

## 📊 RESUMO EXECUTIVO

Este documento detalha o plano completo para corrigir **todos os problemas identificados** na auditoria técnica do projeto Facebook Ads AI Agent.

**Problemas Identificados:**
- 🔴 **5 Críticos** (Segurança e Testes)
- ⚠️ **8 Altos** (Performance e Configuração)
- 🟡 **12 Médios** (Code Quality e Features)

**Impacto Esperado:**
- Nota de Segurança: **4/10 → 9/10**
- Cobertura de Testes: **26% → 85%+**
- Performance: **Melhoria de 40%**
- Production Readiness: **70% → 95%**

---

## 🗓️ CRONOGRAMA GERAL

| Fase | Período | Foco | Status |
|------|---------|------|--------|
| **Fase 0** | Dia 1 | Setup e Preparação | ⏳ Pendente |
| **Fase 1** | Semana 1-2 | Segurança Crítica | ⏳ Pendente |
| **Fase 2** | Semana 3-4 | Testes e Qualidade | ⏳ Pendente |
| **Fase 3** | Semana 5-6 | Refactoring e Performance | ⏳ Pendente |
| **Fase 4** | Semana 7-8 | Configurações de Produção | ⏳ Pendente |
| **Fase 5** | Semana 9-10 | Features Faltantes | ⏳ Pendente |
| **Fase 6** | Semana 11-12 | Validação e Deploy | ⏳ Pendente |

---

# 🚨 FASE 0: SETUP E PREPARAÇÃO (DIA 1)

## Objetivos
- Preparar ambiente de desenvolvimento
- Criar backups de segurança
- Configurar ferramentas de qualidade

## Tarefas

### 0.1 Backup Completo
```bash
# 1. Backup do código atual
cd /c/Users/marco/Macspark
tar -czf facebook-ads-ai-agent-backup-$(date +%Y%m%d).tar.gz facebook-ads-ai-agent/

# 2. Backup do banco de dados (se existir)
cd facebook-ads-ai-agent
docker-compose exec postgres pg_dump -U postgres facebook_ads_ai > backups/db_backup_$(date +%Y%m%d).sql

# 3. Criar branch de desenvolvimento
git checkout -b fix/comprehensive-fixes
git push -u origin fix/comprehensive-fixes
```

### 0.2 Instalar Ferramentas de Qualidade
```bash
# Instalar ferramentas de análise
pip install --upgrade \
    black \
    isort \
    flake8 \
    mypy \
    bandit \
    safety \
    pre-commit \
    pytest \
    pytest-cov \
    pytest-asyncio \
    pytest-mock
```

### 0.3 Configurar Pre-commit Hooks
```bash
# Criar .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100', '--extend-ignore=E203,W503']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: ['--ignore-missing-imports']
EOF

# Instalar hooks
pre-commit install
```

### 0.4 Criar Estrutura de Tracking
```bash
# Criar arquivo de tracking de progresso
cat > PROGRESS.md << 'EOF'
# Progresso de Correções

## ✅ Completado
- [ ] Fase 0: Setup

## 🔄 Em Progresso
- Nenhum item

## ⏳ Pendente
- Todas as fases seguintes
EOF
```

**Checklist Fase 0:**
- [ ] Backup criado
- [ ] Branch de desenvolvimento criada
- [ ] Ferramentas instaladas
- [ ] Pre-commit configurado
- [ ] Arquivo de tracking criado

**Tempo Estimado: 2 horas**

---

# 🔴 FASE 1: SEGURANÇA CRÍTICA (SEMANA 1-2)

## Objetivos
- Eliminar credenciais expostas
- Implementar autenticação JWT
- Configurar CORS seguro
- Adicionar rate limiting

---

## 1.1 ROTAÇÃO DE CREDENCIAIS [URGENTE - DIA 1]

### Problema
- Arquivo `.env` contém credenciais REAIS expostas
- Notion API Token: `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`
- n8n API Key: JWT exposto
- SECRET_KEY padrão: `"change-me-in-production"`

### Solução

#### 1.1.1 Renovar Credenciais Externas
```bash
# 1. NOTION API TOKEN
# Acesse: https://www.notion.so/my-integrations
# - Encontre a integração existente
# - Clique em "Refresh Token" ou crie nova integração
# - Copie o novo token

# 2. N8N API KEY
# Acesse: https://fluxos.macspark.dev/settings/api
# - Delete a API key antiga
# - Crie nova API key
# - Copie o novo token

# 3. Gerar novo SECRET_KEY
openssl rand -hex 32
# Resultado exemplo: 8f3a2c1b9d4e7f6a5c8b2e9d1f4a7c3b6e9f2a5c8b1d4e7f3a6c9b2e5f8a1d4c
```

#### 1.1.2 Criar .env.example Seguro
```bash
# Atualizar .env.example (sem valores reais)
cat > .env.example << 'EOF'
# FACEBOOK ADS AI AGENT - CONFIGURAÇÕES

# Application
APP_NAME=Facebook Ads AI Agent
APP_VERSION=1.0.0
DEBUG=False
ENVIRONMENT=production

# Facebook Ads (OBRIGATÓRIO)
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_AD_ACCOUNT_ID=act_your_account_id

# Database (OBRIGATÓRIO)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database
POSTGRES_PASSWORD=change_me_strong_password

# Redis (OBRIGATÓRIO)
REDIS_URL=redis://localhost:6379/0

# Security (OBRIGATÓRIO - GERE COM: openssl rand -hex 32)
SECRET_KEY=GENERATE_WITH_OPENSSL_RAND_HEX_32
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Notion Integration (OPCIONAL)
NOTION_API_TOKEN=secret_your_notion_token
NOTION_DATABASE_ID=your_database_id

# n8n Integration (OPCIONAL)
N8N_API_URL=https://your-n8n-instance.com/api/v1
N8N_API_KEY=your_n8n_api_key
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=strong_password

# Alertas (OPCIONAL)
WHATSAPP_ALERT_PHONE=+55XXXXXXXXXXX
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
ADMIN_EMAIL=admin@example.com

# AI/NLP (OPCIONAL)
OPENAI_API_KEY=sk-your_openai_api_key

# Monitoring (OPCIONAL)
GRAFANA_PASSWORD=strong_password
FLOWER_PASSWORD=strong_password
EOF
```

#### 1.1.3 Atualizar .env Real (MANUALMENTE)
```bash
# IMPORTANTE: NÃO COMMITAR ESTE ARQUIVO!

# 1. Copiar template
cp .env.example .env

# 2. Editar .env com editor de texto
# Preencher TODAS as credenciais reais

# 3. Verificar que .env está no .gitignore
grep "^\.env$" .gitignore || echo ".env" >> .gitignore

# 4. Remover .env do git SE já foi commitado
git rm --cached .env
git commit -m "security: remove .env from version control"
```

#### 1.1.4 Validar Segurança
```bash
# Verificar se não há credenciais no código
grep -r "ntn_" src/
grep -r "eyJhbGciOi" src/
grep -r "change-me-in-production" src/

# Resultado esperado: Nenhuma ocorrência
```

**Checklist 1.1:**
- [ ] Notion token renovado
- [ ] n8n API key renovada
- [ ] SECRET_KEY gerado (32 bytes)
- [ ] .env.example atualizado
- [ ] .env real configurado
- [ ] .env removido do git
- [ ] Validação de segurança passando

**Tempo Estimado: 1 hora**

---

## 1.2 IMPLEMENTAR AUTENTICAÇÃO JWT [CRÍTICO]

### Problema
- JWT implementado mas NÃO enforçado
- Todos endpoints acessíveis sem autenticação
- Falta middleware de auth

### Solução

#### 1.2.1 Criar Módulo de Autenticação
```bash
# Criar arquivo src/utils/auth.py
cat > src/utils/auth.py << 'EOF'
"""
Authentication and Authorization utilities
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.utils.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token

    Args:
        data: Payload data (should include 'sub' with user identifier)
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get("sub") is None:
            raise credentials_exception

        return payload

    except JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        raise credentials_exception


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get current authenticated user

    Usage:
        @router.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"user": user}
    """
    token = credentials.credentials
    payload = verify_token(token)
    return payload


# Optional: API Key authentication for integrations
async def verify_api_key(api_key: str) -> bool:
    """
    Verify API key for external integrations

    TODO: Implement API key storage (database or Redis)
    """
    # Placeholder - implement with database lookup
    valid_keys = {
        "test-api-key": {"name": "Test Integration", "permissions": ["read"]}
    }
    return api_key in valid_keys
EOF
```

#### 1.2.2 Criar Endpoints de Autenticação
```bash
# Criar arquivo src/api/auth.py
cat > src/api/auth.py << 'EOF'
"""
Authentication API Router
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth import (
    create_access_token,
    verify_password,
    hash_password,
    get_current_user
)
from src.utils.config import settings
from src.utils.database import get_db
from src.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return JWT token
    """
    # TODO: Implement user lookup from database
    # For now, using mock validation

    # Mock user (replace with database query)
    mock_email = "admin@macspark.dev"
    mock_password_hash = hash_password("admin123")  # Change in production!

    if request.email != mock_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not verify_password(request.password, mock_password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token = create_access_token(
        data={"sub": request.email, "type": "user"}
    )

    logger.info(f"User {request.email} logged in successfully")

    return LoginResponse(
        access_token=access_token,
        expires_in=settings.JWT_EXPIRATION_MINUTES * 60
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register new user
    """
    # TODO: Implement user creation in database
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration not implemented yet"
    )


@router.get("/me", response_model=dict)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user information
    """
    return {
        "email": current_user.get("sub"),
        "type": current_user.get("type")
    }


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh access token
    """
    new_token = create_access_token(
        data={"sub": current_user.get("sub"), "type": current_user.get("type")}
    )

    return LoginResponse(
        access_token=new_token,
        expires_in=settings.JWT_EXPIRATION_MINUTES * 60
    )
EOF
```

#### 1.2.3 Adicionar Auth Router ao Main
```bash
# Editar main.py para incluir auth router
# Adicionar após as importações:
# from src.api import auth

# Adicionar após os outros routers:
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
```

#### 1.2.4 Proteger Endpoints Sensíveis
```bash
# Exemplo de proteção de endpoint
# Editar src/api/automation.py

# Adicionar importação:
# from src.utils.auth import get_current_user

# Modificar endpoints para requerer autenticação:
# @router.post("/pause-underperforming")
# async def pause_underperforming(
#     current_user: dict = Depends(get_current_user),  # <- ADICIONAR
#     ... resto dos parâmetros
# ):
```

**Checklist 1.2:**
- [ ] Módulo auth.py criado
- [ ] Router auth.py criado
- [ ] Auth router adicionado ao main.py
- [ ] Endpoints protegidos (automation, analytics)
- [ ] Testado login com Postman/curl

**Tempo Estimado: 4 horas**

---

## 1.3 CONFIGURAR CORS SEGURO [ALTO]

### Problema
- CORS configurado como `allow_origins=["*"]` (aceita qualquer origem)
- Permite CSRF attacks

### Solução

#### 1.3.1 Atualizar Configuração CORS
```python
# Editar main.py (linhas 42-48)

# ANTES:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # INSEGURO!
#     ...
# )

# DEPOIS:
from src.utils.config import settings

# Definir origins permitidas baseado no ambiente
allowed_origins = []

if settings.ENVIRONMENT == "development":
    allowed_origins = [
        "http://localhost:3000",  # Frontend local
        "http://localhost:8000",  # API local
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
elif settings.ENVIRONMENT == "staging":
    allowed_origins = [
        "https://staging.fbads.macspark.dev",
        "https://staging-api.fbads.macspark.dev",
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
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

#### 1.3.2 Adicionar Variável de Ambiente
```bash
# Adicionar ao .env.example e .env
echo "ALLOWED_ORIGINS=https://fbads.macspark.dev,http://localhost:3000" >> .env.example
```

#### 1.3.3 Adicionar Headers de Segurança
```python
# Criar src/utils/security_headers.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response

# Adicionar ao main.py:
# from src.utils.security_headers import SecurityHeadersMiddleware
# app.add_middleware(SecurityHeadersMiddleware)
```

**Checklist 1.3:**
- [ ] CORS configurado com whitelist
- [ ] Variável ALLOWED_ORIGINS adicionada
- [ ] Security headers middleware criado
- [ ] Testado com curl/Postman

**Tempo Estimado: 1 hora**

---

## 1.4 IMPLEMENTAR RATE LIMITING [ALTO]

### Problema
- Sem proteção contra abuso de API
- Endpoints podem ser sobrecarregados

### Solução

#### 1.4.1 Instalar Dependência
```bash
pip install slowapi
pip freeze | grep slowapi >> requirements.txt
```

#### 1.4.2 Configurar Rate Limiting
```python
# Criar src/utils/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Criar limiter
limiter = Limiter(key_func=get_remote_address)

# Adicionar ao main.py:
from src.utils.rate_limit import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Usar em routers:
from src.utils.rate_limit import limiter

@router.get("/campaigns")
@limiter.limit("100/minute")
async def get_campaigns(request: Request, ...):
    ...

@router.post("/automation/pause-underperforming")
@limiter.limit("10/minute")
async def pause_underperforming(request: Request, ...):
    ...
```

**Checklist 1.4:**
- [ ] slowapi instalado
- [ ] Rate limiter configurado
- [ ] Limites aplicados em endpoints
- [ ] Testado com múltiplas requests

**Tempo Estimado: 2 horas**

---

## 1.5 VARREDURA DE SEGURANÇA [VALIDAÇÃO]

### Executar Scans de Segurança
```bash
# 1. Bandit (SAST)
bandit -r src/ -f json -o security-report-bandit.json
bandit -r src/ -ll  # Low severity and above

# 2. Safety (Vulnerability scan)
safety check --json > security-report-safety.json

# 3. Verificar secrets no código
git secrets --scan

# 4. Trufflehog (secret scanning)
trufflehog filesystem . --json > security-report-trufflehog.json
```

**Checklist 1.5:**
- [ ] Bandit: 0 HIGH issues
- [ ] Safety: 0 vulnerabilidades conhecidas
- [ ] Git secrets: Nenhum secret detectado
- [ ] Trufflehog: Clean

**Tempo Estimado: 1 hora**

---

**CHECKLIST COMPLETO FASE 1:**
- [ ] 1.1 Credenciais rotacionadas
- [ ] 1.2 JWT autenticação implementada
- [ ] 1.3 CORS configurado corretamente
- [ ] 1.4 Rate limiting ativo
- [ ] 1.5 Scans de segurança passando

**Tempo Total Fase 1: 10 horas (2 dias úteis)**

---

# 🧪 FASE 2: TESTES E QUALIDADE (SEMANA 3-4)

## Objetivos
- Corrigir suite de testes atual
- Aumentar cobertura para 85%+
- Implementar testes de integração e E2E
- Configurar quality gates no CI/CD

---

## 2.1 CORRIGIR SUITE DE TESTES ATUAL [CRÍTICO]

### Problema
- Teste importa classe inexistente `CampaignInsight`
- Suite falhando com erro de import

### Solução

#### 2.1.1 Corrigir Import Error
```python
# Editar tests/unit/test_facebook_agent.py linha 10

# ANTES:
# from src.agents.facebook_agent import FacebookAdsAgent, CampaignInsight

# DEPOIS:
from src.agents.facebook_agent import FacebookAdsAgent
```

#### 2.1.2 Atualizar Fixtures
```python
# Editar tests/conftest.py
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def sample_campaign():
    """Sample campaign data"""
    return {
        'id': '123456789',
        'name': 'Test Campaign',
        'status': 'ACTIVE',
        'objective': 'CONVERSIONS',
        'daily_budget': '5000',
        'lifetime_budget': None,
        'created_time': '2025-10-01T00:00:00Z',
        'updated_time': '2025-10-18T00:00:00Z'
    }

@pytest.fixture
def sample_insights():
    """Sample insights data"""
    return {
        'campaign_id': '123456789',
        'impressions': 10000,
        'clicks': 500,
        'spend': 250.50,
        'reach': 8500,
        'frequency': 1.18,
        'ctr': 5.0,
        'cpc': 0.50,
        'cpm': 25.05,
        'purchases': 10,
        'cpa': 25.05,
        'roas': 4.0,
        'date_range': 'last_7d'
    }

@pytest.fixture
def mock_facebook_api():
    """Mock Facebook API"""
    with patch('src.agents.facebook_agent.FacebookAdsApi') as mock:
        yield mock
```

#### 2.1.3 Executar Testes
```bash
# Executar testes unitários
pytest tests/unit -v

# Verificar que todos passam
# Expected: All tests passing
```

**Checklist 2.1:**
- [ ] Import error corrigido
- [ ] Fixtures atualizadas
- [ ] Todos testes unitários passando

**Tempo Estimado: 1 hora**

---

## 2.2 EXPANDIR TESTES UNITÁRIOS (META: 80%)

### Problema
- Cobertura atual: 26%
- Módulos com 0% cobertura:
  - `src/integrations/n8n_client.py` (0%)
  - `src/models/*` (0%)
  - `src/tasks/*` (0%)

### Solução

#### 2.2.1 Testes para Models
```bash
# Criar tests/unit/test_models.py
cat > tests/unit/test_models.py << 'EOF'
"""Unit tests for database models"""
import pytest
from datetime import datetime
from src.models.campaign import Campaign, CampaignStatus
from src.models.insight import Insight
from src.models.suggestion import Suggestion, SuggestionType, SuggestionStatus

class TestCampaign:
    def test_campaign_creation(self):
        """Test campaign model creation"""
        campaign = Campaign(
            facebook_id="123456",
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
            objective="CONVERSIONS",
            daily_budget=5000.0
        )

        assert campaign.facebook_id == "123456"
        assert campaign.status == CampaignStatus.ACTIVE

    def test_campaign_status_enum(self):
        """Test campaign status enum"""
        assert CampaignStatus.ACTIVE.value == "ACTIVE"
        assert CampaignStatus.PAUSED.value == "PAUSED"

class TestInsight:
    def test_insight_creation(self):
        """Test insight model creation"""
        insight = Insight(
            campaign_id=1,
            impressions=10000,
            clicks=500,
            spend=250.50,
            ctr=5.0,
            cpc=0.50
        )

        assert insight.impressions == 10000
        assert insight.ctr == 5.0

class TestSuggestion:
    def test_suggestion_creation(self):
        """Test suggestion model creation"""
        suggestion = Suggestion(
            campaign_id=1,
            suggestion_type=SuggestionType.PAUSE_CAMPAIGN,
            reason="CTR too low",
            status=SuggestionStatus.PENDING
        )

        assert suggestion.suggestion_type == SuggestionType.PAUSE_CAMPAIGN
        assert suggestion.status == SuggestionStatus.PENDING
EOF
```

#### 2.2.2 Testes para Integrations
```bash
# Criar tests/unit/test_integrations.py
cat > tests/unit/test_integrations.py << 'EOF'
"""Unit tests for integrations"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import httpx

from src.integrations.n8n_client import N8nClient
from src.integrations.notion_client import NotionClient

class TestN8nClient:
    @pytest.fixture
    def n8n_client(self):
        return N8nClient()

    @pytest.mark.asyncio
    async def test_trigger_workflow(self, n8n_client):
        """Test workflow triggering"""
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.return_value = Mock(
                status_code=200,
                json=lambda: {"status": "success"}
            )

            result = await n8n_client.trigger_workflow(
                webhook_name="alert",
                data={"message": "test"}
            )

            assert result["status"] == "success"
            mock_post.assert_called_once()

class TestNotionClient:
    @pytest.fixture
    def notion_client(self):
        return NotionClient()

    @pytest.mark.asyncio
    async def test_create_page(self, notion_client):
        """Test page creation"""
        # TODO: Implement test
        pass
EOF
```

#### 2.2.3 Testes para Tasks
```bash
# Criar tests/unit/test_tasks.py
cat > tests/unit/test_tasks.py << 'EOF'
"""Unit tests for Celery tasks"""
import pytest
from unittest.mock import Mock, patch

# from src.tasks.collectors import collect_facebook_metrics
# from src.tasks.processors import analyze_performance
# from src.tasks.notifiers import send_alerts

# TODO: Implementar testes quando tasks estiverem funcionais
EOF
```

#### 2.2.4 Executar Cobertura
```bash
# Executar com relatório de cobertura
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Visualizar relatório
# open htmlcov/index.html
```

**Checklist 2.2:**
- [ ] Testes de models criados
- [ ] Testes de integrations criados
- [ ] Testes de tasks criados
- [ ] Cobertura >80%

**Tempo Estimado: 8 horas**

---

## 2.3 IMPLEMENTAR TESTES DE INTEGRAÇÃO

### Objetivo
Testar endpoints completos com banco de dados real

#### 2.3.1 Configurar TestContainers
```bash
pip install testcontainers pytest-postgresql
```

#### 2.3.2 Criar Testes de Integração
```python
# tests/integration/test_api_complete.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestCampaignsAPI:
    def test_list_campaigns_unauthorized(self):
        """Test campaigns endpoint without auth"""
        response = client.get("/api/v1/campaigns")
        assert response.status_code == 401

    def test_list_campaigns_authorized(self):
        """Test campaigns endpoint with auth"""
        # TODO: Get auth token
        headers = {"Authorization": "Bearer test_token"}
        response = client.get("/api/v1/campaigns", headers=headers)
        assert response.status_code == 200
```

**Checklist 2.3:**
- [ ] Testcontainers configurado
- [ ] Testes de integração criados
- [ ] Todos endpoints testados

**Tempo Estimado: 6 horas**

---

## 2.4 IMPLEMENTAR TESTES E2E

### Objetivo
Testar fluxos completos do usuário

#### 2.4.1 Criar Testes E2E
```python
# tests/e2e/test_complete_flow.py
import pytest

class TestCompleteUserFlow:
    def test_user_journey_analysis(self):
        """
        Teste completo:
        1. Login
        2. Fetch campaigns
        3. Get insights
        4. Generate suggestions
        5. View dashboard
        """
        # TODO: Implement
        pass
```

**Checklist 2.4:**
- [ ] 5+ cenários E2E implementados
- [ ] Todos cenários passando

**Tempo Estimado: 4 horas**

---

## 2.5 CONFIGURAR QUALITY GATES

### Objetivo
Bloquear merges com qualidade baixa

#### 2.5.1 Atualizar .gitlab-ci.yml
```yaml
# Adicionar quality gate
quality_gate:
  stage: test
  script:
    - pytest tests/ --cov=src --cov-fail-under=80
  allow_failure: false
  only:
    - merge_requests
    - main
```

**Checklist 2.5:**
- [ ] Quality gate configurado
- [ ] Coverage threshold: 80%
- [ ] Testado com MR

**Tempo Estimado: 1 hora**

---

**CHECKLIST COMPLETO FASE 2:**
- [ ] 2.1 Suite de testes corrigida
- [ ] 2.2 Cobertura expandida para 80%+
- [ ] 2.3 Testes de integração implementados
- [ ] 2.4 Testes E2E implementados
- [ ] 2.5 Quality gates configurados

**Tempo Total Fase 2: 20 horas (4 dias úteis)**

---

# ⚙️ FASE 3: REFACTORING E PERFORMANCE (SEMANA 5-6)

## Objetivos
- Implementar dependency injection
- Substituir NLP pattern matching por LangChain
- Adicionar circuit breakers
- Implementar caching inteligente

---

## 3.1 DEPENDENCY INJECTION PARA FACEBOOKADSAGENT

### Problema
- Cada request cria nova instância de FacebookAdsAgent
- Re-inicialização desnecessária da API

### Solução

#### 3.1.1 Criar Dependencies Module
```python
# Criar src/utils/dependencies.py
from functools import lru_cache
from src.agents.facebook_agent import FacebookAdsAgent
from src.analytics.performance_analyzer import PerformanceAnalyzer
from src.automation.campaign_optimizer import CampaignOptimizer

@lru_cache()
def get_facebook_agent() -> FacebookAdsAgent:
    """Get cached Facebook Agent instance"""
    return FacebookAdsAgent()

@lru_cache()
def get_performance_analyzer() -> PerformanceAnalyzer:
    """Get cached Performance Analyzer instance"""
    return PerformanceAnalyzer()

@lru_cache()
def get_campaign_optimizer() -> CampaignOptimizer:
    """Get cached Campaign Optimizer instance"""
    return CampaignOptimizer()
```

#### 3.1.2 Atualizar Routers
```python
# Atualizar src/api/campaigns.py
from fastapi import Depends
from src.utils.dependencies import get_facebook_agent

@router.get("/")
async def list_campaigns(
    agent: FacebookAdsAgent = Depends(get_facebook_agent),
    status: Optional[str] = None
):
    campaigns = await agent.get_campaigns(status_filter=status)
    return campaigns
```

**Checklist 3.1:**
- [ ] Dependencies module criado
- [ ] Todos routers atualizados
- [ ] Performance medida (antes/depois)

**Tempo Estimado: 3 horas**

---

## 3.2 IMPLEMENTAR LANGCHAIN PARA NLP

### Problema
- NLP atual usa pattern matching simples
- Comentário no código: "TODO: Replace with LangChain"

### Solução

#### 3.2.1 Criar LangChain Agent
```python
# Criar src/agents/nlp_agent.py
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class NLPAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0.7)

        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="""
            You are a Facebook Ads assistant. Extract intent from user query.

            Query: {query}

            Classify into one of:
            - list_campaigns
            - performance_analysis
            - spend_analysis
            - suggestions
            - help

            Output JSON with: {{"intent": "...", "params": {{}}}}
            """
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    async def process_query(self, query: str) -> dict:
        """Process natural language query"""
        result = await self.chain.arun(query=query)
        return result
```

**Checklist 3.2:**
- [ ] LangChain instalado
- [ ] NLP agent criado
- [ ] Integrado no facebook_agent.py
- [ ] Testado com queries complexas

**Tempo Estimado: 4 horas**

---

## 3.3 CIRCUIT BREAKERS PARA APIS EXTERNAS

### Solução

#### 3.3.1 Instalar e Configurar
```bash
pip install circuitbreaker

# Adicionar ao requirements.txt
```

#### 3.3.2 Implementar Circuit Breaker
```python
# Criar src/utils/circuit_breaker.py
from circuitbreaker import circuit

class APICircuitBreaker:
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    async def call_with_circuit_breaker(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        return await func(*args, **kwargs)

# Usar em src/integrations/n8n_client.py
from src.utils.circuit_breaker import APICircuitBreaker

class N8nClient:
    def __init__(self):
        self.breaker = APICircuitBreaker()

    async def trigger_workflow(self, ...):
        return await self.breaker.call_with_circuit_breaker(
            self._trigger_workflow_internal,
            ...
        )
```

**Checklist 3.3:**
- [ ] Circuit breakers implementados
- [ ] Aplicados em Facebook, n8n, Notion APIs
- [ ] Testado com falhas simuladas

**Tempo Estimado: 3 horas**

---

## 3.4 CACHING INTELIGENTE

### Solução

#### 3.4.1 Implementar Redis Cache
```python
# Criar src/utils/cache.py
import redis.asyncio as redis
from functools import wraps
import json
from src.utils.config import settings

class CacheManager:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    async def get(self, key: str):
        """Get value from cache"""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: any, ttl: int = 300):
        """Set value in cache with TTL"""
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value)
        )

    async def delete(self, pattern: str):
        """Delete keys matching pattern"""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

# Decorator para cache
def cached(ttl: int = 300, key_prefix: str = ""):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = CacheManager()

            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            cached_value = await cache.get(cache_key)
            if cached_value:
                return cached_value

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            await cache.set(cache_key, result, ttl)

            return result
        return wrapper
    return decorator

# Usar em src/agents/facebook_agent.py
@cached(ttl=300, key_prefix="campaigns")
async def get_campaigns(self, status_filter=None):
    # ... implementação
```

**Checklist 3.4:**
- [ ] Cache manager criado
- [ ] Cache aplicado em campaigns, insights
- [ ] Cache invalidation implementado
- [ ] Cache hit rate medido

**Tempo Estimado: 3 horas**

---

## 3.5 CODE QUALITY IMPROVEMENTS

### Solução

#### 3.5.1 Executar Linters
```bash
# Black (formatação)
black src/ tests/

# isort (imports)
isort src/ tests/

# flake8 (linting)
flake8 src/ tests/ --max-line-length=100

# mypy (type checking)
mypy src/ --ignore-missing-imports
```

#### 3.5.2 Corrigir Warnings
- Remover imports não utilizados
- Adicionar type hints faltantes
- Refatorar funções >50 linhas

**Checklist 3.5:**
- [ ] Black executado
- [ ] isort executado
- [ ] flake8: 0 erros
- [ ] mypy: 0 erros

**Tempo Estimado: 4 horas**

---

**CHECKLIST COMPLETO FASE 3:**
- [ ] 3.1 Dependency injection implementado
- [ ] 3.2 LangChain integrado
- [ ] 3.3 Circuit breakers ativos
- [ ] 3.4 Caching implementado
- [ ] 3.5 Code quality melhorado

**Tempo Total Fase 3: 17 horas (3.5 dias úteis)**

---

# 🚀 FASE 4: CONFIGURAÇÕES DE PRODUÇÃO (SEMANA 7-8)

## 4.1 ATUALIZAR CONFIGURAÇÕES DOCKER

### Solução

#### 4.1.1 Substituir Domínios de Exemplo
```bash
# Editar docker-compose.prod.yml

# Substituir:
# - fbads.example.com → fbads.macspark.dev
# - admin@example.com → marco@macspark.dev
# - flower.fbads.example.com → flower.fbads.macspark.dev
# - n8n.fbads.example.com → n8n.fbads.macspark.dev
```

#### 4.1.2 Configurar Senhas Fortes
```bash
# Gerar senhas fortes
openssl rand -base64 32  # POSTGRES_PASSWORD
openssl rand -base64 32  # GRAFANA_PASSWORD
openssl rand -base64 32  # FLOWER_PASSWORD
openssl rand -base64 32  # N8N_PASSWORD

# Adicionar ao .env
```

**Checklist 4.1:**
- [ ] Domínios atualizados
- [ ] Senhas geradas e configuradas
- [ ] docker-compose.prod.yml validado

**Tempo Estimado: 1 hora**

---

## 4.2 CONFIGURAR BACKUP AUTOMATIZADO

### Solução

#### 4.2.1 Criar Cron Job para Backup
```bash
# Criar scripts/backup_cron.sh
#!/bin/bash
set -e

# Executar backup
/app/scripts/backup.sh

# Upload para S3/Backblaze
# TODO: Configurar rclone ou aws cli

# Manter apenas últimos 30 backups
find /app/backups -name "*.sql" -mtime +30 -delete

echo "Backup completed at $(date)"
```

#### 4.2.2 Agendar com Cron
```bash
# Adicionar ao crontab
0 3 * * * /app/scripts/backup_cron.sh >> /app/logs/backup.log 2>&1
```

**Checklist 4.2:**
- [ ] Script de backup criado
- [ ] Cron job configurado
- [ ] Testado dry-run

**Tempo Estimado: 2 horas**

---

## 4.3 CONFIGURAR MONITORING AVANÇADO

### Solução

#### 4.3.1 Configurar Alertas Prometheus
```yaml
# Criar config/prometheus_alerts.yml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      - alert: HighLatency
        expr: http_request_duration_seconds_p95 > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API latency too high"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

**Checklist 4.3:**
- [ ] Alertas configurados
- [ ] Dashboards Grafana criados
- [ ] Testado com métricas simuladas

**Tempo Estimado: 3 horas**

---

**CHECKLIST COMPLETO FASE 4:**
- [ ] 4.1 Configurações Docker atualizadas
- [ ] 4.2 Backup automatizado
- [ ] 4.3 Monitoring configurado

**Tempo Total Fase 4: 6 horas (1.5 dias úteis)**

---

# 🎨 FASE 5: FEATURES FALTANTES (SEMANA 9-10)

## 5.1 AUTO-APPLY SUGGESTIONS

### Solução
```python
# Criar endpoint para auto-apply
@router.post("/automation/auto-apply/{suggestion_id}")
async def auto_apply_suggestion(
    suggestion_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Auto-apply approved suggestion"""
    # TODO: Implementar lógica
    pass
```

**Checklist 5.1:**
- [ ] Auto-apply implementado
- [ ] Approval workflow criado
- [ ] Testado em staging

**Tempo Estimado: 4 horas**

---

## 5.2 RELATÓRIOS PDF

### Solução
```bash
pip install weasyprint

# Criar src/reports/pdf_generator.py
from weasyprint import HTML

class PDFReportGenerator:
    def generate_campaign_report(self, campaign_data):
        html_content = self._render_template(campaign_data)
        pdf = HTML(string=html_content).write_pdf()
        return pdf
```

**Checklist 5.2:**
- [ ] PDF generator implementado
- [ ] Templates criados
- [ ] Endpoint /reports/pdf criado

**Tempo Estimado: 4 horas**

---

**CHECKLIST COMPLETO FASE 5:**
- [ ] 5.1 Auto-apply implementado
- [ ] 5.2 Relatórios PDF implementados

**Tempo Total Fase 5: 8 horas (2 dias úteis)**

---

# ✅ FASE 6: VALIDAÇÃO E DEPLOY (SEMANA 11-12)

## 6.1 TESTES FINAIS

### Checklist
- [ ] Todos testes unitários passando
- [ ] Todos testes integração passando
- [ ] Testes E2E passando
- [ ] Cobertura ≥85%
- [ ] Security scan clean
- [ ] Performance benchmarks OK

**Tempo Estimado: 4 horas**

---

## 6.2 DEPLOY STAGING

```bash
# Deploy para staging
./scripts/deploy.sh staging

# Smoke tests
./scripts/smoke.sh staging
```

**Checklist 6.2:**
- [ ] Deploy staging bem-sucedido
- [ ] Smoke tests passando
- [ ] Monitoramento ativo

**Tempo Estimado: 2 horas**

---

## 6.3 DEPLOY PRODUCTION

```bash
# Deploy para produção
./scripts/deploy.sh production

# Verificar health
curl https://api.fbads.macspark.dev/health
```

**Checklist 6.3:**
- [ ] Deploy production bem-sucedido
- [ ] Health check OK
- [ ] Monitoring ativo
- [ ] Backups funcionando

**Tempo Estimado: 2 horas**

---

**CHECKLIST COMPLETO FASE 6:**
- [ ] 6.1 Testes finais passando
- [ ] 6.2 Deploy staging OK
- [ ] 6.3 Deploy production OK

**Tempo Total Fase 6: 8 horas (2 dias úteis)**

---

# 📈 RESUMO GERAL

## Tempo Total Estimado

| Fase | Dias Úteis | Horas |
|------|-----------|-------|
| Fase 0 - Setup | 0.25 | 2h |
| Fase 1 - Segurança | 2 | 10h |
| Fase 2 - Testes | 4 | 20h |
| Fase 3 - Refactoring | 3.5 | 17h |
| Fase 4 - Produção | 1.5 | 6h |
| Fase 5 - Features | 2 | 8h |
| Fase 6 - Deploy | 2 | 8h |
| **TOTAL** | **15.25 dias** | **71 horas** |

## Priorização

### 🔴 CRÍTICO (Fazer IMEDIATAMENTE)
1. Rotação de credenciais (Fase 1.1) - 1h
2. Corrigir testes falhando (Fase 2.1) - 1h
3. CORS seguro (Fase 1.3) - 1h
4. JWT authentication (Fase 1.2) - 4h

### ⚠️ ALTO (Semana 1-2)
5. Rate limiting (Fase 1.4) - 2h
6. Expandir testes (Fase 2.2) - 8h
7. Dependency injection (Fase 3.1) - 3h

### 🟡 MÉDIO (Semana 3-4)
8. Circuit breakers (Fase 3.3) - 3h
9. Caching (Fase 3.4) - 3h
10. Configurações produção (Fase 4) - 6h

### 🟢 BAIXO (Semana 5-6)
11. Features adicionais (Fase 5) - 8h
12. Deploy final (Fase 6) - 8h

---

# 🎯 MÉTRICAS DE SUCESSO

Ao final do plano, atingiremos:

| Métrica | Atual | Meta | Status |
|---------|-------|------|--------|
| Segurança | 4/10 | 9/10 | ⏳ |
| Cobertura Testes | 26% | 85% | ⏳ |
| API Latency (p95) | ~800ms | <300ms | ⏳ |
| Bugs Críticos | 5 | 0 | ⏳ |
| Production Ready | 70% | 95% | ⏳ |

---

# 📞 SUPORTE

Para dúvidas ou problemas durante a execução:
- **Email**: marco@macspark.dev
- **Documentação**: Ver README.md e docs/

---

**Última Atualização**: 18 de Outubro de 2025
**Versão do Documento**: 1.0
