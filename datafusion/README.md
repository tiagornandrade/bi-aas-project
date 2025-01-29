## **Como Construir e Fazer o Deploy no Cloud Run**
### **1️⃣ Build da Imagem**
```bash
docker build -t gcr.io/<PROJECT_ID>/datafusion-service .
```

### **2️⃣ Push da Imagem para o Google Container Registry (GCR)**
```bash
docker push gcr.io/<PROJECT_ID>/datafusion-service
```

### **3️⃣ Deploy no Cloud Run**
```bash
gcloud run deploy datafusion-service \
  --image gcr.io/<PROJECT_ID>/datafusion-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory=1Gi \
  --timeout=300
```

---

## **📌 Recursos e Explicação**
✅ **Base Python Slim**: Para reduzir o tamanho da imagem.  
✅ **PyArrow + DataFusion**: Lida com cache e processamento de consultas.  
✅ **Flask API**: Interface para consultas dinâmicas na camada Gold.  
✅ **Gunicorn**: Melhor para produção ao invés de rodar Flask diretamente.  
✅ **Deploy via Cloud Run**: Fácil escalabilidade sem gerenciamento de servidores.  

Se precisar de ajustes ou otimizações, me avise! 🚀