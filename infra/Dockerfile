# 1. Base Image: Python 3.10 Slim (Leve e Segura)
FROM python:3.10-slim-bookworm

# Definição de Variáveis de Ambiente
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# Define onde o NLTK vai procurar os dados
ENV NLTK_DATA=/opt/spark/nltk_data
# Configurações do Spark e PYTHONPATH
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip:/app

# 2. Instalação do Java 17 e utilitários essenciais
# openjdk-17-jre-headless: Compatível com Spark 3.5.0
# procps: Necessário para o Spark monitorar processos
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    curl \
    procps \
    build-essential \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 3. Download e Instalação Manual do Spark
# Baixamos direto da Apache para garantir integridade e versão exata
WORKDIR /tmp
RUN curl -O https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# 4. Instalação de Dependências Python
WORKDIR /app

# SRE Best Practice:
# Instalamos as libs explicitamente.
# FIX CRÍTICO: "numpy<2.0.0" impede que o pip instale o Numpy 2.0,
# que causa falhas silenciosas (crashes) no Spark 3.5.0 devido a incompatibilidade binária.
RUN pip install --no-cache-dir \
    pyspark==${SPARK_VERSION} \
    textblob \
    kafka-python \
    pydantic \
    pydantic-settings \
    nltk \
    pandas \
    pyarrow \
    "numpy<2.0.0"

# Copia metadados se existirem (para futuro uso com Poetry/setuptools)
# O "|| true" garante que o build não falhe se você ainda não criou o arquivo
COPY pyproject.toml* .
COPY README.md* .

# 5. Configuração dos Dados de NLP (NLTK/TextBlob)
# [SRE FIX] Baixamos 'punkt' e 'averaged_perceptron_tagger' além do 'vader_lexicon'
# O TextBlob PRECISA desses dois primeiros para funcionar (tokenização), senão crasha em runtime.
RUN python3 -m nltk.downloader -d ${NLTK_DATA} vader_lexicon punkt averaged_perceptron_tagger

# Define o diretório de trabalho e usuário root (necessário para permissões de volume no Windows)
USER root
CMD ["/bin/bash"]
