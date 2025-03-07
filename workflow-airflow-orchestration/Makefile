.PHONY: external-network
external-network:
	@echo "🔄 Criando rede 'external-network'..."
	@docker network create etl_network
	@echo "✅ Rede 'external-network' criada com sucesso!"


# Subir serviços com Docker Compose
.PHONY: up
up:
	@echo "⬆️ Iniciando os serviços..."
	@docker compose up -d
	@echo "✅ Serviços iniciados!"


,PHONY: airflow-init
airflow-init:
	@echo "🔗 Criando conexão 'api-etl' no Airflow..."
	@docker compose exec airflow-webserver airflow connections add 'api-etl' \
		--conn-type 'http' \
		--conn-host 'http://127.0.0.1:8000/'
	@echo "✅ Conexão 'api-etl' criada com sucesso!"

# Derrubar serviços com Docker Compose
.PHONY: down
down:
	@echo "⬇️ Parando os serviços..."
	@docker compose down
	@echo "✅ Serviços parados!"

# Reiniciar serviços com Docker Compose
.PHONY: restart
restart:
	@echo "🔄 Reiniciando os serviços..."
	@docker compose restart
	@echo "✅ Serviços reiniciados!"

.PHONY: generate-yaml
generate-yaml:
	@echo "🔄 Gerando arquivo docker-compose.yml..."
	@python3 plugins/generate_yaml.py
	@echo "✅ Arquivo docker-compose.yml gerado!"
