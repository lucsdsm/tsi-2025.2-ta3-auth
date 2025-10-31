# Imagem base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Dá permissão de execução ao entrypoint
RUN chmod +x /app/entrypoint.sh

# Expõe a porta do Django
EXPOSE 8000

# Define o entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
