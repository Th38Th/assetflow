import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from core import send_welcome_email

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "user.signup"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    await consumer.start()
    logging.info(f"Consumer started. Listening on topic: {TOPIC_NAME}")
    try:
        async for msg in consumer:
            try:
                data = msg.value
                username = data.get("username")
                email = data.get("email")
                logging.info(f"Sending email to [{email}]...")
                send_welcome_email(email, username)
            except Exception as e:
                logging.exception(f"Error processing data: {e}")
    finally:
        await consumer.stop()
        logging.info("Consumer stopped.")


if __name__ == "__main__":
    asyncio.run(consume())
