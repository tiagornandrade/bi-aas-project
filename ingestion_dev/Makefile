# export $(xargs <.env)
# export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Definição de variáveis
PYTHON = python3
PIP = pip
VENV_DIR = venv
COUCHDB_URL = http://admin:password@localhost:5984
COUCHDB_DBNAME = etl_jobs
PROJECT_NAME = etl_loader
FUNCTION_NAME = etl_loader
GCP_REGION = us-central1
PORT = 5555

# Inicializar ambiente virtual
.PHONY: venv
venv:
	@echo "🔧 Criando ambiente virtual..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "✅ Ambiente virtual criado!"

# Instalar dependências
.PHONY: install
install: venv
	@echo "📦 Instalando dependências..."
	@$(VENV_DIR)/bin/$(PIP) install --upgrade pip
	@$(VENV_DIR)/bin/$(PIP) install -r requirements.txt
	@echo "✅ Dependências instaladas!"

# Rodar a aplicação localmente
.PHONY: run
run:
	@echo "🚀 Iniciando FastAPI na porta $(PORT)..."
	PYTHONPATH=$(pwd)/src uvicorn src.function-api:app --host 0.0.0.0 --port $(PORT) --reload

# Rodar testes
.PHONY: test
test:
	@echo "🧪 Executando testes..."
	@$(VENV_DIR)/bin/pytest tests/

# Criar e configurar o banco CouchDB
.PHONY: setup-couchdb
setup-couchdb:
	@echo "🛠️ Criando banco CouchDB se não existir..."
	curl -X PUT "$(COUCHDB_URL)/$(COUCHDB_DBNAME)" || echo "✅ Banco já existe!"

# Construir Docker
.PHONY: build
build:
	@echo "🐳 Construindo imagem Docker..."
	@docker build -t $(PROJECT_NAME) .

# Rodar Docker
.PHONY: run-docker
run-docker:
	@echo "🚀 Rodando Docker..."
	@docker run -p $(PORT):$(PORT) $(PROJECT_NAME)

# Subir serviços com Docker Compose
.PHONY: up
up:
	@echo "⬆️ Iniciando os serviços (FastAPI e CouchDB)..."
	@docker-compose up -d
	@echo "✅ Serviços iniciados!"

# Derrubar serviços com Docker Compose
.PHONY: down
down:
	@echo "⬇️ Parando os serviços..."
	@docker-compose down
	@echo "✅ Serviços parados!"

# Reiniciar serviços com Docker Compose
.PHONY: restart
restart:
	@echo "🔄 Reiniciando os serviços..."
	@docker-compose restart
	@echo "✅ Serviços reiniciados!"

# Limpeza
.PHONY: clean
clean:
	@echo "🗑️ Removendo arquivos temporários..."
	@rm -rf $(VENV_DIR) __pycache__ .pytest_cache
	@echo "✅ Limpeza concluída!"

run-migrations:
	python src/utils/migrations.py

run-main:
	python src/main.py

# Ajuda
.PHONY: help
help:
	@echo "📖 Comandos disponíveis:"
	@echo "  make venv            -> Criar ambiente virtual"
	@echo "  make install         -> Instalar dependências"
	@echo "  make run             -> Rodar FastAPI localmente"
	@echo "  make test            -> Executar testes"
	@echo "  make setup-couchdb   -> Criar banco CouchDB"
	@echo "  make build           -> Construir Docker"
	@echo "  make run-docker      -> Rodar aplicação em Docker"
	@echo "  make up              -> Subir serviços (FastAPI + CouchDB) com Docker Compose"
	@echo "  make down            -> Parar serviços com Docker Compose"
	@echo "  make restart         -> Reiniciar serviços com Docker Compose"
	@echo "  make clean           -> Limpar arquivos temporários"