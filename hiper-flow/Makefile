# Subir serviços com Docker Compose
.PHONY: up
up:
	@echo "⬆️ Iniciando os serviços..."
	@docker compose up -d
	@echo "✅ Serviços iniciados!"

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
