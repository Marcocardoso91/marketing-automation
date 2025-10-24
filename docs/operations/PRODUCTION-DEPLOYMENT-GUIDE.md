# 🚀 Guia de Deploy em Produção - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 🎯 O Que Falta Para Produção

### ❌ **CRÍTICO - Obrigatório**
1. **Configuração de Domínio e SSL**
2. **Secrets Management (Produção)**
3. **Monitoramento e Alertas**
4. **Backup e Recovery**
5. **Testes de Carga**

### ⚠️ **IMPORTANTE - Recomendado**
6. **CI/CD Pipeline Completo**
7. **Logs Centralizados**
8. **Métricas de Performance**
9. **Segurança Avançada**

### 🟢 **DESEJÁVEL - Opcional**
10. **Auto-scaling**
11. **Multi-region**
12. **Disaster Recovery**

---

## 🏗️ **PLANO DE IMPLEMENTAÇÃO**

### **Fase 1: Infraestrutura Básica (1-2 dias)**

#### 1.1 Configurar Servidor de Produção

**Requisitos Mínimos:**
- **CPU:** 4 cores
- **RAM:** 8GB
- **Storage:** 50GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Docker:** 24.0+
- **Docker Compose:** 2.20+

**Configuração:**
```bash
# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Configurar firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

#### 1.2 Configurar Domínio e SSL

**Opção A: Traefik + Let's Encrypt (Recomendado)**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  traefik:
    image: traefik:v2.10
    container_name: marketing-traefik
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@seudominio.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    restart: unless-stopped
```

**Opção B: Nginx + Certbot**
```bash
# Instalar Nginx
sudo apt install nginx certbot python3-certbot-nginx

# Configurar certificado SSL
sudo certbot --nginx -d seudominio.com -d api.seudominio.com
```

#### 1.3 Secrets Management

**Criar arquivo `.env.prod`:**
```bash
# ========================================
# PRODUÇÃO - CONFIGURAÇÕES CRÍTICAS
# ========================================

# Facebook API (OBRIGATÓRIO)
FACEBOOK_APP_ID=seu_app_id_real
FACEBOOK_APP_SECRET=seu_app_secret_real
FACEBOOK_ACCESS_TOKEN=seu_token_real
FACEBOOK_AD_ACCOUNT_ID=act_123456789

# Database (OBRIGATÓRIO)
POSTGRES_PASSWORD=senha_super_forte_64_chars
SECRET_KEY=chave_secreta_64_chars_minimo
ANALYTICS_API_KEY=chave_analytics_64_chars_minimo

# Supabase (OBRIGATÓRIO)
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua_chave_anonima_real
SUPABASE_SERVICE_KEY=sua_service_key_real

# N8N (OBRIGATÓRIO)
N8N_WEBHOOK_URL=https://fluxos.macspark.dev/webhook
N8N_API_URL=https://fluxos.macspark.dev/api/v1
N8N_API_KEY=sua_chave_n8n_real

# Segurança
ALLOWED_ORIGINS=https://seudominio.com,https://api.seudominio.com
TRUSTED_HOSTS=seudominio.com,api.seudominio.com
ENVIRONMENT=production
DEBUG=false

# Notificações (OPCIONAL)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/SEU/WEBHOOK/REAL
NOTION_API_TOKEN=secret_sua_chave_notion_real
```

### **Fase 2: Monitoramento e Logs (1 dia)**

#### 2.1 Prometheus + Grafana

**docker-compose.monitoring.yml:**
```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: marketing-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: marketing-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=senha_admin_grafana
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

#### 2.2 Logs Centralizados

**ELK Stack (Elasticsearch + Logstash + Kibana):**
```yaml
# docker-compose.logging.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: marketing-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    restart: unless-stopped

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: marketing-kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    restart: unless-stopped
```

### **Fase 3: Backup e Recovery (1 dia)**

#### 3.1 Backup Automático

**Script de Backup (`scripts/backup.sh`):**
```bash
#!/bin/bash
# Backup completo do sistema

BACKUP_DIR="/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec marketing-postgres pg_dump -U postgres marketing_db > $BACKUP_DIR/postgres.sql

# Backup Redis
docker exec marketing-redis redis-cli BGSAVE
docker cp marketing-redis:/data/dump.rdb $BACKUP_DIR/redis.rdb

# Backup volumes
docker run --rm -v marketing_postgres_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/postgres_data.tar.gz -C /data .

# Backup configurações
cp -r . $BACKUP_DIR/config/

# Upload para S3 (opcional)
aws s3 sync $BACKUP_DIR s3://seu-bucket/backups/$(date +%Y%m%d)/

echo "✅ Backup concluído: $BACKUP_DIR"
```

#### 3.2 Recovery

**Script de Recovery (`scripts/restore.sh`):**
```bash
#!/bin/bash
# Restore do sistema

BACKUP_DIR=$1
if [ -z "$BACKUP_DIR" ]; then
    echo "❌ Uso: $0 <diretorio_backup>"
    exit 1
fi

# Parar serviços
docker-compose down

# Restore PostgreSQL
docker exec marketing-postgres psql -U postgres -c "DROP DATABASE IF EXISTS marketing_db;"
docker exec marketing-postgres psql -U postgres -c "CREATE DATABASE marketing_db;"
docker exec -i marketing-postgres psql -U postgres marketing_db < $BACKUP_DIR/postgres.sql

# Restore Redis
docker cp $BACKUP_DIR/redis.rdb marketing-redis:/data/dump.rdb
docker restart marketing-redis

# Restore volumes
docker run --rm -v marketing_postgres_data:/data -v $BACKUP_DIR:/backup alpine tar xzf /backup/postgres_data.tar.gz -C /data

# Iniciar serviços
docker-compose up -d

echo "✅ Recovery concluído"
```

### **Fase 4: Testes de Carga (1 dia)**

#### 4.1 Locust Load Testing

**locustfile.py:**
```python
from locust import HttpUser, task, between

class MarketingAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def get_campaigns(self):
        self.client.get("/api/v1/campaigns", headers=self.headers)
    
    @task(2)
    def get_analytics(self):
        self.client.get("/api/v1/analytics/dashboard", headers=self.headers)
    
    @task(1)
    def export_metrics(self):
        self.client.get("/api/v1/metrics/export?date_from=2025-10-20&date_until=2025-10-23", 
                       headers={"X-API-Key": "test_key"})
```

**Executar Testes:**
```bash
# Instalar Locust
pip install locust

# Executar testes
locust -f locustfile.py --host=http://localhost:8000 --users=100 --spawn-rate=10
```

### **Fase 5: CI/CD Pipeline (1 dia)**

#### 5.1 GitHub Actions Completo

**.github/workflows/deploy.yml:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*.*.*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/marketing-automation
            git pull origin main
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
            docker system prune -f
```

#### 5.2 Blue-Green Deployment

**Script de Deploy (`scripts/deploy.sh`):**
```bash
#!/bin/bash
# Blue-Green Deployment

# 1. Build nova versão
docker-compose -f docker-compose.prod.yml build

# 2. Testar nova versão
docker-compose -f docker-compose.prod.yml up -d --scale app=0
docker-compose -f docker-compose.prod.yml up -d app-new

# 3. Health check
curl -f http://localhost:8001/health || exit 1

# 4. Switch traffic
docker-compose -f docker-compose.prod.yml stop app
docker-compose -f docker-compose.prod.yml up -d app-new
docker-compose -f docker-compose.prod.yml rename app-old app
docker-compose -f docker-compose.prod.yml rename app-new app

echo "✅ Deploy concluído"
```

---

## 🔧 **CONFIGURAÇÕES DE PRODUÇÃO**

### **Docker Compose Produção**

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  app:
    build: ./backend
    container_name: marketing-api
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    env_file:
      - .env.prod
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'

  postgres:
    image: postgres:15-alpine
    container_name: marketing-postgres
    environment:
      - POSTGRES_DB=marketing_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

  redis:
    image: redis:7-alpine
    container_name: marketing-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.25'

  nginx:
    image: nginx:alpine
    container_name: marketing-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### **Nginx Configuration**

**nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server app:8000;
    }
    
    server {
        listen 80;
        server_name seudominio.com;
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl;
        server_name seudominio.com;
        
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

---

## 📊 **MONITORAMENTO E ALERTAS**

### **Métricas Essenciais**

1. **Performance:**
   - Response time < 200ms
   - Throughput > 1000 req/min
   - Error rate < 1%

2. **Recursos:**
   - CPU < 70%
   - RAM < 80%
   - Disk < 85%

3. **Aplicação:**
   - Health checks
   - Database connections
   - Cache hit rate

### **Alertas Configurados**

**Prometheus Rules:**
```yaml
groups:
  - name: marketing-automation
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
      
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
```

---

## 🚨 **CHECKLIST DE PRODUÇÃO**

### **Pré-Deploy**
- [ ] ✅ Servidor configurado (4 cores, 8GB RAM)
- [ ] ✅ Domínio configurado e SSL válido
- [ ] ✅ Secrets configurados (.env.prod)
- [ ] ✅ Backup configurado
- [ ] ✅ Monitoramento configurado
- [ ] ✅ Testes de carga executados
- [ ] ✅ CI/CD pipeline funcionando

### **Deploy**
- [ ] ✅ Docker Compose produção
- [ ] ✅ Nginx configurado
- [ ] ✅ SSL funcionando
- [ ] ✅ Health checks passando
- [ ] ✅ Logs centralizados
- [ ] ✅ Métricas coletando

### **Pós-Deploy**
- [ ] ✅ Testes de integração
- [ ] ✅ Alertas configurados
- [ ] ✅ Backup automático
- [ ] ✅ Documentação atualizada
- [ ] ✅ Equipe treinada

---

## 🎯 **CRONOGRAMA RECOMENDADO**

| **Dia** | **Atividade** | **Duração** | **Responsável** |
|---------|---------------|-------------|-----------------|
| **1** | Configurar servidor + domínio | 8h | DevOps |
| **2** | Secrets + SSL + Docker | 8h | DevOps |
| **3** | Monitoramento + Logs | 8h | DevOps |
| **4** | Backup + Recovery | 8h | DevOps |
| **5** | Testes de carga | 8h | QA |
| **6** | CI/CD Pipeline | 8h | DevOps |
| **7** | Deploy + Testes | 8h | Full Team |

**Total:** 7 dias (56 horas)

---

## 💰 **CUSTOS ESTIMADOS**

### **Infraestrutura (Mensal)**
- **Servidor:** $50-100/mês
- **Domínio:** $15/ano
- **SSL:** Gratuito (Let's Encrypt)
- **Monitoramento:** $20-50/mês
- **Backup:** $10-30/mês

**Total:** ~$80-180/mês

### **Ferramentas (Opcional)**
- **Datadog:** $15/host/mês
- **New Relic:** $25/host/mês
- **Sentry:** $26/mês

---

## 🔗 **RECURSOS ADICIONAIS**

### **Documentação**
- [Guia de Troubleshooting](../reference/troubleshooting/TROUBLESHOOTING.md)
- [Configuração ENV](../reference/configuration/ENV-VARS.md)
- [API Reference](../api/agent-api/API-REFERENCE.md)

### **Scripts**
- `scripts/setup.ps1` - Setup inicial
- `scripts/health-check.ps1` - Health check
- `scripts/backup.sh` - Backup automático
- `scripts/deploy.sh` - Deploy automatizado

### **Suporte**
- **GitHub Issues:** [Criar issue](https://github.com/your-repo/issues)
- **Documentação:** [docs/INDEX.md](../INDEX.md)

---

**💡 Dica:** Comece pela Fase 1 (Infraestrutura Básica) e vá implementando gradualmente!
