# Projet Cloud S3

## 1. Objectif

Mettre en place une architecture cloud simple pour comprendre les **flux d’informations entre composants** :

1. Génération de données (simulateur de capteur)
2. API d’ingestion HTTP
3. Message broker (Kafka)
4. Service de persistance (Postgres)
5. API d’administration

---

## 2. Architecture

Flux principal :

`sensor_gen  →  ingest_api (HTTP)  →  Kafka (topic "temperatures")  →  measurement_saver  →  PostgreSQL  →  admin_api`

Composants :

- **sensor_gen** : script Python qui simule un capteur de température et envoie des requêtes `POST` régulières.
- **ingest_api** : API FastAPI qui reçoit les mesures et joue le rôle de **producteur Kafka**.
- **Kafka + Zookeeper** : broker de messages (images Confluent).
- **measurement_saver** : service Python **consumer Kafka**, qui insère les messages dans la base SQL.
- **PostgreSQL** : base de données relationnelle avec la table :

  ```sql
  CREATE TABLE measurements (
      id SERIAL PRIMARY KEY,
      sensor_id VARCHAR(50) NOT NULL,
      temperature NUMERIC(5,2) NOT NULL,
      ts TIMESTAMPTZ NOT NULL
  );
