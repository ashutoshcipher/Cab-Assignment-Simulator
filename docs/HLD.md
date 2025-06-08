# Cab Assignment Simulator High Level Design

This document describes a future scalable architecture for the cab assignment service. It complements the low level design and highlights additional components that are currently out of scope for the in-memory prototype.

## Datastore Choices
- **Redis** with the Geo extension to store active driver locations.
- **Postgres** for persisting driver profiles, ride history and other durable data.

## Message Brokers
- **Kafka** topic used for continuous driver location updates.
- **RabbitMQ** queue to publish ride lifecycle events to background workers.

## External Dependencies
- **FastAPI** powers the HTTP API.
- **Pydantic** validates requests and manages configuration.
- Asynchronous worker components (for example Celery or a custom consumer) process messages from Kafka and RabbitMQ.

## Difference from the In-Memory Prototype
The simulator keeps drivers in an in-memory list and handles ride requests synchronously. The [README](../README.md) notes that driver locations should come from a Kafka topic and be stored in Redis-Geo, distance is computed via the Haversine formula, and `max_eta_km` ought to vary per region and time of day. Only the distance provider exists today; the rest of those assumptions are not implemented. A scalable deployment would use Redis and Postgres backed by Kafka and RabbitMQ to process updates asynchronously.
