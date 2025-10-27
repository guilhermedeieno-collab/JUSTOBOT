.PHONY: help install run dev test clean docker-build docker-up docker-down

help:
	@echo "JUSTOBOT - Makefile commands"
	@echo ""
	@echo "  install       - Instalar dependências"
	@echo "  run           - Executar aplicação"
	@echo "  dev           - Executar em modo desenvolvimento"
	@echo "  test          - Executar testes"
	@echo "  lint          - Executar linters"
	@echo "  format        - Formatar código"
	@echo "  clean         - Limpar arquivos temporários"
	@echo "  docker-build  - Build da imagem Docker"
	@echo "  docker-up     - Subir containers"
	@echo "  docker-down   - Parar containers"
	@echo "  docker-logs   - Ver logs dos containers"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest tests/ -v --cov=app --cov-report=html

lint:
	flake8 app/ tests/
	mypy app/

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api

docker-restart:
	docker-compose restart api

docker-clean:
	docker-compose down -v
	docker system prune -f
