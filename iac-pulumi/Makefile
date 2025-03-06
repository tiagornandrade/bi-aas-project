PROJECT_NAME = cyber-gen
STACK_NAME = dev

PULUMI_STACK = $(PROJECT_NAME)-$(STACK_NAME)

.PHONY: install
install:
	@echo "📦 Instalando dependências..."
	@pip install -r requirements.txt
	@echo "✅ Dependências instaladas!"

.PHONY: init
init:
	@echo "🔧 Inicializando o Pulumi..."
	@pulumi stack init $(PULUMI_STACK) || echo "Stack já existe"
	@pulumi config set project_id $(PROJECT_ID)
	@pulumi config set region $(REGION)
	@pulumi config set db_name $(DB_NAME)
	@pulumi config set db_user $(DB_USER)
	@pulumi config set db_password $(DB_PASSWORD) --secret
	@echo "✅ Pulumi configurado!"

.PHONY: up
up:
	@echo "🚀 Criando a infraestrutura..."
	@pulumi up
	@echo "✅ Infraestrutura provisionada!"

.PHONY: destroy
destroy:
	@echo "🔥 Removendo a infraestrutura..."
	@pulumi destroy
	@pulumi stack rm || echo "Stack já removido"
	@echo "✅ Infraestrutura destruída!"

.PHONY: refresh
refresh:
	@echo "🔄 Atualizando a infraestrutura..."
	@pulumi refresh
	@echo "✅ Infraestrutura atualizada!"

.PHONY: help
help:
	@echo "📚 Comandos disponíveis:"
	@echo " make install		-> Instala as dependências do projeto"
	@echo " make init			-> Inicializa o Pulumi"
	@echo " make up				-> Cria a infraestrutura"
	@echo " make destroy		-> Remove a infraestrutura"
	@echo " make help			-> Exibe esta mensagem de ajuda"


# psql "host=/cloudsql/yams-lab-nonprod:us-central1:cyber-gen-db dbname=cybergen user=biaas password=SenhaSegura123"

# gcloud sql instances patch cyber-gen-db --authorized-networks=$(curl -4 -s ifconfig.me)/32
