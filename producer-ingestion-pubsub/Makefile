.PHONY: build_image
build_image:
	@echo "🐳 Construindo imagem Docker..."
	@gcloud builds submit --tag gcr.io/yams-lab-nonprod/producer-ingestion-pubsub:latest

.PHONY: build_local
build_local:
	@echo "🐳 Construindo imagem Docker..."
	@docker build -t producer-ingestion-pubsub .

.PHONY: run_local
run_local:
	@echo "🚀 Rodando Docker..."
	@docker run -p 8080:8080 producer-ingestion-pubsub

.PHONY: deploy_all
deploy_all:
	@echo "🚀 Fazendo deploy das imagens para o Google Artifact Registry..."
	@gcloud run deploy producer --image gcr.io/yams-lab-nonprod/consumer:latest --platform managed --region us-central1 --allow-unauthenticated
	@gcloud run deploy consumer --image gcr.io/yams-lab-nonprod/producer:latest --platform managed --region us-central1 --allow-unauthenticated

.PHONY: help
help:
	@echo "📖 Comandos disponíveis:"
	@echo "  make build_all       -> Construir todas as imagens Docker"
	@echo "  make deploy_all      -> Fazer deploy de todas as imagens no Google Cloud Run"
	@echo "  make build_image     -> Construir imagem Docker"
	@echo "  make build_local     -> Construir imagem Docker localmente"
	@echo "  make run_local       -> Rodar Docker localmente"
	@echo "  make help            -> Exibir ajuda"
