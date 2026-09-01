FROM python:3.10-slim

WORKDIR /app

# Copia o requirements.txt específico da API
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]