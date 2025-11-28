# Base image compatível com Spark 3.3+
FROM bitnami/spark:3.3.2

USER root

# Instalação de dependências do SO necessárias para compilação (se houver)
RUN apt-get update && apt-get install -y gcc python3-dev

# Instalação das libs Python críticas para o nosso projeto
# pyarrow e pandas são obrigatórios para Pandas UDF
# kafka-python para scripts auxiliares
# nltk para a análise de sentimento
RUN pip install pandas pyarrow nltk kafka-python

# [SENIOR MOVE] Baixar o modelo NLTK na construção da imagem (Bake-in)
# Isso evita que os workers tentem baixar da internet durante o processamento
RUN python -c "import nltk; nltk.download('vader_lexicon', download_dir='/opt/bitnami/spark/nltk_data')"

# Define variável de ambiente para o NLTK encontrar os dados
ENV NLTK_DATA=/opt/bitnami/spark/nltk_data

USER 1001