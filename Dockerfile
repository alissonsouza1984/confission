# Usa imagem base leve com Python
FROM python:3.11-slim  # <-- versão suportada


# Instala libs do sistema que o WeasyPrint precisa
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto local para o container
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Flask usará
EXPOSE 10000

# Define variável de ambiente usada pelo Flask
ENV PORT=10000

# Comando para iniciar o app Flask
CMD ["python", "app.py"]
