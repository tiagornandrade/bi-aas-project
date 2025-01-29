
# BI as a Service (BIaaS) - Business Intelligence as Code

## Visão Geral
Este projeto implementa um **Business Intelligence as Code (BIaaC)** baseado no **Google Cloud Platform (GCP)**, utilizando **Airbyte**, **SQLMesh**, **Apache DataFusion**, **PyArrow** e **Apache Superset** para construir um pipeline escalável de ingestão, transformação e análise de dados.

A solução foi projetada para **PMEs** e **startups**, permitindo ingestão eficiente de dados transacionais, transformação em camadas do modelo **Medalhão** e visualização otimizada via Superset.

## **Arquitetura**

### **Componentes Principais**
1. **Airbyte** → Ingestão de dados de fontes transacionais para o Google Cloud Storage (GCS).
2. **SQLMesh** → Transformação dos dados em camadas **Bronze, Silver e Gold**.
3. **Apache DataFusion + PyArrow** → Criação de cache otimizado para visualização de dados.
4. **Apache Superset** → Visualização dos dados a partir do cache DataFusion.
5. **Terraform** → Infraestrutura como código para provisionamento automático de recursos no GCP.

## **Estrutura do Repositório**
```plaintext
bi-aas-project/
├── airbyte/                   # Ingestão de dados
│   ├── docker-compose.yml      # Configuração local do Airbyte
│   ├── connectors/             # Conectores personalizados
│   └── README.md               # Documentação do Airbyte
├── sqlmesh/                   # Transformação de dados (Medalhão)
│   ├── models/                 # Modelos Bronze, Silver, Gold
│   ├── tests/                  # Testes de transformações
│   ├── configs/                # Configuração do SQLMesh
│   ├── requirements.txt        # Dependências
│   └── README.md               # Documentação do SQLMesh
├── datafusion/                # Cache para visualização
│   ├── app.py                  # Código do cache PyArrow
│   ├── dockerfile              # Configuração para Cloud Run
│   └── README.md               # Documentação do DataFusion
├── superset/                  # Visualização de dados
│   ├── docker-compose.yml      # Configuração local do Superset
│   ├── dashboards/             # Exportações dos dashboards
│   └── README.md               # Documentação do Superset
├── terraform/                 # Infraestrutura no GCP
│   ├── main.tf                 # Configuração principal
│   ├── modules/                # Módulos para cada serviço
│   └── README.md               # Documentação do Terraform
├── docs/                      # Documentação do projeto
│   ├── architecture.md         # Arquitetura
│   ├── mvp.md                  # Documentação do MVP
│   ├── scaling-strategy.md     # Estratégia de escalabilidade
│   └── setup.md                # Passo a passo para setup
├── scripts/                   # Scripts auxiliares
│   ├── deploy.sh               # Deploy de serviços
│   ├── local_test.sh           # Teste local
│   ├── gcs_cleanup.py          # Limpeza de dados antigos no GCS
├── .github/                   # Configuração CI/CD
│   ├── workflows/
│   │   ├── ci-cd.yml           # Workflow CI/CD
│   │   └── terraform-plan.yml  # Workflow Terraform
│   └── ISSUE_TEMPLATE.md       # Template de issues
├── .env.example               # Variáveis de ambiente
├── docker-compose.yml         # Configuração geral para testes locais
├── requirements.txt           # Dependências gerais
├── README.md                  # Este arquivo
└── LICENSE                    # Licença do projeto
```

## **Setup Inicial**
### **1. Clonar o Repositório**
```bash
git clone https://github.com/seu-usuario/bi-aas-project.git
cd bi-aas-project
```

### **2. Configurar o Ambiente**
```bash
cp .env.example .env
```
- Preencher as variáveis de ambiente no arquivo `.env`

### **3. Iniciar o Airbyte** (opcional, apenas para testes locais)
```bash
cd airbyte
docker-compose up -d
```

### **4. Provisionar Infraestrutura no GCP**
```bash
cd terraform
terraform init
terraform apply
```

### **5. Deploy de Serviços no Cloud Run**
```bash
cd scripts
./deploy.sh
```

## **CI/CD**
O projeto usa **GitHub Actions** para:
- **Testes Automáticos** (SQLMesh, PyArrow, Airbyte)
- **Validação do Terraform**
- **Deploy Automático** para o Cloud Run após merge na branch principal

## **Contribuição**
1. Crie um **fork** do projeto.
2. Crie uma **branch** com sua funcionalidade/bugfix:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça **commit** das mudanças:
   ```bash
   git commit -m "Minha feature"
   ```
4. Faça **push** para a branch:
   ```bash
   git push origin minha-feature
   ```
5. Abra um **Pull Request** no GitHub.

## **Licença**
Este projeto é distribuído sob a licença **MIT**.

## **Contato**
Dúvidas ou sugestões? Entre em contato via **[contato@tiagonavarro.me](mailto:contato@tiagonavarro.me)**.
