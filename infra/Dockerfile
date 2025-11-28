# 1. Base Image
FROM python:3.10-slim-bookworm

# Variáveis de Versão (Fácil manutenção)
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 2. Instalação do Java (Dependência do Spark) e utilitários básicos
# Usamos 'headless' para economizar espaço (sem interface gráfica)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    curl \
    procps && \
    rm -rf /var/lib/apt/lists/*

# 3. Download e Instalação do Spark
# Baixamos, extraímos para /opt/spark e removemos o arquivo .tgz para limpar a imagem
WORKDIR /tmp
RUN curl -O https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# 4. Configuração de Ambiente
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip

# 5. Instalação de Dependências Python
# Copiamos apenas os arquivos de requisitos primeiro para aproveitar o cache do Docker
WORKDIR /app
COPY pyproject.toml .

# Instalamos o pyproject.toml (assumindo que você tem um build system ou apenas dependencias listadas)
# Dica de SRE: Se der erro aqui, podemos criar um requirements.txt simples temporário.
RUN pip install --no-cache-dir pyspark==${SPARK_VERSION}

# O comando final é definido pelo docker-compose, mas deixamos um bash por padrão
CMD ["/bin/bash"]
