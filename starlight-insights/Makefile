.PHONY: venv
venv:
	@echo "🔧 Criando ambiente virtual..."
	@python3 -m venv venv
	@echo "✅ Ambiente virtual criado!"

.PHONY: install
install: venv
	@echo "📦 Instalando dependências..."
	@source venv/bin/activate && pip install --upgrade pip
	@source venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Dependências instaladas!"

.PHONY: run
run:
	@echo "🚀 Iniciando Superset..."
	@docker exec -it superset superset run -p 8088 --host 0.0.0.0 --with-threads

.PHONY: test
test:
	@echo "🧪 Executando testes..."
	@source venv/bin/activate && pytest -vv --junitxml=test-results-database.xml

.PHONY: up
up:
	@echo "⬆️ Iniciando os serviços (Superset, PostgreSQL, Redis, Celery)..."
	@docker-compose -f docker-compose.yml up -d
	@echo "✅ Serviços iniciados!"

.PHONY: down
down:
	@echo "⬇️ Parando os serviços..."
	@docker-compose down
	@echo "✅ Serviços parados!"

.PHONY: restart
restart:
	@echo "🔄 Reiniciando os serviços..."
	@docker-compose restart
	@echo "✅ Serviços reiniciados!"

.PHONY: setup
setup: up
	@echo "⚙️  Configurando Superset..."
	@docker exec -it superset superset db upgrade
	@docker exec -it superset superset init
	@docker exec -it superset superset fab create-admin \
		--username admin \
		--firstname Superset \
		--lastname Admin \
		--email admin@localhost \
		--password admin
	@echo "✅ Superset configurado!"

.PHONY: logs
logs:
	@echo "📜 Exibindo logs do Superset..."
	@docker-compose logs -f superset

.PHONY: clean
clean:
	@echo "🗑️ Removendo arquivos temporários..."
	@rm -rf venv __pycache__ .pytest_cache
	@echo "✅ Limpeza concluída!"

.PHONY: help
help:
	@echo "📖 Comandos disponíveis:"
	@echo "  make venv            -> Criar ambiente virtual"
	@echo "  make install         -> Instalar dependências"
	@echo "  make run             -> Rodar Superset localmente"
	@echo "  make test            -> Executar testes"
	@echo "  make up              -> Subir serviços com Docker Compose"
	@echo "  make down            -> Parar serviços com Docker Compose"
	@echo "  make restart         -> Reiniciar serviços com Docker Compose"
	@echo "  make setup           -> Configurar Superset"
	@echo "  make logs            -> Ver logs do Superset"
	@echo "  make clean           -> Limpar arquivos temporários"
