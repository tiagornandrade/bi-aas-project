FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY credential/service-account.json /app/service-account.json

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account.json"

COPY . .

EXPOSE 8080

CMD ["uvicorn", "src.function_api:app", "--host", "0.0.0.0", "--port", "8080"]
