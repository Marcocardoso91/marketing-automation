# Makefile para Facebook Ads AI Agent

.PHONY: help install test lint format clean docker-build docker-up docker-down

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - Instala dependências"
	@echo "  make test          - Executa todos os testes"
	@echo "  make test-unit     - Executa testes unitários"
	@echo "  make test-integration - Executa testes de integração"
	@echo "  make lint          - Executa linters"
	@echo "  make format        - Formata código"
	@echo "  make clean         - Remove arquivos temporários"
	@echo "  make docker-build  - Build da imagem Docker"
	@echo "  make docker-up     - Inicia containers"
	@echo "  make docker-down   - Para containers"
	@echo "  make run           - Executa aplicação"

install:
	pip install -r requirements.txt
	pip install pytest pytest-cov pytest-asyncio black isort flake8 mypy

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-unit:
	pytest tests/unit -v --cov=src

test-integration:
	pytest tests/integration -v

test-coverage:
	pytest tests/ --cov=src --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	flake8 src tests --max-line-length=100
	mypy src --ignore-missing-imports

format:
	black src tests
	isort src tests

format-check:
	black --check src tests
	isort --check-only src tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec app /bin/bash

run:
	python main.py

run-dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

migrate:
	alembic upgrade head

migrate-rollback:
	alembic downgrade -1

seed:
	python scripts/seed_database.py

security-scan:
	bandit -r src -f screen
	safety check

pre-commit:
	make format
	make lint
	make test-unit
