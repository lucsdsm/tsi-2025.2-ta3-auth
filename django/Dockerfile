# Imagem base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y libpq-dev gcc dos2unix

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Copia e prepara o entrypoint (converte CRLF->LF e dá permissão)
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN dos2unix /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

# Expõe a porta do Django
EXPOSE 8000

# Define o entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
