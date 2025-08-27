#!/bin/bash

# COMANDOS PARA EXECUTAR DIRETAMENTE NA VPS DE HOMOLOGAÇÃO
# Copie e execute estes comandos na VPS

echo "=== Comandos para corrigir Portainer na VPS ==="
echo ""
echo "Execute estes comandos NA VPS (um por vez):"
echo ""
echo "# 1. Remover Portainer das redes desnecessárias e adicionar à traefik-public:"
echo 'docker service update portainer_portainer --network-rm portainer_default 2>/dev/null'
echo ""
echo "# 2. Adicionar Portainer à rede correta:"
echo 'docker service update portainer_portainer --network-add traefik-public'
echo ""
echo "# 3. Atualizar todas as labels do Portainer (comando único):"
cat << 'EOF'
docker service update portainer_portainer \
  --label-add "traefik.enable=true" \
  --label-add "traefik.docker.network=traefik-public" \
  --label-add "traefik.http.routers.portainer.rule=Host(\`painel.homolog.macspark.dev\`)" \
  --label-add "traefik.http.routers.portainer.entrypoints=web,websecure" \
  --label-add "traefik.http.routers.portainer.service=portainer" \
  --label-add "traefik.http.routers.portainer.tls=true" \
  --label-add "traefik.http.routers.portainer.tls.certresolver=letsencrypt" \
  --label-add "traefik.http.services.portainer.loadbalancer.server.port=9000" \
  --label-add "traefik.http.middlewares.portainer-https.redirectscheme.scheme=https" \
  --label-add "traefik.http.middlewares.portainer-https.redirectscheme.permanent=true" \
  --label-add "traefik.http.routers.portainer-http.rule=Host(\`painel.homolog.macspark.dev\`)" \
  --label-add "traefik.http.routers.portainer-http.entrypoints=web" \
  --label-add "traefik.http.routers.portainer-http.middlewares=portainer-https"
EOF

echo ""
echo "# 4. Verificar se Traefik está rodando:"
echo 'docker service ls | grep traefik'
echo ""
echo "# 5. Se Traefik NÃO estiver rodando, fazer deploy:"
echo 'cd ~/Setup-Macspark && docker stack deploy -c stacks/core/traefik.yml traefik'
echo ""
echo "# 6. Aguardar 30 segundos e testar:"
echo 'sleep 30'
echo 'curl -I -H "Host: painel.homolog.macspark.dev" http://127.0.0.1'
echo 'curl -kI -H "Host: painel.homolog.macspark.dev" https://127.0.0.1'
echo ""
echo "# 7. Verificar logs do Traefik:"
echo 'docker service logs traefik_traefik --tail 50 | grep -E "(portainer|painel)"'
echo ""
echo "# 8. Verificar configuração final:"
echo 'docker service inspect portainer_portainer --format "{{json .Spec.Labels}}" | jq .'