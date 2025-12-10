# ingest_api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import os
import time

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:19092")
TOPIC = os.getenv("KAFKA_TOPIC", "temperatures")

app = FastAPI()


class Measurement(BaseModel):
    sensor_id: str
    temperature: float
    timestamp: str


def get_producer():
    """Create a Kafka producer with a few retries."""
    last_exc = None
    for _ in range(5):
        try:
            print(f"Trying to connect producer to {KAFKA_BOOTSTRAP} ...")
            p = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            print("Producer connected.")
            return p
        except Exception as e:
            last_exc = e
            print("Kafka not ready yet (producer), retrying in 2s...", e)
            time.sleep(2)
    raise last_exc


@app.post("/measurements")
def receive_measurement(m: Measurement):
    producer = get_producer()
    producer.send(TOPIC, m.dict())
    producer.flush()
    return {"status": "ok"}

#################
##################  API HTTP + producer Kafka