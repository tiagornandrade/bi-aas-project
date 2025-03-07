# export $(xargs <.env)
# export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Definição de variáveis
PYTHON = python3
PIP = pip
VENV_DIR = venv

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
	fastapi dev src/function-api.py

# Rodar testes
.PHONY: test
test:
	@echo "🧪 Executando testes..."
	pytest -vv  --junitxml=test-results-database.xml

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

run-couchdb:
	http://localhost:5984/_utils/

build-image:
	gcloud builds submit --tag gcr.io/yams-lab-nonprod/cyber-gen:latest

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


## docker build -t cyber-gen-test .
## docker run -p 8080:8080 cyber-gen-test

## gcloud builds submit --tag gcr.io/yams-lab-nonprod/cyber-gen:latest

## docker pull gcr.io/yams-lab-nonprod/cyber-gen:latest
## docker run -p 8080:8080 gcr.io/yams-lab-nonprod/cyber-gen:latest

## gcloud firestore databases describe --project=yams-lab-nonprod;


# gcloud run deploy cyber-gen-service-dev \
#     --image gcr.io/yams-lab-nonprod/cyber-gen:latest \
#     --region us-central1 \
#     --service-account=biaas-dev@yams-lab-nonprod.iam.gserviceaccount.com \
#     --allow-unauthenticated
