import os


class Config:
    # Kafka
    KAFKA_TOPIC_INPUT = "raw-tweets"
    KAFKA_TOPIC_OUTPUT = "processed-sentiment"

    # Lógica SRE: Detecta ambiente.
    # Se existir o arquivo .dockerenv, estamos no container e usamos o hostname 'kafka'.
    # Caso contrário, estamos no Windows e usamos 'localhost'.
    IS_DOCKER = os.path.exists("/.dockerenv")
    KAFKA_BOOTSTRAP_SERVERS = "kafka:9092" if IS_DOCKER else "localhost:9092"

    # Spark
    SPARK_APP_NAME = "SentimentAnalysisStream"
    # Aponta para o master definido no docker-compose [cite: 4]
    SPARK_MASTER = "spark://spark-master:7077"

    # NLTK Data Path (Garantindo que o Worker ache os dados baixados)
    NLTK_DATA_DIR = "/opt/spark/nltk_data"


settings = Config()
