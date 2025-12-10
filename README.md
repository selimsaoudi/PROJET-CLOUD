# Cloud Project – Sensor Monitoring Pipeline

This project implements the architecture described in class (components **1 → 2 → Kafka → 3 → SQL → 4**) using **Python**, **Docker**, **Kafka** and **PostgreSQL**.

The goal is to **understand how information flows between cloud components**:

1. A generator sends HTTP requests  
2. An API ingests and forwards messages to a message broker (Kafka)  
3. A background service consumes messages and writes them to a SQL database  
4. An admin API reads from the database and exposes the data

---

## 1. Architecture Overview

**Use case:** monitoring temperature sensors.

- **(1) `sensor_gen`**  
  Simulates a physical sensor and periodically sends temperature measurements via HTTP `POST` to the ingestion API.

- **(2) `ingest_api` (FastAPI)**  
  - Exposes `POST /measurements`  
  - Receives JSON payloads from `sensor_gen`  
  - Acts as a **Kafka producer** and publishes each measurement to the topic `temperatures`

- **Kafka + Zookeeper (Confluent images)**  
  - Kafka acts as a **message broker** between ingestion and persistence  
  - Zookeeper is required by Kafka for coordination

- **(3) `measurement_saver`**  
  - Kafka **consumer** on the `temperatures` topic  
  - For each message, inserts a row into the SQL table `measurements` in PostgreSQL

- **PostgreSQL (`cloud_db`)**  
  - Stores all measurements in a relational table

- **(4) `admin_api` (FastAPI)**  
  - Exposes `GET /measurements?limit=N`  
  - Reads from PostgreSQL and returns recent measurements as JSON for an admin / dashboard

The whole system is **dockerized** and orchestrated via **`docker-compose`**.

---

## 2. Technologies

- **Python 3.11**
  - FastAPI (HTTP APIs)
  - `kafka-python` (Kafka producer / consumer)
  - `psycopg2-binary` (PostgreSQL client)
  - `requests` (HTTP client in `sensor_gen`)
- **Docker / Docker Compose**
- **Kafka + Zookeeper** (Confluent images)
- **PostgreSQL 16**

---

## 3. Project Structure

Projet Cloud S3/

docker-compose.yml  
README.md  
  sensor_gen/
    main.py
    requirements.txt
    Dockerfile
  ingest_api/
    main.py
    requirements.txt
    Dockerfile
  measurement_saver/
    main.py
    requirements.txt
    Dockerfile
  admin_api/
    main.py
    requirements.txt

    Dockerfile


