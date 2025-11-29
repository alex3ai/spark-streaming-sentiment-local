import time
import json
import random
from kafka import KafkaProducer
from app.config import settings  # <--- Importando a configuração centralizada


def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print(f"✅ Conectado ao Kafka em {settings.KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        print(f"❌ Erro ao conectar no Kafka: {e}")
        return None


def generate_transaction():
    from faker import Faker  # Usando a lib Faker que instalamos

    fake = Faker()
    return {
        "transaction_id": fake.uuid4(),
        "amount": round(random.uniform(10.0, 5000.0), 2),
        "currency": random.choice(["BRL", "USD", "EUR"]),
        "city": fake.city(),
        "timestamp": int(time.time()),
    }


if __name__ == "__main__":
    producer = create_producer()
    if producer:
        print(f"🚀 Enviando dados para o tópico '{settings.KAFKA_TOPIC_INPUT}'...")
        try:
            while True:
                data = generate_transaction()
                producer.send(settings.KAFKA_TOPIC_INPUT, data)
                print(f"📤 Enviado: {data}")
                time.sleep(1)
        except KeyboardInterrupt:
            producer.close()
