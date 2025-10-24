# 🚀 COMECE AGORA - Passos para Usar o Projeto

**Tempo estimado:** 30-45 minutos  
**Última atualização:** 20 de Outubro, 2025

---

## ✅ O Que Já Está PRONTO

- ✅ Projeto reorganizado e limpo
- ✅ Credenciais Facebook obtidas (App ID, Secret, Token)
- ✅ Supabase configurado e validado
- ✅ Docker configurado
- ✅ Scripts prontos
- ✅ Documentação completa

---

## 🎯 O Que VOCÊ Precisa Fazer (3 Passos)

### **PASSO 1: Configurar Permissões Facebook** ⏱️ 10 minutos

**CRÍTICO:** Sem isso, a coleta de métricas não funciona!

#### 1.1 Acessar Business Manager
```
https://business.facebook.com/settings
```

#### 1.2 Configurar App
1. Menu lateral → **"Contas"** → **"Apps"**
2. Encontrar **"Marketing API"** (ID: 833349949092216)
3. Clicar no app

#### 1.3 Adicionar Permissões
1. Procurar seção **"Contas de anúncios"**
2. Selecionar **"Conta 01"** (act_659480752041234)
3. Adicionar permissões:
   - ✅ `ads_management`
   - ✅ `ads_read`
   - ✅ `business_management`
4. Salvar

#### 1.4 Testar
```powershell
python scripts\test-facebook.py
```

**Deve mostrar:**
```
Status: 200
✅ Conexão com Facebook API funcionando!
Campanhas encontradas: X
```

---

### **PASSO 2: Configurar .env** ⏱️ 15 minutos

#### 2.1 Verificar se .env existe
```powershell
# Se não existir, criar
Copy-Item env.template .env
```

#### 2.2 Editar .env
```powershell
notepad .env
```

#### 2.3 Preencher OBRIGATÓRIAS

**Facebook (JÁ TEMOS):**
```env
FACEBOOK_APP_ID=833349949092216
FACEBOOK_APP_SECRET=7aa2ee153fc3bc26b61693a0fdbccb6b
FACEBOOK_ACCESS_TOKEN=EAA6jvRJIplMBPpYrMQBdwYwIlLrnZAxfRXZCZAN16KXLSe0V2fgItVYlaHVuxpfBu1IoouF0KqvEZBbXEW5pPj6izM589JbQwoUpWOoCxeAX5RZB96v4VhlyKyvfWbq1g5i962rqGPZA2nUAQf5YGZC0Lk9OSZBajRwGLJdI4zGxSNxGfm5cZBuUS7LJBDDUsvxXUQfXmw2ZAg0ZCZBNPFHTecZBncbVbU3VI7ZAwEuupYQGyhPWECH7ju2k53umPlFUnUiTKEsA9gsM0mah2Brz7Wx3bJDQ3O0QZDZD
FACEBOOK_AD_ACCOUNT_ID=act_659480752041234
```

**Supabase (VOCÊ PRECISA OBTER):**
```env
SUPABASE_URL=https://zzpjqldhosgaxyjpcvqc.supabase.co
SUPABASE_SERVICE_KEY=sua_service_key_aqui
```

**Como obter Supabase keys:**
1. Acessar: https://supabase.com/dashboard/project/zzpjqldhosgaxyjpcvqc/settings/api
2. Copiar **"service_role"** key (não a anon)
3. Colar no .env

**Senhas e Keys (GERAR NOVAS):**
```powershell
# Executar para gerar keys aleatórias
.\scripts\setup.ps1
# Copiar as keys geradas e colar no .env
```

Você verá algo assim:
```
ANALYTICS_API_KEY=AbCdEf123456...
SECRET_KEY=XyZ789GhIjKl...
SUPERSET_SECRET_KEY=MnOpQr456789...
```

**Senha do PostgreSQL:**
```env
POSTGRES_PASSWORD=uma_senha_forte_123
```

#### 2.4 Salvar .env
- Salvar arquivo
- Fechar editor

---

### **PASSO 3: Iniciar Sistema** ⏱️ 10 minutos

#### 3.1 Verificar Docker Desktop
```
Abrir Docker Desktop
Aguardar inicializar (ícone fica verde)
```

#### 3.2 Instalar Shared Package
```powershell
cd shared
pip install -e .
cd ..
```

#### 3.3 Subir Serviços
```powershell
docker-compose -f docker-compose.integrated.yml up -d
```

**Aguardar ~2 minutos** para todos os containers iniciarem.

#### 3.4 Verificar Saúde
```powershell
.\scripts\health-check.ps1
```

**Deve mostrar:**
```
✅ Agent API
✅ Metrics Endpoint
✅ Superset
```

---

## 🎉 SISTEMA FUNCIONANDO!

### **Acessar Interfaces:**

**1. API Backend (Swagger):**
```
http://localhost:8000/docs
```
- Explorar endpoints
- Testar interativamente

**2. Apache Superset (Dashboards):**
```
http://localhost:8088
User: admin
Pass: (ver SUPERSET_ADMIN_PASSWORD no .env)
```
- Criar dashboards
- Visualizar métricas

**3. Prometheus (Monitoring):**
```
http://localhost:9090
```
- Ver métricas do sistema

---

## 🧪 TESTAR Fluxo Completo

### Teste 1: Coletar Métricas do Facebook
```powershell
cd analytics\scripts
python metrics-to-supabase.py
```

**Deve:**
1. ✅ Conectar no backend API
2. ✅ Backend buscar do Facebook
3. ✅ Salvar dados no Supabase
4. ✅ Mostrar resumo

### Teste 2: Ver no Supabase
1. Acessar: https://supabase.com/dashboard/project/zzpjqldhosgaxyjpcvqc/editor
2. Abrir tabela `daily_metrics`
3. Ver dados inseridos

### Teste 3: Dashboards
1. Abrir Superset (http://localhost:8088)
2. Conectar ao Supabase
3. Criar visualizações

---

## 🆘 PROBLEMAS COMUNS

### Facebook retorna 403
**Solução:** Voltar ao PASSO 1 e configurar permissões

### Docker não inicia
**Solução:** Abrir Docker Desktop e aguardar inicializar

### Porta em uso
**Solução:** 
```powershell
netstat -ano | findstr :8000
taskkill /PID numero /F
```

### Shared package não encontrado
**Solução:**
```powershell
cd shared
pip install -e .
cd ..
```

---

## 📚 Documentação Completa

**Para saber mais:**
- **Guia Detalhado:** [docs/USER-GUIDE.md](docs/USER-GUIDE.md)
- **Troubleshooting:** [docs/reference/troubleshooting/TROUBLESHOOTING.md](docs/reference/troubleshooting/TROUBLESHOOTING.md)
- **Arquitetura:** [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- **Navegação:** [docs/INDEX.md](docs/INDEX.md)
- **MCP Guide:** [docs/MCP-DOCUMENTATION-GUIDE.md](docs/MCP-DOCUMENTATION-GUIDE.md) (para agentes IA)

---

## ✅ CHECKLIST RÁPIDO

**Antes de começar:**
- [ ] Docker Desktop instalado e rodando
- [ ] Python 3.12+ instalado
- [ ] Git configurado

**Configuração (1x):**
- [ ] Permissões Facebook configuradas (PASSO 1)
- [ ] .env criado e preenchido (PASSO 2)
- [ ] Shared package instalado (PASSO 3.2)

**Uso:**
- [ ] Docker containers rodando (PASSO 3.3)
- [ ] Health check OK (PASSO 3.4)
- [ ] Teste de métricas funcionando

---

## 🎯 TL;DR (Resumo Ultra-Rápido)

```powershell
# 1. Configurar Facebook (manual no site)
https://business.facebook.com/settings

# 2. Editar .env
notepad .env
# Preencher: FACEBOOK_*, SUPABASE_*, POSTGRES_PASSWORD

# 3. Iniciar
docker-compose -f docker-compose.integrated.yml up -d

# 4. Testar
python scripts\test-facebook.py
.\scripts\health-check.ps1

# 5. Usar
cd analytics\scripts
python metrics-to-supabase.py
```

**Pronto! Sistema funcionando!** 🎉

---

**Tempo total:** 30-45 minutos  
**Dificuldade:** Fácil  
**Resultado:** Sistema 100% operacional

---

**Próxima ação:** Executar PASSO 1 (configurar Facebook) → [docs/USER-GUIDE.md](docs/USER-GUIDE.md) tem o guia detalhado!

---

## 🤖 MCP (Model Context Protocol)

Para agentes de IA acessarem a documentação automaticamente:

```bash
# Configurar servidor MCP
cd mcp-server
npm install && npm run build

# Usar com Claude Desktop ou outros clientes MCP
# Ver: docs/MCP-DOCUMENTATION-GUIDE.md
```

**Recursos MCP disponíveis:**
- 🔍 Busca semântica na documentação
- 📖 Leitura de recursos específicos
- 🛠️ Exemplos de código automáticos
- 🆘 Troubleshooting inteligente

