# 1. Base Image
FROM python:3.10-slim-bookworm

ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# Define onde o NLTK vai procurar os dados (Mesmo caminho do config.py)
ENV NLTK_DATA=/opt/spark/nltk_data

# 2. Instalação do Java e utilitários essenciais
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    curl \
    procps \
    build-essential \
    python3-dev && \
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

# 5. Instalação de Dependências e Aplicação
WORKDIR /app

# Copia os arquivos de metadados do projeto
COPY pyproject.toml .
# É boa prática copiar o README se ele for referenciado no toml, mas opcional se não for
COPY README.md .

# [CORREÇÃO CRÍTICA]
# O comando 'pip install .' lê o pyproject.toml, que diz que o código está em 'app'.
# Portanto, a pasta 'app' PRECISA existir antes do pip rodar.
COPY app ./app

# Instala as dependências (pyspark, nltk, etc) E o pacote local 'app'
RUN pip install --no-cache-dir .

# [SENIOR MOVE] Baixamos o léxico do VADER
# Isso deve rodar DEPOIS do pip install, pois requer o módulo 'nltk' instalado
RUN python -m nltk.downloader -d ${NLTK_DATA} vader_lexicon

CMD ["/bin/bash"]
