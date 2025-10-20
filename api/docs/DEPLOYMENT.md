# Deployment Guide

Guia completo de deploy do Facebook Ads AI Agent em produção.

## Pré-requisitos

### VPS/Servidor
- Ubuntu 22.04 LTS ou superior
- Mínimo: 8GB RAM, 4 vCPU, 50GB SSD
- Acesso SSH com sudo
- IP público estático

### Domínio
- Domínio registrado (exemplo: fbads.example.com)
- Acesso ao gerenciamento de DNS
- Subdomínios configuráveis:
  - api.fbads.example.com (ou fbads.example.com)
  - grafana.fbads.example.com
  - n8n.fbads.example.com
  - flower.fbads.example.com
  - prometheus.fbads.example.com

### Credenciais
- Facebook App ID, Secret, Access Token
- (Opcional) Slack Webhook URL
- (Opcional) SendGrid API Key

## Provisioning do VPS

### 1. Instalar Docker

```bash
# Update packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Configurar Firewall

```bash
# Install UFW
sudo apt-get install -y ufw

# Configure rules
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Enable firewall
sudo ufw enable
sudo ufw status
```

### 3. Configurar Fail2Ban

```bash
# Install
sudo apt-get install -y fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Start service
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Deploy da Aplicação

### 1. Clonar Repositório

```bash
cd /opt
sudo git clone https://github.com/your-org/facebook-ads-ai-agent.git
cd facebook-ads-ai-agent
sudo chown -R $USER:$USER .
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copy template
cp .env.example .env

# Edit with production values
nano .env
```

**Importante:** Configure TODOS os valores:
- FACEBOOK_* credentials
- POSTGRES_PASSWORD (senha forte!)
- SECRET_KEY (gerar com: `openssl rand -hex 32`)
- SLACK_WEBHOOK_URL
- SENDGRID_API_KEY
- DEBUG=false
- ENVIRONMENT=production

### 3. Configurar DNS

No seu provedor de DNS, adicione registros A:

```
fbads.example.com          A    <seu-ip-vps>
grafana.fbads.example.com  A    <seu-ip-vps>
n8n.fbads.example.com      A    <seu-ip-vps>
flower.fbads.example.com   A    <seu-ip-vps>
prometheus.fbads.example.com A  <seu-ip-vps>
```

**Aguarde propagação DNS:** 30min - 2h

### 4. Deploy Inicial

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run deploy
./scripts/deploy.sh
```

**Aguarde:** 5-10 minutos para build e start

### 5. Verificar SSL

Traefik emitirá certificados Let's Encrypt automaticamente no primeiro acesso.

```bash
# Verificar logs
docker-compose -f docker-compose.prod.yml logs traefik | grep acme

# Aguardar emissão (pode levar 2-5min)
# Testar
curl https://fbads.example.com/health
```

### 6. Validação Pós-Deploy

```bash
# Check all containers
docker-compose -f docker-compose.prod.yml ps

# Health checks
curl https://fbads.example.com/health
# Esperado: {"status":"healthy"...}

curl https://fbads.example.com/metrics
# Esperado: Métricas Prometheus

# Acessar interfaces web
# https://fbads.example.com/docs (Swagger)
# https://grafana.fbads.example.com (Grafana)
# https://n8n.fbads.example.com (n8n)
# https://flower.fbads.example.com (Flower)
```

## Configuração Pós-Deploy

### 1. Importar Workflows n8n

1. Acesse https://n8n.fbads.example.com
2. Login com admin/admin
3. **IMPORTANTE:** Vá em Settings → Change Password
4. Workflows → Import from File
5. Importar cada workflow de `config/n8n/workflows/`
6. Configurar credentials (Facebook, Slack, Email)

Ver [docs/n8n-setup.md](n8n-setup.md) para detalhes

### 2. Configurar Grafana

1. Acesse https://grafana.fbads.example.com
2. Login com admin/admin
3. **IMPORTANTE:** Trocar senha
4. Verificar datasource Prometheus conectado
5. Importar dashboards (se disponíveis)

### 3. Configurar Backup Automático

```bash
# Add to crontab
crontab -e

# Add line:
0 2 * * * cd /opt/facebook-ads-ai-agent && ./scripts/backup.sh >> /var/log/fbads-backup.log 2>&1
```

## Monitoramento

### Métricas Chave

- **API Response Time:** < 500ms (p95)
- **Facebook API Calls:** Taxa de sucesso > 95%
- **Celery Tasks:** Success rate > 99%
- **Uptime:** > 99.5%

### Configurar Alertas

**Prometheus Alertmanager** (configurar se necessário):

```yaml
# config/alertmanager.yml
route:
  receiver: 'slack'

receivers:
  - name: 'slack'
    slack_configs:
      - api_url: '<SLACK_WEBHOOK_URL>'
        channel: '#alerts'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

### Uptime Monitoring Externo

Recomendado: UptimeRobot, Pingdom, ou similar

- Endpoint: https://fbads.example.com/health
- Intervalo: 5 minutos
- Notificar: Email/SMS se down

## Manutenção

### Atualização de Código

```bash
cd /opt/facebook-ads-ai-agent
./scripts/deploy.sh  # Faz pull, build, restart e migrations automaticamente
```

### Atualização de Dependências

```bash
# Edit requirements.txt
nano requirements.txt

# Deploy
./scripts/deploy.sh
```

### Escalar Aplicação

```bash
# Aumentar workers FastAPI (não aplicável com docker-compose, usar load balancer)
# Aumentar workers Celery
docker-compose -f docker-compose.prod.yml up -d --scale celery_worker=3

# Aumentar concorrência por worker
# Edit docker-compose.prod.yml
# command: celery ... --concurrency=8
```

## Rollback

```bash
# Identificar versão anterior
cd /opt/facebook-ads-ai-agent
git log --oneline -n 10

# Checkout versão anterior
git checkout <commit-hash>

# Deploy
./scripts/deploy.sh

# Se migration causou problema
docker-compose -f docker-compose.prod.yml exec app alembic downgrade -1
```

## Troubleshooting

Ver [RUNBOOK.md](RUNBOOK.md) para procedimentos de emergência.

### Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f app
```

### SSL Issues

```bash
# Check Traefik logs
docker-compose -f docker-compose.prod.yml logs traefik | grep -i error

# Renew certificate manually (if needed)
rm letsencrypt/acme.json
docker-compose -f docker-compose.prod.yml restart traefik
```

## Security Checklist

- [ ] Trocar senhas padrão (Grafana, n8n, Flower)
- [ ] Configurar SECRET_KEY forte
- [ ] Usar POSTGRES_PASSWORD segura
- [ ] Configurar HTTPS (Traefik + Let's Encrypt)
- [ ] Configurar Firewall (UFW)
- [ ] Configurar Fail2Ban
- [ ] Desabilitar DEBUG mode
- [ ] Limitar CORS origins em produção
- [ ] Configurar backups automáticos
- [ ] Configurar monitoramento externo

---

**Última atualização:** Outubro 2025

