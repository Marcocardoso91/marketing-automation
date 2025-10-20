# 🚀 GUIA DE INÍCIO RÁPIDO
## Facebook Ads AI Agent - Primeiros Passos

---

## ⏱️ TEMPO ESTIMADO: 2 horas

Este guia te levará de **zero a uma aplicação rodando localmente** em 2 horas.

---

## ✅ PRÉ-REQUISITOS

### Software Necessário
```bash
# Verificar instalações
docker --version       # Docker 20.10+
docker-compose --version  # Docker Compose 1.29+
git --version         # Git 2.30+
python --version      # Python 3.11+
```

### Credenciais Facebook
- [ ] Facebook App ID
- [ ] Facebook App Secret  
- [ ] Facebook Access Token (User ou System)
- [ ] Facebook Ad Account ID (formato: `act_123456789`)

**Como obter:** https://developers.facebook.com/apps/

---

## 📋 PASSO 1: CRIAR ESTRUTURA BASE (30min)

### 1.1 Clonar Repositório
```bash
cd ~/projects
git clone https://github.com/seu-org/facebook-ads-ai-agent.git
cd facebook-ads-ai-agent
```

### 1.2 Criar Estrutura de Diretórios
```bash
# Criar estrutura completa
mkdir -p src/{agents,api,analytics,automation,reports,integrations,models,schemas,tasks,utils}
mkdir -p tests/{unit,integration,e2e,features}
mkdir -p config/{grafana/dashboards,n8n/workflows}
mkdir -p scripts alembic/versions logs data/{cache,exports}

# Criar __init__.py em cada diretório Python
find src tests -type d -exec touch {}/__init__.py \;

echo "✅ Estrutura de diretórios criada"
tree src/ -L 2
```

### 1.3 Mover Arquivos Existentes
```bash
# Mover módulos para src/utils/
mv api_client.py src/utils/
mv context_memory.py src/utils/
mv token_manager.py src/utils/

# Mover testes
mv test_facebook_agent.py tests/unit/
mv test_api_integration.py tests/integration/

echo "✅ Arquivos organizados"
```

---

## 📋 PASSO 2: CONFIGURAR DEPENDÊNCIAS (20min)

### 2.1 Criar requirements.txt
```bash
cat > requirements.txt << 'EOF'
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Cache & Queue
redis==5.0.1
celery==5.3.4

# Facebook
facebook-business==18.0.4

# Async
httpx==0.25.2
aiohttp==3.9.1
tenacity==8.2.3

# Monitoring
prometheus-client==0.19.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1

# Security
python-jose[cryptography]==3.3.0

# Dev
black==23.12.0
isort==5.13.0
flake8==6.1.0
python-dotenv==1.0.0
EOF

echo "✅ requirements.txt criado"
```

### 2.2 Criar Ambiente Virtual e Instalar
```bash
# Criar venv
python -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ativar (Windows)
# venv\Scripts\activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependências instaladas"
```

---

## 📋 PASSO 3: CONFIGURAR APLICAÇÃO (30min)

### 3.1 Criar Configurações
```bash
cat > src/utils/config.py << 'EOF'
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Facebook Ads AI Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Facebook
    FACEBOOK_APP_ID: str
    FACEBOOK_APP_SECRET: str
    FACEBOOK_ACCESS_TOKEN: str
    FACEBOOK_AD_ACCOUNT_ID: str
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/facebook_ads_ai"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        
settings = Settings()
EOF

echo "✅ config.py criado"
```

### 3.2 Criar Logger
```bash
cat > src/utils/logger.py << 'EOF'
import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
EOF

echo "✅ logger.py criado"
```

### 3.3 Criar Database Setup
```bash
cat > src/utils/database.py << 'EOF'
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
EOF

echo "✅ database.py criado"
```

### 3.4 Criar main.py
```bash
cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Facebook Ads AI Agent API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
EOF

echo "✅ main.py criado"
```

### 3.5 Criar .env
```bash
cat > .env << 'EOF'
# Facebook Credentials
FACEBOOK_APP_ID=seu_app_id_aqui
FACEBOOK_APP_SECRET=seu_app_secret_aqui
FACEBOOK_ACCESS_TOKEN=seu_token_aqui
FACEBOOK_AD_ACCOUNT_ID=act_123456789

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/facebook_ads_ai

# Redis
REDIS_URL=redis://localhost:6379/0
EOF

echo "⚠️  IMPORTANTE: Edite .env com suas credenciais Facebook!"
echo "   nano .env  # ou use seu editor favorito"
```

---

## 📋 PASSO 4: TESTAR APLICAÇÃO (10min)

### 4.1 Testar Localmente (Sem Docker)
```bash
# Executar aplicação
python main.py

# Em outro terminal, testar
curl http://localhost:8000/health
# Deve retornar: {"status":"healthy"}

# Acessar documentação
# Abrir navegador: http://localhost:8000/docs
```

**Resultado Esperado:** Swagger UI deve aparecer com 2 endpoints (`/` e `/health`)

---

## 📋 PASSO 5: DOCKER (OPCIONAL - 40min)

### 5.1 Criar Dockerfile
```bash
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

echo "✅ Dockerfile criado"
```

### 5.2 Criar docker-compose.yml
```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    build: .
    container_name: fbads-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/facebook_ads_ai
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: fbads-postgres
    environment:
      POSTGRES_DB: facebook_ads_ai
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: fbads-redis
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  postgres_data:
EOF

echo "✅ docker-compose.yml criado"
```

### 5.3 Executar Stack Docker
```bash
# Build e start
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f app

# Testar
curl http://localhost:8000/health
```

**Resultado Esperado:** Todos os 3 containers devem estar "Up"

---

## 📋 PASSO 6: VALIDAÇÃO FINAL (10min)

### Checklist
- [ ] `python main.py` executa sem erros
- [ ] http://localhost:8000/health retorna 200 OK
- [ ] http://localhost:8000/docs mostra Swagger UI
- [ ] Estrutura `src/` criada corretamente
- [ ] `.env` configurado com credenciais Facebook
- [ ] (Opcional) Docker Compose rodando

### Testes Rápidos
```bash
# Teste 1: Health check
curl http://localhost:8000/health
# Esperado: {"status":"healthy"}

# Teste 2: Root endpoint
curl http://localhost:8000/
# Esperado: {"message":"Facebook Ads AI Agent API",...}

# Teste 3: Swagger
# Abrir navegador: http://localhost:8000/docs
# Esperado: Interface Swagger com endpoints documentados

# Teste 4: ReDoc
# Abrir navegador: http://localhost:8000/redoc
# Esperado: Documentação alternativa
```

---

## 🎉 PARABÉNS!

Você tem agora uma **aplicação FastAPI básica rodando**! 🚀

### Próximos Passos

#### Curto Prazo (Esta Semana)
1. ✅ Implementar `FacebookAdsAgent` (ver PLANO-EXECUCAO-SPRINTS.md → Sprint 2)
2. ✅ Criar routers REST (`src/api/campaigns.py`, etc.)
3. ✅ Adicionar testes unitários

#### Médio Prazo (Próximas 2 Semanas)
4. ✅ Integrar n8n para automações
5. ✅ Configurar Prometheus + Grafana
6. ✅ Implementar Celery workers

#### Longo Prazo (Próximo Mês)
7. ✅ Deploy em produção com Traefik
8. ✅ Configurar SSL/HTTPS
9. ✅ Ativar monitoramento 24/7

---

## 📚 DOCUMENTAÇÃO ADICIONAL

### Leitura Recomendada
1. **AUDIT-REPORT-TECNICO.md** - Análise técnica completa
2. **ARCHITECTURE-BLUEPRINT.md** - Diagramas de arquitetura
3. **PLANO-EXECUCAO-SPRINTS.md** - Cronograma de 8 semanas
4. **GAPS-E-RECOMENDACOES.md** - Melhorias sugeridas

### Comandos Úteis
```bash
# Desenvolvimento
make run              # Executar app com reload
make test             # Rodar todos os testes
make lint             # Verificar code quality
make format           # Formatar código

# Docker
make docker-up        # Subir stack
make docker-down      # Parar stack
make docker-logs      # Ver logs

# Database
make migrate          # Rodar migrations
make migrate-rollback # Reverter migration
```

---

## 🆘 TROUBLESHOOTING

### Problema 1: ModuleNotFoundError
```bash
# Erro: ModuleNotFoundError: No module named 'src'
# Solução: Adicionar ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Problema 2: Port Already in Use
```bash
# Erro: Address already in use (port 8000)
# Solução: Matar processo
lsof -ti:8000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8000   # Windows (identificar PID e matar)
```

### Problema 3: Docker Compose Falha
```bash
# Erro: Cannot connect to Docker daemon
# Solução: Iniciar Docker Desktop ou daemon
sudo systemctl start docker    # Linux
# Docker Desktop deve estar rodando (Mac/Windows)
```

### Problema 4: Facebook API Error
```bash
# Erro: Invalid OAuth access token
# Solução: Verificar token no .env
# Gerar novo token em: https://developers.facebook.com/tools/accesstoken/
```

---

## 💡 DICAS PRO

### VS Code Extensions Recomendadas
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-azuretools.vscode-docker",
    "esbenp.prettier-vscode",
    "redhat.vscode-yaml"
  ]
}
```

### .gitignore Essencial
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/

# Secrets
.env
*.pem
*.key

# IDE
.vscode/
.idea/

# Logs
logs/
*.log

# Data
data/

# Coverage
htmlcov/
.coverage
EOF
```

---

## 📞 SUPORTE

### Dúvidas Técnicas
- **Documentação:** `/docs/prd/facebook-ads-agent/`
- **Issues:** GitHub Issues
- **Chat:** Slack #facebook-ads-agent

### Recursos
- **Facebook API Docs:** https://developers.facebook.com/docs/marketing-api/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Docker Docs:** https://docs.docker.com/

---

**Guia criado por:** AI Agent (Claude Sonnet 4.5)  
**Data:** 18 de Outubro de 2025  
**Versão:** 1.0.0  
**Tempo Estimado:** 2 horas

**Sucesso na implementação! 🚀**


