# Instalação Detalhada - Marketing Automation Platform

**Tempo estimado:** 30-45 minutos  
**Última atualização:** 23 de Outubro, 2025  
**Versão:** 2.0.0

---

## 📋 Pré-requisitos Detalhados

### Sistema Operacional
- **Windows:** 10/11 (recomendado)
- **Linux:** Ubuntu 20.04+ ou equivalente
- **macOS:** 12.0+ (Monterey)

### Software Obrigatório

#### 1. Docker Desktop
```bash
# Verificar versão
docker --version
# Deve ser: Docker version 24.0.0+

# Verificar se está rodando
docker ps
```

**Download:** https://www.docker.com/products/docker-desktop/

#### 2. Python 3.12+
```bash
# Verificar versão
python --version
# Deve ser: Python 3.12.0+

# Verificar pip
pip --version
```

**Download:** https://www.python.org/downloads/

#### 3. Git
```bash
# Verificar versão
git --version
# Deve ser: Git 2.40.0+
```

**Download:** https://git-scm.com/downloads

### Contas Necessárias

#### 1. Facebook Business Manager
- **URL:** https://business.facebook.com/
- **Necessário:** App ID, Secret, Access Token
- **Tutorial:** [Setup Facebook API](../guides/operations/SETUP-FACEBOOK-API.md)

#### 2. Supabase (Data Warehouse)
- **URL:** https://supabase.com/
- **Necessário:** Project URL, Service Key
- **Tutorial:** [Setup Supabase](../../analytics/docs/setup-supabase.md)

#### 3. Opcionais
- **Slack:** Para notificações
- **Notion:** Para relatórios
- **N8N:** Para workflows avançados

---

## 🔧 Instalação Passo a Passo

### Fase 1: Preparar Ambiente (10 minutos)

#### 1.1 Clonar Repositório
```bash
# Navegar para diretório desejado
cd C:\Users\marco\Macspark\

# Clonar repositório
git clone https://github.com/Marcocardoso91/marketing-automation.git
cd marketing-automation

# Verificar estrutura
ls -la
```

#### 1.2 Verificar Docker
```bash
# Verificar se Docker está rodando
docker ps

# Se não estiver, iniciar Docker Desktop
# Aguardar ícone ficar verde
```

#### 1.3 Verificar Python
```bash
# Verificar versão
python --version

# Se necessário, instalar Python 3.12+
# https://www.python.org/downloads/
```

### Fase 2: Configurar Credenciais (15 minutos)

#### 2.1 Criar Arquivo .env
```bash
# Copiar template
cp env.template .env

# Abrir para edição
notepad .env  # Windows
# ou
nano .env     # Linux/macOS
```

#### 2.2 Configurar Facebook API
```bash
# No .env, adicionar:
FACEBOOK_APP_ID=833349949092216
FACEBOOK_APP_SECRET=7aa2ee153fc3bc26b61693a0fdbccb6b
FACEBOOK_ACCESS_TOKEN=EAA6jvRJIplMBPpYrMQBdwYwIlLrnZAxfRXZCZAN16KXLSe0V2fgItVYlaHVuxpfBu1IoouF0KqvEZBbXEW5pPj6izM589JbQwoUpWOoCxeAX5RZB96v4VhlyKyvfWbq1g5i962rqGPZA2nUAQf5YGZC0Lk9OSZBajRwGLJdI4zGxSNxGfm5cZBuUS7LJBDDUsvxXUQfXmw2ZAg0ZCZBNPFHTecZBncbVbU3VI7ZAwEuupYQGyhPWECH7ju2k53umPlFUnUiTKEsA9gsM0mah2Brz7Wx3bJDQ3O0QZDZD
FACEBOOK_AD_ACCOUNT_ID=act_659480752041234
```

**Como obter credenciais Facebook:**
1. Acessar https://business.facebook.com/settings
2. Ir em "Contas" → "Apps" → "Marketing API"
3. Copiar App ID e Secret
4. Gerar Access Token (longa duração)

#### 2.3 Configurar Supabase
```bash
# No .env, adicionar:
SUPABASE_URL=https://zzpjqldhosgaxyjpcvqc.supabase.co
SUPABASE_SERVICE_KEY=sua_service_key_aqui
```

**Como obter credenciais Supabase:**
1. Acessar https://supabase.com/dashboard/project/zzpjqldhosgaxyjpcvqc/settings/api
2. Copiar Project URL
3. Copiar service_role key (não a anon)

#### 2.4 Gerar Chaves Automáticas
```bash
# Executar script de setup
.\scripts\setup.ps1  # Windows
# ou
./scripts/setup.sh   # Linux/macOS
```

Este script irá gerar:
- `ANALYTICS_API_KEY`
- `SECRET_KEY`
- `SUPERSET_SECRET_KEY`
- `POSTGRES_PASSWORD`

### Fase 3: Instalar Dependências (10 minutos)

#### 3.1 Instalar Shared Package
```bash
# Navegar para shared
cd shared

# Instalar em modo desenvolvimento
pip install -e .

# Verificar instalação
python -c "from marketing_shared.utils.api_client import AgentAPIClient; print('✅ OK')"

# Voltar para raiz
cd ..
```

#### 3.2 Instalar Dependências do Backend
```bash
# Navegar para backend
cd backend

# Instalar dependências
pip install -r requirements.txt

# Voltar para raiz
cd ..
```

#### 3.3 Instalar Dependências do Analytics
```bash
# Navegar para analytics
cd analytics/scripts

# Instalar dependências
pip install -r requirements.txt

# Voltar para raiz
cd ../..
```

### Fase 4: Iniciar Serviços (10 minutos)

#### 4.1 Subir Stack Completa
```bash
# Subir todos os serviços
docker-compose -f docker-compose.integrated.yml up -d

# Aguardar inicialização (~2-3 minutos)
```

#### 4.2 Verificar Saúde
```bash
# Health check completo
.\scripts\health-check.ps1  # Windows
# ou
./scripts/health-check.sh   # Linux/macOS
```

**Output esperado:**
```
✅ Agent API (http://localhost:8000)
✅ Metrics Endpoint (http://localhost:8000/api/v1/metrics/health)
✅ Superset (http://localhost:8088)
✅ PostgreSQL (localhost:5432)
✅ Redis (localhost:6379)
✅ Prometheus (http://localhost:9090)
```

#### 4.3 Testar Integração
```bash
# Teste 1: API funcionando
curl http://localhost:8000/health

# Teste 2: Coletar métricas
cd analytics/scripts
python metrics-to-supabase.py

# Teste 3: Verificar Supabase
# Acessar: https://supabase.com/dashboard/project/zzpjqldhosgaxyjpcvqc/editor
# Abrir tabela daily_metrics
```

---

## 🎯 Verificação Final

### Checklist de Instalação

#### ✅ Ambiente
- [ ] Docker Desktop rodando
- [ ] Python 3.12+ instalado
- [ ] Git configurado
- [ ] Repositório clonado

#### ✅ Configuração
- [ ] Arquivo .env criado
- [ ] Credenciais Facebook configuradas
- [ ] Credenciais Supabase configuradas
- [ ] Chaves automáticas geradas

#### ✅ Dependências
- [ ] Shared package instalado
- [ ] Backend dependencies instaladas
- [ ] Analytics dependencies instaladas

#### ✅ Serviços
- [ ] Docker containers rodando
- [ ] Health check passando
- [ ] API respondendo
- [ ] Superset acessível

#### ✅ Testes
- [ ] Coleta de métricas funcionando
- [ ] Dados salvos no Supabase
- [ ] Dashboards acessíveis

---

## 🆘 Troubleshooting

### Problemas Comuns

#### Docker não inicia
```bash
# Verificar se Docker Desktop está rodando
docker ps

# Se não estiver:
# 1. Abrir Docker Desktop
# 2. Aguardar inicialização completa
# 3. Verificar se não há conflitos de porta
```

#### Porta em uso
```bash
# Ver o que está usando a porta
netstat -ano | findstr :8000  # Windows
# ou
lsof -i :8000                 # Linux/macOS

# Parar processo
taskkill /PID numero /F       # Windows
# ou
kill -9 PID                   # Linux/macOS
```

#### Shared package não encontrado
```bash
# Reinstalar shared package
cd shared
pip install -e .
cd ..

# Verificar instalação
python -c "import marketing_shared; print('✅ OK')"
```

#### Facebook API retorna 403
1. Verificar se token é válido
2. Verificar se permissões estão configuradas
3. Aguardar propagação (5-10 minutos)
4. Testar com script: `python scripts/test-facebook.py`

#### Supabase não conecta
1. Verificar se URL está correta
2. Verificar se service key está correta
3. Verificar se projeto está ativo
4. Testar conexão: `python analytics/scripts/test-supabase-connection.py`

---

## 📚 Próximos Passos

### Após Instalação Completa

1. **Configurar Dashboards**
   - Acessar Superset: http://localhost:8088
   - Conectar ao Supabase
   - Criar visualizações

2. **Configurar Workflows N8N**
   - Importar workflows: `analytics/n8n-workflows/`
   - Configurar credenciais
   - Ativar workflows

3. **Configurar Alertas**
   - Slack webhook
   - Notion integration
   - Email notifications

4. **Produção**
   - Configurar domínio
   - HTTPS com Let's Encrypt
   - Backups automáticos
   - Monitoring avançado

---

## 🔗 Documentação Relacionada

- **Quick Start:** [QUICK-START.md](QUICK-START.md) (15 min)
- **User Guide:** [USER-GUIDE.md](../USER-GUIDE.md) (uso diário)
- **Architecture:** [ARCHITECTURE.md](../architecture/ARCHITECTURE.md) (entender sistema)
- **Troubleshooting:** [TROUBLESHOOTING.md](../reference/troubleshooting/TROUBLESHOOTING.md) (problemas)
- **API Reference:** [API-REFERENCE.md](../api/agent-api/API-REFERENCE.md) (endpoints)

---

**Tempo total:** 30-45 minutos  
**Dificuldade:** Intermediário  
**Resultado:** Sistema completo e funcional

---

**Próxima ação:** Configurar dashboards → [USER-GUIDE.md](../USER-GUIDE.md) tem o guia de uso!
