# Deploy VPS Homologação - Guia Completo

## 🚀 Deploy Rápido (Comando Único)

Na VPS, execute:

```bash
cd ~/Setup-Macspark
git pull
bash scripts/deployment/deploy-homolog-complete.sh
```

## 🔧 Correção Manual do Problema Atual

O erro que você está enfrentando é porque o comando estava usando `<TRAEFIK_NET>` literalmente. Aqui está a correção:

### 1. Comando Correto para Atualizar o Portainer (execute na VPS):

```bash
docker service update portainer_portainer \
  --network-add traefik-public \
  --label-add "traefik.enable=true" \
  --label-add "traefik.docker.network=traefik-public" \
  --label-add "traefik.http.routers.portainer.rule=Host(\`painel.homolog.macspark.dev\`)" \
  --label-add "traefik.http.routers.portainer.entrypoints=web,websecure" \
  --label-add "traefik.http.routers.portainer.service=portainer" \
  --label-add "traefik.http.routers.portainer.tls=true" \
  --label-add "traefik.http.routers.portainer.tls.certresolver=letsencrypt" \
  --label-add "traefik.http.services.portainer.loadbalancer.server.port=9000"
```

### 2. Verificar se Funcionou:

```bash
# Teste local
curl -I -H "Host: painel.homolog.macspark.dev" http://127.0.0.1

# Ver logs do Traefik
docker service logs traefik_traefik --tail 50 | grep portainer
```

## 📋 Checklist de Problemas Comuns

### ✅ Rede traefik-public existe?
```bash
docker network ls | grep traefik-public
```
**Solução se não existir:**
```bash
docker network create --driver=overlay --attachable traefik-public
```

### ✅ Traefik está rodando?
```bash
docker service ls | grep traefik
```
**Solução se não estiver:**
```bash
cd ~/Setup-Macspark
docker stack deploy -c setup-macspark/stacks/core/traefik/traefik-homolog.yml traefik
```

### ✅ Portainer está na rede correta?
```bash
docker service inspect portainer_portainer --format '{{range .Spec.TaskTemplate.Networks}}{{.Target}} {{end}}'
```
**Deve incluir a rede traefik-public**

### ✅ Labels corretas no Portainer?
```bash
docker service inspect portainer_portainer --format '{{index .Spec.Labels "traefik.docker.network"}}'
```
**Deve retornar: traefik-public**

## 🌐 Configuração DNS

Adicione estes registros no seu provedor DNS:

| Tipo | Nome | Valor | TTL |
|------|------|-------|-----|
| A | painel.homolog.macspark.dev | IP_DA_VPS | 300 |
| A | traefik.homolog.macspark.dev | IP_DA_VPS | 300 |

**Obter IP da VPS:**
```bash
curl ifconfig.me
```

## 📁 Arquivos Criados/Atualizados

### Configurações:
- `/setup-macspark/stacks/core/traefik/traefik-homolog.yml` - Configuração Traefik para homologação
- `/setup-macspark/stacks/applications/development/portainer-homolog.yml` - Configuração Portainer

### Scripts de Deploy:
- `/scripts/deployment/deploy-homolog-complete.sh` - Deploy completo automático
- `/scripts/fix-portainer-traefik.sh` - Correção específica do Portainer
- `/scripts/check-traefik-status.sh` - Verificação de status
- `/scripts/vps-fix-commands.sh` - Comandos manuais para correção

## 🔍 Debug e Troubleshooting

### Ver todos os logs do Traefik:
```bash
docker service logs traefik_traefik -f
```

### Ver labels do Portainer:
```bash
docker service inspect portainer_portainer --format '{{json .Spec.Labels}}' | jq .
```

### Testar certificado SSL:
```bash
openssl s_client -connect painel.homolog.macspark.dev:443 -servername painel.homolog.macspark.dev
```

### Verificar portas abertas:
```bash
netstat -tlnp | grep -E "(:80|:443|:8080)"
```

## 🎯 URLs de Acesso

Após configuração completa:

- **Portainer**: https://painel.homolog.macspark.dev
- **Traefik Dashboard**: https://traefik.homolog.macspark.dev
  - Usuário: `admin`
  - Senha: `admin123`

## 🔄 Sincronização com Repositório

Para atualizar os arquivos na VPS com as últimas mudanças:

```bash
cd ~/Setup-Macspark
git pull origin main
```

## ⚠️ Notas Importantes

1. **Certificados SSL**: O ambiente de homologação usa certificados de staging do Let's Encrypt. Eles aparecerão como "não confiáveis" no navegador, mas isso é normal para homologação.

2. **Tempo de Propagação DNS**: Após configurar o DNS, pode levar até 48 horas para propagar completamente.

3. **Firewall**: Certifique-se que as portas 80, 443 e 8080 estão abertas no firewall da VPS.

4. **Modo Swarm**: O Docker precisa estar em modo Swarm. O script verifica e inicializa automaticamente se necessário.

## 📞 Suporte

Se encontrar problemas:

1. Execute o script de verificação:
   ```bash
   bash scripts/check-traefik-status.sh
   ```

2. Verifique os logs:
   ```bash
   docker service logs traefik_traefik --tail 100
   docker service logs portainer_portainer --tail 100
   ```

3. Confirme a conectividade de rede:
   ```bash
   docker network inspect traefik-public
   ```

---

**Última atualização**: 27/08/2025
**Versão**: 1.0.0
**Ambiente**: Homologação