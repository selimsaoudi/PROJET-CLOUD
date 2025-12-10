# admin_api/main.py
from fastapi import FastAPI
import psycopg2
import os

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "monitoring")
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

@app.get("/measurements")
def get_measurements(limit: int = 100):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT sensor_id, temperature, ts "
        "FROM measurements ORDER BY ts DESC LIMIT %s",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"sensor_id": r[0], "temperature": float(r[1]), "timestamp": r[2].isoformat()}
        for r in rows
    ]



####################
####################### API admin qui lit la base SQL