import os
import json
import time
from kafka import KafkaConsumer
import psycopg2

# ----- Kafka config -----
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:19092")
TOPIC = os.getenv("KAFKA_TOPIC", "temperatures")

# ----- Postgres config -----
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "monitoring")
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")


def get_consumer():
    """Create Kafka consumer with retries."""
    last_exc = None
    for _ in range(10):
        try:
            print(f"Trying to connect consumer to {KAFKA_BOOTSTRAP} ...")
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                group_id="measurement_saver",
                auto_offset_reset="earliest",
            )
            print("Kafka consumer connected.")
            return consumer
        except Exception as e:
            last_exc = e
            print("Kafka not ready yet (consumer), retrying in 2s...", e)
            time.sleep(2)
    raise last_exc


def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def main():
    consumer = get_consumer()
    conn = get_db_conn()
    conn.autocommit = True
    cur = conn.cursor()

    insert_sql = """
        INSERT INTO measurements (sensor_id, temperature, ts)
        VALUES (%s, %s, %s)
    """

    print("measurement_saver: ready, waiting for messages...")
    for msg in consumer:
        m = msg.value
        cur.execute(insert_sql, (m["sensor_id"], m["temperature"], m["timestamp"]))
        print("Saved measurement:", m)


if __name__ == "__main__":
    main()

##############
################# Consumer Kafka → SQL