# Guia Completo: Testes, CI/CD e Produção

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Testes Automatizados](#testes-automatizados)
3. [CI/CD](#cicd)
4. [Segurança](#segurança)
5. [Observabilidade](#observabilidade)
6. [Deploy](#deploy)
7. [Troubleshooting](#troubleshooting)

---

## 1. Visão Geral

Este guia cobre todas as etapas para levar o **Facebook Ads AI Agent** de desenvolvimento para produção com qualidade, segurança e confiabilidade.

### Componentes Implementados

✅ **Testes Automatizados**
- Testes unitários completos
- Testes de integração de APIs
- Coverage > 80%
- Fixtures compartilhadas

✅ **Pipelines CI/CD**
- GitHub Actions
- GitLab CI
- Testes automáticos em cada commit
- Build e deploy automatizados

✅ **Segurança**
- Rate limiting e retry
- Renovação automática de tokens
- Scanners de vulnerabilidades
- Gestão segura de secrets

✅ **Observabilidade**
- Contexto de conversação persistente
- Logs estruturados
- Métricas Prometheus

---

## 2. Testes Automatizados

### 2.1 Estrutura de Testes

```
tests/
├── conftest.py                    # Fixtures compartilhadas
├── unit/
│   └── test_facebook_agent.py     # Testes unitários do agente
└── integration/
    └── test_api_integration.py    # Testes de API
```

### 2.2 Executar Testes

#### Todos os testes
```bash
pytest tests/ -v
```

#### Apenas testes unitários
```bash
pytest tests/unit -v
```

#### Apenas testes de integração
```bash
pytest tests/integration -v
```

#### Com coverage
```bash
pytest tests/ --cov=src --cov-report=html
# Relatório: htmlcov/index.html
```

### 2.3 Fixtures Disponíveis

**`mock_facebook_api`**: Mock da Facebook Marketing API
```python
def test_example(mock_facebook_api):
    # Seu teste aqui
    pass
```

**`sample_campaign_data`**: Dados de exemplo de campanha
```python
def test_campaign(sample_campaign_data):
    assert sample_campaign_data['id'] == '123456789'
```

**`sample_insights_data`**: Dados de insights de exemplo
```python
def test_insights(sample_insights_data):
    assert sample_insights_data['ctr'] == 5.0
```

### 2.4 Escrever Novos Testes

#### Template de Teste Unitário
```python
import pytest
from unittest.mock import Mock, patch

class TestMinhaFuncionalidade:
    """Testes da minha funcionalidade"""
    
    @pytest.mark.asyncio
    async def test_caso_sucesso(self):
        """Testa caso de sucesso"""
        # Arrange
        ...
        
        # Act
        result = await minha_funcao()
        
        # Assert
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_caso_erro(self):
        """Testa tratamento de erro"""
        with pytest.raises(Exception):
            await minha_funcao_com_erro()
```

### 2.5 Coverage Mínimo

O projeto exige **80% de coverage** mínimo. Para verificar:

```bash
pytest --cov=src --cov-report=term-missing
```

---

## 3. CI/CD

### 3.1 GitHub Actions

Pipeline automático que executa a cada push ou pull request:

**Stages:**
1. **Lint** - Verifica formatação e style guide
2. **Test** - Executa todos os testes
3. **Security** - Scan de vulnerabilidades
4. **Build** - Build da imagem Docker
5. **Deploy** - Deploy em produção (apenas branch main)

#### Configurar Secrets no GitHub

Vá em: **Settings** → **Secrets and variables** → **Actions**

Adicione os secrets:
```
FACEBOOK_APP_ID
FACEBOOK_APP_SECRET
FACEBOOK_ACCESS_TOKEN
FACEBOOK_AD_ACCOUNT_ID
DOCKER_USERNAME
DOCKER_PASSWORD
DEPLOY_HOST
DEPLOY_USER
DEPLOY_SSH_KEY
SNYK_TOKEN
```

#### Monitorar Pipeline

Vá em: **Actions** tab no GitHub para ver execuções.

### 3.2 GitLab CI

Pipeline similar ao GitHub Actions, configurado em `.gitlab-ci.yml`.

#### Configurar Variables no GitLab

Vá em: **Settings** → **CI/CD** → **Variables**

Adicione as mesmas variáveis do GitHub Actions.

### 3.3 Makefile - Comandos Úteis

```bash
# Instalar dependências
make install

# Executar testes
make test
make test-unit
make test-integration

# Lint e formatação
make lint
make format

# Docker
make docker-build
make docker-up
make docker-down

# Limpeza
make clean

# Executar aplicação
make run
make run-dev  # Com reload automático
```

### 3.4 Pre-commit Hooks (Opcional)

Crie `.git/hooks/pre-commit`:
```bash
#!/bin/bash
make format-check
make lint
make test-unit
```

Torne executável:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 4. Segurança

### 4.1 Rate Limiting e Retry

O módulo `src/utils/api_client.py` implementa:

- **Rate limiting automático**: Máximo 10 requests/segundo
- **Retry com backoff exponencial**: Até 5 tentativas
- **Detecção de rate limit**: Códigos 17 e 80004

#### Usar o API Client

```python
from src.utils.api_client import get_api_client

client = get_api_client()

# Executar com retry automático
result = await client.execute_with_retry(
    minha_funcao_api,
    arg1,
    arg2
)
```

### 4.2 Renovação Automática de Tokens

O módulo `src/utils/token_manager.py` gerencia tokens:

```python
from src.utils.token_manager import get_token_manager

token_mgr = get_token_manager()

# Obter token válido (renova automaticamente se necessário)
token = token_mgr.get_valid_token()
```

**Características:**
- Verifica validade do token
- Renova 7 dias antes de expirar
- Obtém tokens de longa duração (60 dias)

### 4.3 Gestão de Secrets

**NUNCA** commite credenciais no código!

#### Desenvolvimento
Use arquivo `.env`:
```bash
cp .env.example .env
# Edite .env com credenciais reais
```

#### Produção
Use variáveis de ambiente ou serviços como:
- **AWS Secrets Manager**
- **HashiCorp Vault**
- **Azure Key Vault**

### 4.4 Scanners de Segurança

#### Snyk (Dependências)
```bash
# Instalar
npm install -g snyk

# Escanear
snyk test
```

#### Bandit (Código Python)
```bash
# Instalar
pip install bandit

# Escanear
bandit -r src
```

#### Safety (Dependências Python)
```bash
# Instalar
pip install safety

# Escanear
safety check
```

---

## 5. Observabilidade

### 5.1 Contexto de Conversação

O módulo `src/utils/context_memory.py` mantém histórico de conversas:

```python
from src.utils.context_memory import get_context_manager

context_mgr = get_context_manager()

# Buscar histórico
history = await context_mgr.get_conversation_history(user_id)

# Adicionar mensagem
await context_mgr.add_message(
    user_id="user123",
    role="user",
    message="Liste campanhas ativas"
)
```

**Benefícios:**
- IA mantém contexto entre conversas
- Análise de preferências do usuário
- Histórico para auditoria

### 5.2 Logs Estruturados

Todos os módulos usam logging estruturado:

```python
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

logger.info("Operação executada", extra={
    'user_id': user_id,
    'campaign_id': campaign_id,
    'duration_ms': 150
})
```

### 5.3 Métricas Prometheus

Endpoint disponível em: `http://localhost:8000/metrics`

**Métricas coletadas:**
- Requests por segundo
- Latência de API
- Erros por tipo
- Campanhas processadas

#### Visualizar no Grafana

1. Adicionar Prometheus como data source
2. Importar dashboard pré-configurado
3. Configurar alertas

---

## 6. Deploy

### 6.1 Desenvolvimento Local

```bash
# Com Python
python main.py

# Com Docker
docker-compose up
```

### 6.2 Produção com Docker

```bash
# Build
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Verificar logs
docker-compose logs -f app

# Executar migrações
docker-compose exec app alembic upgrade head
```

### 6.3 Produção em VPS

#### Pré-requisitos
- Ubuntu 20.04+
- Docker e Docker Compose instalados
- Nginx (opcional, para SSL)

#### Passos

1. **Clonar repositório**
```bash
ssh user@seu-servidor
cd /opt
git clone https://github.com/seu-usuario/facebook-ads-ai-agent.git
cd facebook-ads-ai-agent
```

2. **Configurar variáveis de ambiente**
```bash
cp .env.example .env
nano .env  # Editar com credenciais reais
```

3. **Iniciar aplicação**
```bash
docker-compose up -d
```

4. **Configurar Nginx (SSL)**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **SSL com Let's Encrypt**
```bash
sudo certbot --nginx -d seu-dominio.com
```

### 6.4 Health Checks

```bash
# Verificar saúde da aplicação
curl http://localhost:8000/health

# Verificar status do sistema
curl http://localhost:8000/api/v1/status
```

---

## 7. Troubleshooting

### 7.1 Testes Falhando

#### Problema: Import errors
```
ModuleNotFoundError: No module named 'src'
```

**Solução:**
```bash
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

#### Problema: Database errors nos testes
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solução:**
```bash
# Iniciar banco de teste
docker-compose up -d postgres redis
```

### 7.2 Rate Limit do Facebook

#### Sintoma
```
FacebookRequestError: (#17) User request limit reached
```

**Solução:**
- O sistema já implementa retry automático
- Se persistir, aguarde 30-60 minutos
- Considere usar múltiplas contas de app

### 7.3 Token Expirado

#### Sintoma
```
FacebookRequestError: (#190) Error validating access token
```

**Solução:**
```python
from src.utils.token_manager import get_token_manager

# Forçar renovação
token_mgr = get_token_manager()
new_token = token_mgr.get_long_lived_token()
```

### 7.4 Performance Lenta

#### Sintoma
API responde em >2 segundos

**Soluções:**
1. Verificar índices do banco
2. Habilitar cache Redis
3. Aumentar workers Celery
4. Limitar tamanho de batches

```python
# Em config.py
CELERY_WORKER_CONCURRENCY = 4
BATCH_SIZE = 50
CACHE_TTL = 300  # 5 minutos
```

### 7.5 Memory Leaks

#### Sintoma
Container usa >2GB de RAM

**Soluções:**
1. Limpar cache antigo
```python
await context_mgr.clear_old_conversations(days=7)
```

2. Reiniciar workers periodicamente
```bash
# Adicionar ao cron
0 */6 * * * docker-compose restart worker
```

---

## 8. Checklist de Deploy

Antes de fazer deploy em produção:

### Código
- [ ] Todos os testes passando
- [ ] Coverage > 80%
- [ ] Lint sem erros
- [ ] Secrets removidos do código

### Configuração
- [ ] `.env` configurado corretamente
- [ ] Database URL para produção
- [ ] Tokens válidos
- [ ] Rate limits configurados

### Infraestrutura
- [ ] Docker Compose funcionando
- [ ] Banco de dados inicializado
- [ ] Redis funcionando
- [ ] Nginx configurado (se aplicável)

### Segurança
- [ ] SSL/HTTPS ativado
- [ ] Firewall configurado
- [ ] Backups automáticos
- [ ] Logs de auditoria ativos

### Monitoramento
- [ ] Health checks configurados
- [ ] Alertas configurados
- [ ] Dashboards criados
- [ ] Logs centralizados

### Documentação
- [ ] README atualizado
- [ ] API docs acessíveis
- [ ] Runbook criado
- [ ] Contatos de emergência

---

## 9. Próximos Passos

1. **Expandir Testes**
   - Adicionar testes E2E
   - Testes de carga com Locust
   - Testes de segurança

2. **Melhorar Observabilidade**
   - Integrar OpenTelemetry
   - Distributed tracing
   - APM (Application Performance Monitoring)

3. **Automação Avançada**
   - Auto-scaling baseado em carga
   - Self-healing containers
   - Blue-green deployments

4. **IA Avançada**
   - Fine-tuning de modelos
   - A/B testing de prompts
   - Feedback loop automático

---

**Desenvolvido com ❤️ - Facebook Ads AI Agent v1.0**