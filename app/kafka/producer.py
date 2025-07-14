from aiokafka import AIOKafkaProducer
import asyncio
import json

producer = None

async def start_kafka():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()

async def stop_kafka():
    await producer.stop()

async def send_event(topic: str, data: dict):
    await producer.send_and_wait(topic, data)