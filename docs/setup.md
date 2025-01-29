# **Setup Inicial do Projeto BI as Code**
Este documento descreve como configurar o ambiente do projeto do zero.

## **1. Pré-requisitos**
- **Google Cloud Platform (GCP)**
  - Criar um projeto no GCP.
  - Ativar **Cloud Storage, Cloud Run e Cloud SQL**.
- **Ferramentas Locais**
  - Docker e Docker Compose.
  - Terraform instalado.

---

## **2. Configuração no GCP**
### 🔹 Criar Buckets no GCS
```bash
gsutil mb -p <PROJECT_ID> -c STANDARD -l US gs://bi-aas-project-bronze/
gsutil mb -p <PROJECT_ID> -c STANDARD -l US gs://bi-aas-project-silver/
gsutil mb -p <PROJECT_ID> -c STANDARD -l US gs://bi-aas-project-gold/
```

### 🔹 Criar Cloud SQL para o Airflow
```bash
gcloud sql instances create airflow-db --tier=db-f1-micro
gcloud sql users set-password postgres --instance=airflow-db --password=<PASSWORD>
```

---

## **3. Deploy dos Serviços**
### 🔹 Deploy via Terraform
```bash
cd terraform
terraform init
terraform apply -auto-approve
```

### 🔹 Rodando Airbyte no Cloud Run
```bash
gcloud run deploy airbyte-service --image=airbyte/airbyte --platform=managed --region=us-central1
```

### 🔹 Rodando SQLMesh no Cloud Run
```bash
gcloud run deploy sqlmesh-service --image=custom-sqlmesh-image --platform=managed --region=us-central1
```

---

## **4. Configuração do Apache Superset**
1. Acesse `http://localhost:8088`
2. Configure a conexão com o Apache DataFusion:
   - **Database URI**: `datafusion+pyarrow://`
   - **Tipo de Conexão**: SQLite (configurado para PyArrow)
3. Carregue os dashboards padrão.
