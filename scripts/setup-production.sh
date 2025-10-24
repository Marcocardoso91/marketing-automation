#!/bin/bash
# Setup Produção - Marketing Automation Platform
# Versão: 1.0.0
# Data: 23 de Outubro, 2025

set -e

echo "🚀 SETUP PRODUÇÃO - Marketing Automation Platform"
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Verificar se é root
if [ "$EUID" -eq 0 ]; then
    error "Não execute como root! Use um usuário com sudo."
fi

# Verificar sistema operacional
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    error "Este script é apenas para Linux"
fi

log "Verificando pré-requisitos..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    log "Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    success "Docker instalado"
else
    success "Docker já instalado"
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log "Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    success "Docker Compose instalado"
else
    success "Docker Compose já instalado"
fi

# Verificar Git
if ! command -v git &> /dev/null; then
    log "Instalando Git..."
    sudo apt update && sudo apt install -y git
    success "Git instalado"
else
    success "Git já instalado"
fi

# Verificar Nginx
if ! command -v nginx &> /dev/null; then
    log "Instalando Nginx..."
    sudo apt update && sudo apt install -y nginx
    success "Nginx instalado"
else
    success "Nginx já instalado"
fi

# Verificar Certbot
if ! command -v certbot &> /dev/null; then
    log "Instalando Certbot..."
    sudo apt install -y certbot python3-certbot-nginx
    success "Certbot instalado"
else
    success "Certbot já instalado"
fi

log "Configurando firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
success "Firewall configurado"

log "Criando estrutura de diretórios..."
mkdir -p /opt/marketing-automation
mkdir -p /opt/marketing-automation/backups
mkdir -p /opt/marketing-automation/logs
mkdir -p /opt/marketing-automation/ssl
mkdir -p /opt/marketing-automation/monitoring
success "Diretórios criados"

log "Configurando Nginx..."
cat > /opt/marketing-automation/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream api {
        server app:8000;
    }
    
    server {
        listen 80;
        server_name _;
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl;
        server_name _;
        
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
EOF
success "Nginx configurado"

log "Criando script de backup..."
cat > /opt/marketing-automation/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/marketing-automation/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec marketing-postgres pg_dump -U postgres marketing_db > $BACKUP_DIR/postgres.sql

# Backup Redis
docker exec marketing-redis redis-cli BGSAVE
docker cp marketing-redis:/data/dump.rdb $BACKUP_DIR/redis.rdb

# Backup volumes
docker run --rm -v marketing_postgres_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/postgres_data.tar.gz -C /data .

echo "✅ Backup concluído: $BACKUP_DIR"
EOF
chmod +x /opt/marketing-automation/backup.sh
success "Script de backup criado"

log "Criando script de restore..."
cat > /opt/marketing-automation/restore.sh << 'EOF'
#!/bin/bash
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

# Iniciar serviços
docker-compose up -d

echo "✅ Recovery concluído"
EOF
chmod +x /opt/marketing-automation/restore.sh
success "Script de restore criado"

log "Criando script de deploy..."
cat > /opt/marketing-automation/deploy.sh << 'EOF'
#!/bin/bash
# Deploy automatizado

echo "🚀 Iniciando deploy..."

# 1. Backup antes do deploy
./backup.sh

# 2. Pull latest code
git pull origin main

# 3. Build novas imagens
docker-compose -f docker-compose.prod.yml build

# 4. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 5. Health check
sleep 30
curl -f http://localhost:8000/health || {
    echo "❌ Health check falhou, fazendo rollback..."
    ./restore.sh backups/$(ls -t backups/ | head -1)
    exit 1
}

echo "✅ Deploy concluído com sucesso!"
EOF
chmod +x /opt/marketing-automation/deploy.sh
success "Script de deploy criado"

log "Configurando cron para backup diário..."
echo "0 2 * * * cd /opt/marketing-automation && ./backup.sh" | sudo crontab -
success "Cron configurado"

log "Criando usuário de sistema..."
sudo useradd -r -s /bin/false marketing-automation
sudo chown -R marketing-automation:marketing-automation /opt/marketing-automation
success "Usuário de sistema criado"

log "Configurando logrotate..."
sudo tee /etc/logrotate.d/marketing-automation << 'EOF'
/opt/marketing-automation/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 marketing-automation marketing-automation
}
EOF
success "Logrotate configurado"

echo ""
echo "🎉 SETUP PRODUÇÃO CONCLUÍDO!"
echo "=============================="
echo ""
echo "📁 Diretório: /opt/marketing-automation"
echo "🔧 Scripts disponíveis:"
echo "   - backup.sh    - Backup automático"
echo "   - restore.sh   - Restore do backup"
echo "   - deploy.sh    - Deploy automatizado"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Copiar código para /opt/marketing-automation"
echo "2. Configurar .env.prod"
echo "3. Configurar domínio e SSL"
echo "4. Executar: ./deploy.sh"
echo ""
echo "📚 Documentação: docs/operations/PRODUCTION-DEPLOYMENT-GUIDE.md"
echo ""
success "Setup produção finalizado!"
