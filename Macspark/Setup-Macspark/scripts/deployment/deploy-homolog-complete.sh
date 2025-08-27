#!/bin/bash

# Script completo de deploy para ambiente de homologação
# Este script configura Traefik e Portainer corretamente

set -e  # Parar em caso de erro

echo "╔══════════════════════════════════════════════════════╗"
echo "║    Deploy Completo - Ambiente de Homologação        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Função para verificar status
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        exit 1
    fi
}

# 1. Verificar se está no modo Swarm
echo -e "${BLUE}[1/8] Verificando Docker Swarm...${NC}"
if ! docker info 2>/dev/null | grep -q "Swarm: active"; then
    echo "Inicializando Docker Swarm..."
    docker swarm init --advertise-addr $(hostname -I | awk '{print $1}')
    check_status "Docker Swarm inicializado"
else
    check_status "Docker Swarm já está ativo"
fi

# 2. Criar rede traefik-public
echo ""
echo -e "${BLUE}[2/8] Criando rede overlay traefik-public...${NC}"
if ! docker network ls | grep -q "traefik-public"; then
    docker network create --driver=overlay --attachable traefik-public
    check_status "Rede traefik-public criada"
else
    check_status "Rede traefik-public já existe"
fi

# 3. Remover stacks antigos se existirem
echo ""
echo -e "${BLUE}[3/8] Limpando stacks antigos...${NC}"
docker stack rm traefik 2>/dev/null || true
docker stack rm portainer 2>/dev/null || true
sleep 10  # Aguardar remoção completa
check_status "Stacks antigos removidos"

# 4. Deploy do Traefik
echo ""
echo -e "${BLUE}[4/8] Fazendo deploy do Traefik...${NC}"
docker stack deploy -c ~/Setup-Macspark/setup-macspark/stacks/core/traefik/traefik-homolog.yml traefik
check_status "Traefik deployed"

# 5. Aguardar Traefik estar pronto
echo ""
echo -e "${BLUE}[5/8] Aguardando Traefik inicializar (30 segundos)...${NC}"
sleep 30

# Verificar se Traefik está rodando
TRAEFIK_RUNNING=$(docker service ls --filter name=traefik_traefik --format "{{.Replicas}}")
if [[ "$TRAEFIK_RUNNING" == *"1/1"* ]]; then
    check_status "Traefik está rodando"
else
    echo -e "${YELLOW}⚠ Traefik pode não estar totalmente pronto${NC}"
fi

# 6. Deploy do Portainer
echo ""
echo -e "${BLUE}[6/8] Fazendo deploy do Portainer...${NC}"
docker stack deploy -c ~/Setup-Macspark/setup-macspark/stacks/applications/development/portainer-homolog.yml portainer
check_status "Portainer deployed"

# 7. Aguardar Portainer estar pronto
echo ""
echo -e "${BLUE}[7/8] Aguardando Portainer inicializar (30 segundos)...${NC}"
sleep 30

# 8. Verificação final
echo ""
echo -e "${BLUE}[8/8] Verificação final...${NC}"
echo ""

# Listar serviços
echo "Serviços em execução:"
docker service ls | grep -E "(traefik|portainer)"

echo ""
echo "═══════════════════════════════════════════════════════"
echo ""

# Obter IP externo
EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || echo "IP não detectado")

echo -e "${GREEN}✅ Deploy concluído com sucesso!${NC}"
echo ""
echo "Informações de acesso:"
echo "──────────────────────"
echo ""
echo "1. Configure o DNS apontando para: ${GREEN}$EXTERNAL_IP${NC}"
echo ""
echo "2. Adicione os seguintes registros DNS:"
echo "   - painel.homolog.macspark.dev → $EXTERNAL_IP"
echo "   - traefik.homolog.macspark.dev → $EXTERNAL_IP"
echo ""
echo "3. URLs de acesso (após configurar DNS):"
echo "   - Portainer: ${BLUE}https://painel.homolog.macspark.dev${NC}"
echo "   - Traefik Dashboard: ${BLUE}https://traefik.homolog.macspark.dev${NC}"
echo "     (user: admin, senha: admin123)"
echo ""
echo "4. Para testar localmente (sem DNS):"
echo "   curl -H 'Host: painel.homolog.macspark.dev' http://$EXTERNAL_IP"
echo ""
echo "5. Monitorar logs:"
echo "   docker service logs -f traefik_traefik"
echo "   docker service logs -f portainer_portainer"
echo ""
echo "═══════════════════════════════════════════════════════"

# Teste rápido
echo ""
echo "Teste rápido de conectividade:"
echo "──────────────────────────────"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Host: painel.homolog.macspark.dev" http://127.0.0.1 2>/dev/null)
if [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "308" ]; then
    echo -e "${GREEN}✓${NC} Redirecionamento HTTP→HTTPS funcionando (código: $HTTP_CODE)"
elif [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Portainer acessível via HTTP"
else
    echo -e "${YELLOW}⚠${NC} Resposta HTTP: $HTTP_CODE (pode levar alguns minutos para ficar pronto)"
fi

echo ""
echo "Script finalizado em: $(date)"