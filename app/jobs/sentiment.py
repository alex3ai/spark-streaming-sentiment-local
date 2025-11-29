import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, pandas_udf
from pyspark.sql.types import FloatType
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# --- CORREÇÃO DE PATH E IMPORTS ---
# Adiciona '/app' ao path para que o Python "enxergue" os arquivos dentro da pasta montada
sys.path.append("/app")

# Como estamos olhando para dentro de /app, importamos direto (sem o prefixo 'app.')
from config import settings  # noqa: E402
from schemas.tweet import TWEET_SCHEMA  # noqa: E402


# --- LÓGICA VETORIZADA (Pandas UDF) ---
@pandas_udf(FloatType())
def analyze_sentiment(text_series: pd.Series) -> pd.Series:
    # Inicializa o analisador APENAS nos workers
    sid = SentimentIntensityAnalyzer()

    def get_score(text):
        try:
            # Retorna o score composto (-1.0 a 1.0)
            return sid.polarity_scores(str(text))["compound"]
        except Exception:
            return 0.0

    # Aplica a função na série inteira do Pandas (eficiência de memória)
    return text_series.apply(get_score)


def main():
    # Inicializa Spark com Arrow habilitado (Crítico para Pandas UDF)
    spark = (
        SparkSession.builder.appName(settings.SPARK_APP_NAME)
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 1. Leitura do Stream Kafka
    df_raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", settings.KAFKA_BOOTSTRAP_SERVERS)
        .option("subscribe", settings.KAFKA_TOPIC_INPUT)
        .option("startingOffsets", "latest")
        .load()
    )

    # 2. Parsing (JSON -> Colunas Tipadas)
    df_parsed = df_raw.select(from_json(col("value").cast("string"), TWEET_SCHEMA).alias("data")).select("data.*")

    # 3. Transformação (IA/ML Application)
    df_processed = df_parsed.withColumn("sentiment_score", analyze_sentiment(col("text")))

    # 4. Preparação para o Kafka (Serialização)
    # O Kafka aceita bytes ou strings. Precisamos converter nosso Struct para JSON String.
    df_kafka_output = df_processed.selectExpr(
        "CAST(id AS STRING) AS key",  # A chave será o ID do tweet
        "to_json(struct(*)) AS value",  # O valor será o JSON completo com o score
    )

    # 5. Output: Escreve de volta no Kafka (Sink)
    query = (
        df_kafka_output.writeStream.outputMode("append")
        .format("kafka")
        .option("kafka.bootstrap.servers", settings.KAFKA_BOOTSTRAP_SERVERS)
        .option("topic", settings.KAFKA_TOPIC_OUTPUT)
        # CRÍTICO: Checkpoint garante tolerância a falhas.
        # Se o container cair, ele volta a ler exatamente de onde parou.
        .option("checkpointLocation", "/data/checkpoints/sentiment_job_v1")
        .start()
    )

    query.awaitTermination()
