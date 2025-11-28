.PHONY: up down logs test clean setup help

# Configuração inicial do ambiente de desenvolvimento
setup:
	@echo "Configurando pre-commit..."
	pip install pre-commit
	pre-commit install

# Sobe a infraestrutura (Mínima: Detached & Build)
up:
	docker-compose up -d --build

# Derruba a infraestrutura
down:
	docker-compose down

# Visualiza logs em tempo real
logs:
	docker-compose logs -f

# Executa testes dentro do container (após 'make up')
test:
	docker exec -it spark-master pytest /app/tests

# Limpeza de arquivos temporários do Python
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Ajuda para listar comandos disponíveis
help:
	@echo "Comandos disponíveis:"
	@echo "  make setup   - Instala e configura pre-commit hooks"
	@echo "  make up      - Sobe os containers (build force)"
	@echo "  make down    - Para e remove os containers"
	@echo "  make logs    - Segue os logs dos containers"
	@echo "  make test    - Roda os testes via pytest no container"
	@echo "  make clean   - Limpa caches python (__pycache__)"
