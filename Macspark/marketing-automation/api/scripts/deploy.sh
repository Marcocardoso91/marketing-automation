#!/bin/bash
set -e

echo "========================================="
echo "Facebook Ads AI Agent - Deploy Script"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}ERROR: .env file not found!${NC}"
    echo "Please create .env from .env.example and configure your credentials"
    exit 1
fi

# Pull latest code
echo -e "${YELLOW}[1/5] Pulling latest code from Git...${NC}"
git pull origin main

# Build images
echo -e "${YELLOW}[2/5] Building Docker images...${NC}"
docker-compose -f docker-compose.prod.yml build --no-cache

# Stop old containers
echo -e "${YELLOW}[3/5] Stopping old containers...${NC}"
docker-compose -f docker-compose.prod.yml down

# Start new containers
echo -e "${YELLOW}[4/5] Starting new containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo -e "${YELLOW}[5/5] Running database migrations...${NC}"
docker-compose -f docker-compose.prod.yml exec -T app alembic upgrade head

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Deploy completed successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Services status:"
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "Access your application at:"
echo "  - API: https://fbads.example.com"
echo "  - Docs: https://fbads.example.com/docs"
echo "  - Grafana: https://grafana.fbads.example.com"
echo "  - n8n: https://n8n.fbads.example.com"
echo "  - Flower: https://flower.fbads.example.com"
echo ""

