#!/bin/bash

# Script para corrigir configuração do Portainer com Traefik
# Para ambiente de homologação

echo "=== Correção da Configuração Portainer + Traefik ==="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está no modo Swarm
if ! docker info 2>/dev/null | grep -q "Swarm: active"; then
    echo -e "${RED}Erro: Docker não está em modo Swarm${NC}"
    exit 1
fi

# 1. Verificar rede traefik-public
echo "1. Verificando rede traefik-public..."
TRAEFIK_NET=$(docker network ls --filter name=traefik-public --format "{{.Name}}")
if [ -z "$TRAEFIK_NET" ]; then
    echo -e "${RED}Erro: Rede traefik-public não encontrada${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Rede encontrada: $TRAEFIK_NET${NC}"

# 2. Verificar se o Traefik está rodando
echo ""
echo "2. Verificando serviço Traefik..."
TRAEFIK_SERVICE=$(docker service ls --filter name=traefik --format "{{.Name}}")
if [ -z "$TRAEFIK_SERVICE" ]; then
    echo -e "${YELLOW}Aviso: Serviço Traefik não encontrado. Tentando criar...${NC}"
    # Deploy do Traefik se não existir
    docker stack deploy -c stacks/core/traefik.yml traefik
    sleep 10
fi
echo -e "${GREEN}✓ Traefik está rodando${NC}"

# 3. Atualizar Portainer com configuração completa
echo ""
echo "3. Atualizando configuração do Portainer..."

docker service update portainer_portainer \
  --network-add traefik-public \
  --label-add "traefik.enable=true" \
  --label-add "traefik.docker.network=traefik-public" \
  --label-add "traefik.http.routers.portainer.rule=Host(\`painel.homolog.macspark.dev\`)" \
  --label-add "traefik.http.routers.portainer.entrypoints=web,websecure" \
  --label-add "traefik.http.routers.portainer.service=portainer" \
  --label-add "traefik.http.routers.portainer.tls=true" \
  --label-add "traefik.http.routers.portainer.tls.certresolver=letsencrypt" \
  --label-add "traefik.http.services.portainer.loadbalancer.server.port=9000" \
  --label-add "traefik.http.middlewares.portainer-redirect.redirectscheme.scheme=https" \
  --label-add "traefik.http.middlewares.portainer-redirect.redirectscheme.permanent=true" \
  --label-add "traefik.http.routers.portainer-http.rule=Host(\`painel.homolog.macspark.dev\`)" \
  --label-add "traefik.http.routers.portainer-http.entrypoints=web" \
  --label-add "traefik.http.routers.portainer-http.middlewares=portainer-redirect" \
  --constraint-add "node.role==manager"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Portainer atualizado com sucesso${NC}"
else
    echo -e "${RED}✗ Erro ao atualizar Portainer${NC}"
    exit 1
fi

# 4. Verificar DNS
echo ""
echo "4. Verificando resolução DNS..."
DNS_IP=$(dig +short painel.homolog.macspark.dev)
SERVER_IP=$(curl -s ifconfig.me)

if [ -z "$DNS_IP" ]; then
    echo -e "${YELLOW}Aviso: DNS não configurado para painel.homolog.macspark.dev${NC}"
    echo "Por favor, configure o DNS apontando para: $SERVER_IP"
else
    echo -e "${GREEN}✓ DNS configurado: painel.homolog.macspark.dev -> $DNS_IP${NC}"
    if [ "$DNS_IP" != "$SERVER_IP" ]; then
        echo -e "${YELLOW}Aviso: DNS aponta para $DNS_IP mas servidor tem IP $SERVER_IP${NC}"
    fi
fi

# 5. Aguardar convergência
echo ""
echo "5. Aguardando convergência do serviço (30 segundos)..."
sleep 30

# 6. Testar acesso
echo ""
echo "6. Testando acesso ao Portainer..."
echo ""

# Teste HTTP local
echo "Teste local HTTP:"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Host: painel.homolog.macspark.dev" http://127.0.0.1)
if [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "308" ]; then
    echo -e "${GREEN}✓ Redirecionamento HTTP -> HTTPS funcionando (código: $HTTP_CODE)${NC}"
elif [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Portainer acessível via HTTP (código: $HTTP_CODE)${NC}"
else
    echo -e "${YELLOW}✗ Resposta HTTP inesperada (código: $HTTP_CODE)${NC}"
fi

# Teste HTTPS local
echo ""
echo "Teste local HTTPS:"
HTTPS_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" -H "Host: painel.homolog.macspark.dev" https://127.0.0.1)
if [ "$HTTPS_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Portainer acessível via HTTPS (código: $HTTPS_CODE)${NC}"
else
    echo -e "${YELLOW}✗ Resposta HTTPS (código: $HTTPS_CODE)${NC}"
fi

# 7. Verificar logs
echo ""
echo "7. Últimas linhas dos logs do Traefik:"
docker service logs traefik_traefik --tail 5 2>/dev/null | grep -E "(portainer|painel.homolog.macspark.dev)" || echo "Sem logs relevantes"

echo ""
echo "=== Diagnóstico Completo ==="
echo ""
echo "Informações do serviço Portainer:"
docker service inspect portainer_portainer --format '{{range .Spec.Labels}}{{println .}}{{end}}' | grep traefik

echo ""
echo "=== Próximos Passos ==="
echo ""
echo "1. Verifique se o DNS está configurado corretamente:"
echo "   - Adicione um registro A ou CNAME para: painel.homolog.macspark.dev -> $SERVER_IP"
echo ""
echo "2. Se usando Cloudflare:"
echo "   - Certifique-se que o proxy está desabilitado (nuvem cinza) inicialmente"
echo "   - Ou configure um tunnel Cloudflare adequadamente"
echo ""
echo "3. Acesse:"
echo "   - HTTP:  http://painel.homolog.macspark.dev"
echo "   - HTTPS: https://painel.homolog.macspark.dev"
echo ""
echo "4. Para debug adicional:"
echo "   docker service logs traefik_traefik -f"
echo "   docker service logs portainer_portainer -f"