.PHONY: help install test run clean docker-build docker-run setup-local-llms format lint dev-install logs health-check docs

# Variáveis
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy

# Cores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Mostrar esta mensagem de ajuda
	@echo "$(BLUE)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instalar dependências
	@echo "$(YELLOW)Instalando dependências...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependências instaladas$(NC)"

install-dev: ## Instalar dependências de desenvolvimento
	@echo "$(YELLOW)Instalando dependências de desenvolvimento...$(NC)"
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .
	@echo "$(GREEN)✓ Dependências de desenvolvimento instaladas$(NC)"

test: ## Executar testes
	@echo "$(YELLOW)Executando testes...$(NC)"
	$(PYTEST) tests/ -v --cov=mcp_orchestrator --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Testes concluídos$(NC)"

test-unit: ## Executar apenas testes unitários
	@echo "$(YELLOW)Executando testes unitários...$(NC)"
	$(PYTEST) tests/unit/ -v
	@echo "$(GREEN)✓ Testes unitários concluídos$(NC)"

test-integration: ## Executar apenas testes de integração
	@echo "$(YELLOW)Executando testes de integração...$(NC)"
	$(PYTEST) tests/integration/ -v
	@echo "$(GREEN)✓ Testes de integração concluídos$(NC)"

run: ## Executar o servidor MCP
	@echo "$(YELLOW)Iniciando servidor MCP...$(NC)"
	$(PYTHON) -m mcp_orchestrator.server

run-dev: ## Executar em modo desenvolvimento
	@echo "$(YELLOW)Iniciando servidor MCP em modo desenvolvimento...$(NC)"
	LOG_LEVEL=DEBUG $(PYTHON) -m mcp_orchestrator.server

clean: ## Limpar arquivos temporários
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
	@echo "$(GREEN)✓ Limpeza concluída$(NC)"

format: ## Formatar código
	@echo "$(YELLOW)Formatando código...$(NC)"
	$(BLACK) src/ tests/
	$(ISORT) src/ tests/
	@echo "$(GREEN)✓ Código formatado$(NC)"

lint: ## Verificar código
	@echo "$(YELLOW)Verificando código...$(NC)"
	$(FLAKE8) src/ tests/
	$(MYPY) src/
	@echo "$(GREEN)✓ Verificação concluída$(NC)"

lint-fix: ## Corrigir problemas de linting automaticamente
	@echo "$(YELLOW)Corrigindo problemas de linting...$(NC)"
	$(BLACK) src/ tests/ --check || $(BLACK) src/ tests/
	$(ISORT) src/ tests/ --check-only || $(ISORT) src/ tests/
	@echo "$(GREEN)✓ Correções aplicadas$(NC)"

docker-build: ## Construir imagem Docker
	@echo "$(YELLOW)Construindo imagem Docker...$(NC)"
	docker build -t mcp-orchestrator .
	@echo "$(GREEN)✓ Imagem Docker construída$(NC)"

docker-run: ## Executar com Docker Compose
	@echo "$(YELLOW)Executando com Docker Compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Serviços iniciados$(NC)"

docker-stop: ## Parar serviços Docker
	@echo "$(YELLOW)Parando serviços Docker...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Serviços parados$(NC)"

docker-logs: ## Ver logs dos containers
	@echo "$(YELLOW)Mostrando logs dos containers...$(NC)"
	docker-compose logs -f

setup-local-llms: ## Configurar LLMs locais
	@echo "$(YELLOW)Configurando LLMs locais...$(NC)"
	@if command -v ollama >/dev/null 2>&1; then \
		echo "$(BLUE)Instalando modelos Ollama...$(NC)"; \
		ollama pull llama3.1:8b; \
		ollama pull codellama:7b; \
		ollama pull mistral:7b; \
		echo "$(GREEN)✓ Modelos Ollama instalados$(NC)"; \
	else \
		echo "$(RED)✗ Ollama não está instalado$(NC)"; \
		echo "Instale em: https://ollama.ai/"; \
	fi

logs: ## Ver logs da aplicação
	@echo "$(YELLOW)Mostrando logs da aplicação...$(NC)"
	@if [ -f logs/mcp_orchestrator.log ]; then \
		tail -f logs/mcp_orchestrator.log; \
	else \
		echo "$(RED)Arquivo de log não encontrado$(NC)"; \
	fi

logs-error: ## Ver logs de erro
	@echo "$(YELLOW)Mostrando logs de erro...$(NC)"
	@if [ -f logs/errors.log ]; then \
		tail -f logs/errors.log; \
	else \
		echo "$(RED)Arquivo de log de erro não encontrado$(NC)"; \
	fi

health-check: ## Verificar saúde do sistema
	@echo "$(YELLOW)Verificando saúde do sistema...$(NC)"
	@if command -v curl >/dev/null 2>&1; then \
		echo "$(BLUE)Verificando Ollama...$(NC)"; \
		curl -f http://localhost:11434/api/tags >/dev/null 2>&1 && echo "$(GREEN)✓ Ollama OK$(NC)" || echo "$(RED)✗ Ollama não responde$(NC)"; \
		echo "$(BLUE)Verificando LM Studio...$(NC)"; \
		curl -f http://localhost:1234/v1/models >/dev/null 2>&1 && echo "$(GREEN)✓ LM Studio OK$(NC)" || echo "$(RED)✗ LM Studio não responde$(NC)"; \
	else \
		echo "$(RED)curl não está instalado$(NC)"; \
	fi

docs: ## Gerar documentação
	@echo "$(YELLOW)Gerando documentação...$(NC)"
	@if command -v sphinx-build >/dev/null 2>&1; then \
		cd docs && make html; \
		echo "$(GREEN)✓ Documentação gerada$(NC)"; \
	else \
		echo "$(RED)sphinx-build não está instalado$(NC)"; \
		echo "Instale com: pip install sphinx sphinx-rtd-theme"; \
	fi

security-check: ## Verificar segurança do código
	@echo "$(YELLOW)Verificando segurança do código...$(NC)"
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r src/; \
		echo "$(GREEN)✓ Verificação de segurança concluída$(NC)"; \
	else \
		echo "$(RED)bandit não está instalado$(NC)"; \
		echo "Instale com: pip install bandit"; \
	fi

coverage: ## Gerar relatório de cobertura
	@echo "$(YELLOW)Gerando relatório de cobertura...$(NC)"
	$(PYTEST) tests/ --cov=mcp_orchestrator --cov-report=html --cov-report=term --cov-fail-under=80
	@echo "$(GREEN)✓ Relatório de cobertura gerado$(NC)"

benchmark: ## Executar benchmarks
	@echo "$(YELLOW)Executando benchmarks...$(NC)"
	$(PYTHON) -m pytest tests/benchmark/ -v
	@echo "$(GREEN)✓ Benchmarks concluídos$(NC)"

update-deps: ## Atualizar dependências
	@echo "$(YELLOW)Atualizando dependências...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	@echo "$(GREEN)✓ Dependências atualizadas$(NC)"

check-env: ## Verificar variáveis de ambiente
	@echo "$(YELLOW)Verificando variáveis de ambiente...$(NC)"
	@if [ -f .env ]; then \
		echo "$(GREEN)✓ Arquivo .env encontrado$(NC)"; \
		echo "$(BLUE)Variáveis configuradas:$(NC)"; \
		grep -E "^[A-Z_]+=" .env | cut -d'=' -f1 | sort; \
	else \
		echo "$(RED)✗ Arquivo .env não encontrado$(NC)"; \
		echo "Copie .env.example para .env e configure as variáveis"; \
	fi

init-project: ## Inicializar projeto completo
	@echo "$(YELLOW)Inicializando projeto...$(NC)"
	$(MAKE) install-dev
	$(MAKE) setup-local-llms
	$(MAKE) check-env
	$(MAKE) test
	@echo "$(GREEN)✓ Projeto inicializado$(NC)"

deploy: ## Deploy para produção
	@echo "$(YELLOW)Realizando deploy...$(NC)"
	$(MAKE) clean
	$(MAKE) test
	$(MAKE) security-check
	$(MAKE) docker-build
	$(MAKE) docker-run
	@echo "$(GREEN)✓ Deploy concluído$(NC)"

monitor: ## Abrir dashboards de monitoramento
	@echo "$(YELLOW)Abrindo dashboards de monitoramento...$(NC)"
	@echo "$(BLUE)Grafana: http://localhost:3000 (admin/admin)$(NC)"
	@echo "$(BLUE)Prometheus: http://localhost:9090$(NC)"
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:3000; \
		xdg-open http://localhost:9090; \
	elif command -v open >/dev/null 2>&1; then \
		open http://localhost:3000; \
		open http://localhost:9090; \
	fi

# Comandos de desenvolvimento rápido
dev: ## Modo desenvolvimento (format + lint + test + run)
	@echo "$(YELLOW)Modo desenvolvimento...$(NC)"
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test-unit
	$(MAKE) run-dev

quick-test: ## Teste rápido (apenas testes unitários)
	@echo "$(YELLOW)Executando teste rápido...$(NC)"
	$(PYTEST) tests/unit/ -v --tb=short

quick-lint: ## Lint rápido (apenas black e isort)
	@echo "$(YELLOW)Executando lint rápido...$(NC)"
	$(BLACK) src/ --check
	$(ISORT) src/ --check-only

# Comandos de manutenção
backup: ## Fazer backup dos dados
	@echo "$(YELLOW)Fazendo backup dos dados...$(NC)"
	tar -czf backup-$(shell date +%Y%m%d-%H%M%S).tar.gz data/ logs/ config/
	@echo "$(GREEN)✓ Backup criado$(NC)"

restore: ## Restaurar backup (use: make restore BACKUP=arquivo.tar.gz)
	@echo "$(YELLOW)Restaurando backup...$(NC)"
	@if [ -z "$(BACKUP)" ]; then \
		echo "$(RED)Especifique o arquivo de backup: make restore BACKUP=arquivo.tar.gz$(NC)"; \
		exit 1; \
	fi
	tar -xzf $(BACKUP)
	@echo "$(GREEN)✓ Backup restaurado$(NC)"

# Comandos de debug
debug: ## Executar com debug completo
	@echo "$(YELLOW)Executando com debug completo...$(NC)"
	LOG_LEVEL=DEBUG PYTHONPATH=src $(PYTHON) -m pdb -m mcp_orchestrator.server

profile: ## Executar com profiling
	@echo "$(YELLOW)Executando com profiling...$(NC)"
	$(PYTHON) -m cProfile -o profile.stats -m mcp_orchestrator.server

show-profile: ## Mostrar resultados do profiling
	@echo "$(YELLOW)Mostrando resultados do profiling...$(NC)"
	$(PYTHON) -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)" 