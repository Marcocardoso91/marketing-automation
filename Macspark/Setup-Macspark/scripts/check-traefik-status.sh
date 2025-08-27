#!/bin/bash

# Script para verificar status completo do Traefik e serviços
# Para debug de problemas de roteamento

echo "=== Verificação de Status do Traefik ==="
echo ""
echo "Data: $(date)"
echo "Host: $(hostname)"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 1. Verificar Traefik
echo -e "${BLUE}1. Status do Traefik:${NC}"
TRAEFIK_STATUS=$(docker service ls --filter name=traefik --format "table {{.Name}}\t{{.Replicas}}\t{{.Mode}}")
if [ -n "$TRAEFIK_STATUS" ]; then
    echo "$TRAEFIK_STATUS"
    
    # Verificar se Traefik está ouvindo nas portas
    echo ""
    echo "Portas do Traefik:"
    docker service inspect traefik_traefik --format '{{range .Endpoint.Ports}}{{.PublishedPort}}:{{.TargetPort}}/{{.Protocol}} {{end}}' 2>/dev/null || echo "Não foi possível obter portas"
else
    echo -e "${RED}Traefik não está rodando!${NC}"
    echo "Tentando verificar se existe stack Traefik..."
    docker stack ls | grep traefik
fi

# 2. Verificar redes
echo ""
echo -e "${BLUE}2. Redes Docker Overlay:${NC}"
docker network ls --filter driver=overlay --format "table {{.ID}}\t{{.Name}}\t{{.Scope}}"

# 3. Verificar serviços com labels Traefik
echo ""
echo -e "${BLUE}3. Serviços com labels Traefik habilitados:${NC}"
for service in $(docker service ls --format "{{.Name}}"); do
    ENABLED=$(docker service inspect $service --format '{{index .Spec.Labels "traefik.enable"}}' 2>/dev/null)
    if [ "$ENABLED" = "true" ]; then
        HOST=$(docker service inspect $service --format '{{index .Spec.Labels "traefik.http.routers.'${service##*_}'.rule"}}' 2>/dev/null)
        PORT=$(docker service inspect $service --format '{{index .Spec.Labels "traefik.http.services.'${service##*_}'.loadbalancer.server.port"}}' 2>/dev/null)
        echo -e "${GREEN}✓${NC} $service"
        [ -n "$HOST" ] && echo "  Host: $HOST"
        [ -n "$PORT" ] && echo "  Port: $PORT"
    fi
done

# 4. Verificar conectividade de rede do Portainer
echo ""
echo -e "${BLUE}4. Redes do Portainer:${NC}"
docker service inspect portainer_portainer --format '{{range .Spec.TaskTemplate.Networks}}{{.Target}} {{end}}' 2>/dev/null | while read net_id; do
    if [ -n "$net_id" ]; then
        NET_NAME=$(docker network inspect $net_id --format '{{.Name}}' 2>/dev/null)
        echo "  - $NET_NAME (ID: $net_id)"
    fi
done

# 5. Verificar resolução DNS interna
echo ""
echo -e "${BLUE}5. Teste de Resolução DNS:${NC}"
# Verificar IPs
echo "IP Externo: $(curl -s ifconfig.me 2>/dev/null || echo 'Não disponível')"
echo "IPs Locais:"
ip -4 addr show | grep inet | grep -v 127.0.0.1 | awk '{print "  - " $2}'

# 6. Verificar certificados Let's Encrypt
echo ""
echo -e "${BLUE}6. Certificados SSL/TLS:${NC}"
ACME_FILE="/var/lib/docker/volumes/traefik_certificates/_data/acme.json"
if [ -f "$ACME_FILE" ]; then
    echo "Arquivo ACME existe: $ACME_FILE"
    # Verificar certificados no arquivo
    if command -v jq &> /dev/null; then
        CERT_COUNT=$(cat $ACME_FILE 2>/dev/null | jq '.letsencrypt.Certificates | length' 2>/dev/null || echo "0")
        echo "Certificados Let's Encrypt: $CERT_COUNT"
        cat $ACME_FILE 2>/dev/null | jq -r '.letsencrypt.Certificates[].domain.main' 2>/dev/null | while read domain; do
            echo "  - $domain"
        done
    else
        echo "jq não instalado - não é possível listar certificados"
    fi
else
    echo -e "${YELLOW}Arquivo ACME não encontrado${NC}"
fi

# 7. Testar endpoints
echo ""
echo -e "${BLUE}7. Teste de Endpoints:${NC}"
echo ""

# Função para testar endpoint
test_endpoint() {
    local host=$1
    local proto=$2
    local port=$3
    
    echo -n "Testing $proto://$host:$port ... "
    
    if [ "$proto" = "https" ]; then
        CODE=$(curl -k -s -o /dev/null -w "%{http_code}" -H "Host: $host" $proto://127.0.0.1:$port 2>/dev/null)
    else
        CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Host: $host" $proto://127.0.0.1:$port 2>/dev/null)
    fi
    
    case $CODE in
        200) echo -e "${GREEN}✓ OK (200)${NC}" ;;
        301|302|308) echo -e "${GREEN}✓ Redirect ($CODE)${NC}" ;;
        401|403) echo -e "${YELLOW}⚠ Auth Required ($CODE)${NC}" ;;
        404) echo -e "${RED}✗ Not Found ($CODE)${NC}" ;;
        502|503|504) echo -e "${RED}✗ Backend Error ($CODE)${NC}" ;;
        000) echo -e "${RED}✗ Connection Failed${NC}" ;;
        *) echo -e "${YELLOW}? Code: $CODE${NC}" ;;
    esac
}

# Testar Portainer
test_endpoint "painel.homolog.macspark.dev" "http" "80"
test_endpoint "painel.homolog.macspark.dev" "https" "443"

# 8. Logs recentes do Traefik
echo ""
echo -e "${BLUE}8. Logs Recentes do Traefik (erros/avisos):${NC}"
docker service logs traefik_traefik --tail 20 2>&1 | grep -E "(error|ERROR|warn|WARN|portainer|painel)" | tail -10 || echo "Sem logs de erro recentes"

# 9. Diagnóstico rápido
echo ""
echo -e "${BLUE}=== Diagnóstico Rápido ===${NC}"
echo ""

ISSUES=0

# Verificar Traefik
if ! docker service ls | grep -q traefik; then
    echo -e "${RED}✗ Traefik não está rodando${NC}"
    ISSUES=$((ISSUES + 1))
else
    echo -e "${GREEN}✓ Traefik está rodando${NC}"
fi

# Verificar rede
if ! docker network ls | grep -q traefik-public; then
    echo -e "${RED}✗ Rede traefik-public não existe${NC}"
    ISSUES=$((ISSUES + 1))
else
    echo -e "${GREEN}✓ Rede traefik-public existe${NC}"
fi

# Verificar Portainer
if ! docker service ls | grep -q portainer; then
    echo -e "${RED}✗ Portainer não está rodando${NC}"
    ISSUES=$((ISSUES + 1))
else
    echo -e "${GREEN}✓ Portainer está rodando${NC}"
fi

# Verificar label docker.network
DOCKER_NET=$(docker service inspect portainer_portainer --format '{{index .Spec.Labels "traefik.docker.network"}}' 2>/dev/null)
if [ "$DOCKER_NET" = "traefik-public" ]; then
    echo -e "${GREEN}✓ Label traefik.docker.network configurada corretamente${NC}"
else
    echo -e "${RED}✗ Label traefik.docker.network incorreta ou ausente (valor atual: '$DOCKER_NET')${NC}"
    ISSUES=$((ISSUES + 1))
fi

echo ""
if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ Nenhum problema detectado!${NC}"
else
    echo -e "${YELLOW}⚠ $ISSUES problema(s) detectado(s)${NC}"
    echo ""
    echo "Execute o script de correção:"
    echo "  bash scripts/fix-portainer-traefik.sh"
fi