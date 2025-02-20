PROJECT_NAME = wal_decoder
PYTHON = python3
PIP = pip
CELERY = celery
DOCKER_COMPOSE = docker-compose
VENV = .venv

SRC_DIR = src
WORKERS_DIR = $(SRC_DIR)/workers
WAL_LISTENER = $(SRC_DIR)/main.py

WORKERS = identity_worker finance_worker insurance_worker credit_worker compliance_worker commerce_worker

VENV_ACTIVATE = . $(VENV)/bin/activate

.PHONY: setup
setup:
	@echo "🚀 Criando ambiente virtual..."
	$(PYTHON) -m venv $(VENV)
	@echo "📦 Instalando dependências..."
	$(VENV)/bin/$(PIP) install --upgrade pip
	$(VENV)/bin/$(PIP) install -r requirements.txt
	@echo "✅ Configuração concluída!"

.PHONY: up
up:
	@echo "🚀 Subindo containers Docker..."
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down:
	@echo "🛑 Parando containers Docker..."
	$(DOCKER_COMPOSE) down

.PHONY: restart
restart:
	@echo "🔄 Reiniciando containers Docker..."
	$(DOCKER_COMPOSE) restart

.PHONY: listen
listen:
	@echo "📡 Iniciando WAL Listener..."
	export PYTHONPATH="${PYTHONPATH}:$(pwd)" && \
	$(PYTHON) $(WAL_LISTENER)

.PHONY: workers
workers:
	@echo "🛠️ Iniciando todos os workers..."
	$(foreach worker, $(WORKERS), \
		$(VENV)/bin/$(CELERY) -A $(WORKERS_DIR).$(worker) worker --loglevel=info -Q $(worker) & \
	)

.PHONY: worker
worker:
	@echo "🔧 Especifique o worker: make worker name=<worker>"
	@echo "Opções disponíveis: $(WORKERS)"

.PHONY: worker_run
worker_run:
	@echo "🚀 Iniciando worker $(name)..."
	$(VENV)/bin/$(CELERY) -A $(WORKERS_DIR).$(name) worker --loglevel=info -Q $(name)

.PHONY: start_workers
start_workers:
	@echo "⚙️ Rodando todos os workers em um único processo..."
	$(VENV)/bin/$(CELERY) -A $(WORKERS_DIR).celery_app worker --loglevel=info --concurrency=6

.PHONY: run
run: up listen workers

.PHONY: logs
logs:
	@echo "📜 Logs do Celery..."
	$(DOCKER_COMPOSE) logs -f celery

.PHONY: test
test:
	@echo "🧪 Rodando testes..."
	$(VENV)/bin/pytest tests/

.PHONY: clean
clean:
	@echo "🧹 Limpando ambiente..."
	rm -rf $(VENV) __pycache__ .mypy_cache .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✅ Limpeza concluída!"

run-migrations:
	python src/utils/migrations.py
