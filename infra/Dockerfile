# 1. Base Image
FROM python:3.10-slim-bookworm

# Variáveis de Versão
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 2. Instalação do Java e utilitários
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    curl \
    procps && \
    rm -rf /var/lib/apt/lists/*

# 3. Download e Instalação do Spark
WORKDIR /tmp
RUN curl -O https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# 4. Configuração de Ambiente
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip

# 5. Instalação de Dependências e do Projeto
WORKDIR /app

# Copia o arquivo de configuração de dependências
COPY pyproject.toml .

# --- CORREÇÃO ---
# Precisamos copiar a pasta 'app' ANTES de rodar o pip install,
# pois o pyproject.toml diz que o código fonte está nela.
COPY app ./app

# Instala todas as libs (pandas, nltk, faker...) e o próprio pacote app
RUN pip install --no-cache-dir .

# Comando padrão
CMD ["/bin/bash"]
