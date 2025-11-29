import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, pandas_udf
from pyspark.sql.types import FloatType
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# Hack para garantir que o python encontre o módulo 'app' dentro do Spark Submit
sys.path.append("/app")

# Adicionamos 'noqa: E402' para o linter ignorar que o import não está no topo
from app.config import settings  # noqa: E402
from app.schemas.tweet import TWEET_SCHEMA  # noqa: E402


# --- LÓGICA VETORIZADA (Pandas UDF) ---
@pandas_udf(FloatType())
def analyze_sentiment(text_series: pd.Series) -> pd.Series:
    # Inicializa o analisador APENAS nos workers
    sid = SentimentIntensityAnalyzer()

    def get_score(text):
        try:
            # Retorna o score composto (-1.0 a 1.0)
            return sid.polarity_scores(str(text))["compound"]
        except Exception:  # Correção E722: Exception específica
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

    # 4. Output (Console para Debug Local)
    query = (
        df_processed.writeStream.outputMode("append")
        .format("console")
        .option("truncate", "false")
        .trigger(processingTime="1 seconds")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
