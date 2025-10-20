# Script Python - Meta Ads → Notion

## Descrição

Script backup para buscar métricas do Meta Ads e adicionar no Notion caso o N8n falhe.

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Configuração

1. Copiar `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Editar `.env` e preencher os valores:
   - Ver `../docs/setup-n8n-meta-ads.md` para obter tokens

## Uso

### Execução Manual

```bash
python meta-to-notion.py
```

### Execução Agendada (Windows - Task Scheduler)

1. Abrir **Task Scheduler**
2. Criar nova tarefa
3. Trigger: Diário às 9h
4. Action: Executar `python C:\caminho\meta-to-notion.py`

### Execução Agendada (Linux/Mac - Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha (executa todo dia às 9h)
0 9 * * * cd /caminho/scripts && python meta-to-notion.py >> logs.txt 2>&1
```

## Saída Esperada

```
🚀 Iniciando coleta de métricas...
📅 Data: 2025-10-18 09:00:00

📊 Buscando dados do Meta Ads...
✅ 2 campanhas encontradas

⚙️ Processando métricas...
📈 Resumo das métricas:
   Gasto: R$ 40.00
   Alcance: 3,200
   CTR: 1.50%
   CPE: R$ 0.45
   Novos Seguidores: 26
   Custo/Seguidor: R$ 1.54

📝 Adicionando no Notion...

✅ Processo concluído com sucesso!
🔗 Acesse: https://www.notion.so/e344b2ff2ded4418b93413b9dbd2e131
```

## Troubleshooting

Ver documentação completa em: `../docs/setup-n8n-meta-ads.md`

