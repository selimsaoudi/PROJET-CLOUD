# sensor_gen/main.py
import os
import time
import random
import requests
from datetime import datetime, timezone

INGEST_URL = os.getenv("INGEST_URL", "http://localhost:8000/measurements")

def generate_measurement(sensor_id: str):
    return {
        "sensor_id": sensor_id,
        "temperature": round(random.uniform(20.0, 40.0), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    sensor_id = "sensor-1"
    while True:
        payload = generate_measurement(sensor_id)
        try:
            r = requests.post(INGEST_URL, json=payload, timeout=2)
            print("Sent:", payload, "status:", r.status_code)
        except Exception as e:
            print("Error sending data:", e)
        time.sleep(5)


################
################ Générateur de mesures