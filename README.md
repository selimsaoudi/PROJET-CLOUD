### 1. Contexte du projet

Dans le cadre du cours *Cloud & Data Engineering*, l’objectif du projet est de mettre en pratique les notions vues en cours : architecture client–serveur, pattern producer–consumer via un message broker, persistance des données, virtualisation et portabilité avec Docker et Docker-Compose.

On nous demande d’implémenter une petite architecture cloud composée de plusieurs services qui communiquent entre eux et d’observer les **flux d’informations entre composants** (requêtes HTTP, messages Kafka, requêtes SQL).

---

### 2. Architecture mise en place

L’architecture réalisée suit le schéma proposé en cours dans la section “Projects: Implement the following architecture”.

Flux principal :

**sensor_gen → ingest_api (HTTP) → Kafka (topic `temperatures`) → measurement_saver → PostgreSQL → admin_api**

Rôles des composants :

* **sensor_gen**
  Service Python qui simule un capteur de température. Il envoie régulièrement des mesures à l’API d’ingestion via des requêtes HTTP `POST`.
  → Cela illustre le pattern **client–serveur** présenté en cours.

* **ingest_api**
  API REST réalisée avec FastAPI. Elle expose un endpoint `POST /measurements` qui valide les données puis joue le rôle de **producteur Kafka** : chaque mesure reçue est publiée dans le topic `temperatures`.
  → On combine ici API / HTTP / JSON comme dans la partie “Client-Server Pattern”.

* **Kafka (broker) + Zookeeper**
  Kafka sert de **message broker** au centre de l’architecture et implémente le pattern **publisher–subscriber / producer–consumer** vu dans le cours d’architecture.

* **measurement_saver**
  Service Python **consumer Kafka** : il consomme les messages du topic `temperatures` et insère chaque mesure dans la base PostgreSQL via une requête `INSERT`.
  → On ajoute ainsi une couche de **persistance** comme dans la section “Adding a database in our Architecture”.

* **PostgreSQL (base SQL)**
  Base relationnelle contenant une table `measurements(id, sensor_id, temperature, ts)` qui stocke l’historique des mesures.

* **admin_api**
  Deuxième API FastAPI qui interroge la base SQL et expose un endpoint `GET /measurements?limit=N` pour récupérer les N dernières mesures.
  → Cette API représente un **service d’administration / monitoring** du système.

---

### 3. Flux d’informations

1. **Génération** : `sensor_gen` génère périodiquement une mesure sous la forme d’un JSON (`sensor_id`, `temperature`, `timestamp`).
2. **Ingestion HTTP** : la mesure est envoyée en `POST` à `ingest_api` (architecture client–serveur).
3. **Publication dans Kafka** : `ingest_api` sérialise la mesure en JSON et la publie dans le topic `temperatures`.
4. **Consommation et persistance** : `measurement_saver` consomme les messages du topic, puis exécute `INSERT INTO measurements(...)` dans PostgreSQL.
5. **Lecture par l’admin** : `admin_api` exécute un `SELECT` sur la table `measurements` et renvoie le résultat en JSON au client (interface Swagger ou autre).

Ce pipeline permet de séparer les responsabilités : production des données, transport asynchrone via broker, stockage durable, exposition de vues de lecture.

---

### 4. Dockerisation et portabilité

Tous les composants sont **conteneurisés avec Docker**, ce qui s’inscrit dans la partie du cours sur la virtualisation, la containerisation et la portabilité.

* Chaque service (`sensor_gen`, `ingest_api`, `measurement_saver`, `admin_api`) possède son **Dockerfile** basé sur une image Python.
* Kafka, Zookeeper et PostgreSQL utilisent des images existantes.
* Un fichier **`docker-compose.yml`** orchestre l’ensemble :

  * définition des services,
  * configuration du réseau,
  * variables d’environnement (connexion Kafka, paramètres SQL),
  * dépendances entre services.

Grâce à Docker-Compose, l’architecture complète peut être démarrée avec une seule commande :

```bash
docker compose up -d --build
```
