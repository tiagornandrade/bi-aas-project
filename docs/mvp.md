# MVP - Business Intelligence as Code

## **Objetivo do MVP**
O MVP (Minimum Viable Product) tem como objetivo validar a ingestão, transformação e visualização de dados para pequenas e médias empresas usando uma solução **Business Intelligence as Code (BIaaC)** baseada no Google Cloud Platform (GCP).

## **Componentes do MVP**

### **1. Ingestão de Dados (Airbyte)**
- Configuração de conectores para capturar dados transacionais.
- Salvamento dos dados na camada **Bronze** no Google Cloud Storage (GCS) em formato Parquet.

### **2. Transformação de Dados (SQLMesh)**
- Aplicação de transformações nas camadas **Bronze → Silver → Gold**.
- Geração de dados otimizados para análise.

### **3. Motor de Consulta e Cache (Apache DataFusion + PyArrow)**
- Configuração do **Apache DataFusion** para leitura eficiente dos dados no GCS.
- Uso de **PyArrow** para criar um cache da camada **Gold**.

### **4. Visualização (Apache Superset)**
- Conexão do Superset ao cache do **DataFusion**.
- Criação de dashboards interativos com métricas básicas.

## **Infraestrutura do MVP**
- **Cloud Run**: Deploy dos serviços do pipeline.
- **Google Cloud Storage (GCS)**: Armazenamento centralizado dos dados.
- **Terraform**: Automação da infraestrutura na nuvem.

## **Fluxo de Dados no MVP**
1. **Airbyte** coleta dados e armazena na camada **Bronze** no GCS.
2. **SQLMesh** processa os dados e gera camadas **Silver e Gold**.
3. **Apache DataFusion** consulta os dados e PyArrow aplica cache.
4. **Apache Superset** exibe dashboards baseados nos dados processados.

## **Critérios de Sucesso**
✅ Dados ingeridos corretamente via Airbyte e armazenados no GCS.
✅ SQLMesh processa as camadas **Bronze → Silver → Gold** sem erros.
✅ Apache DataFusion e PyArrow fornecem respostas rápidas para consultas.
✅ Dashboards básicos no Superset exibindo métricas corretas.

## **Próximos Passos**
- Refinamento das transformações no SQLMesh.
- Implementação de testes automatizados para validação de dados.
- Otimização da performance de consultas no Apache DataFusion.
