# Workflow N8n - Meta Ads → Notion

## Descrição

Este workflow busca métricas do Meta Ads Manager diariamente às 9h da manhã e adiciona automaticamente no database de Métricas & KPIs do Notion.

## Arquivos

- `meta-ads-notion.json` - Workflow principal

## Métricas Coletadas

- Gasto total em ads (R$)
- Alcance
- Impressões
- CTR (Taxa de cliques)
- CPC (Custo por clique)
- CPE (Custo por engajamento)
- Frequência
- Novos seguidores
- Custo por seguidor

## Como Usar

1. Importar workflow no N8n
2. Configurar credenciais (Meta Ads + Notion)
3. Definir variáveis de ambiente
4. Ativar workflow
5. Testar execução manual primeiro

Ver documentação completa em: `../docs/setup-n8n-meta-ads.md`

