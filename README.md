# Crypto Market Data Engineering Pipeline

**An Airflow-Orchestrated, PostgreSQL-Backed, Modular Data Platform**

## Project Overview

This project is a production-style data engineering pipeline designed to ingest, process, and persist cryptocurrency market data in two complementary forms:
**1. Market Snapshots** – Point-in-time state of crypto assets
**2. Market Time-Series** – Continuous historical price evolution
The system is orchestrated using Apache Airflow, deployed via Docker, and persists data into multiple PostgreSQL databases using SQLAlchemy ORM.

Unlike simple ETL scripts, this project emphasizes:

- Deterministic orchestration
- Idempotent database design
- Explicit initialization vs runtime mutation

Separation of concerns between orchestration, ingestion, storage, and computation

## High-Level Architecture
+------------------+
|   Airflow DAG    |
| (Scheduler)      |
+--------+---------+
         |
         v
+------------------------+
|  BashOperator Tasks   |
|  (python -m pipeline) |
+-----------+------------+
            |
            v
+-----------------------------+
|        Pipeline Layer       |
|  snapshot | timeseries      |
+------------+----------------+
             |
             v
+-----------------------------+
|     Storage / ORM Layer     |
|  SQLAlchemy Engines         |
|  Schema-bound Models        |
+------------+----------------+
             |
             v
+-----------------------------+
| PostgreSQL Databases        |
| airflow_snapshot            |
| airflow_timeseries          |
+-----------------------------+

## Repository Structure
crypto-pipeline/
│
├── api/
│   ├── __init__.py
│   └── app.py
│
├── dags/
│   └── crypto_market_dag.py        # Airflow orchestration
│
├── data/
│   ├── snapshot/
│       ├── raw
│       └── processed
│   └── timeseries/
│       ├── raw
│       └── processed
│
├── ingestion/
│   ├── __init__.py
│   ├── coingecko_client.py
│   ├── fetch_market_snapshot.py
│   └── fetch_market_timeseries.py
│
├── orchestration/
│   ├── __init__.py
│   ├── scheduler.py
│   └── state_manager.py
│
├── pipeline/
│   ├── __init__.py
│   ├── __main__.py                 # CLI entry point
│   ├── run_market_snapshot.py
│   └── run_market_timeseries.py
│
├── transformations
│   ├── __init__.py
│   ├── aggregates.py
│   └── clean_market_data.py
│
├── storage/
│   ├── base_snapshot.py
│   ├──base_timeseries.py
│   ├── db_snapshot.py              # Snapshot DB engine + sessions
│   ├── db_timeseries.py             # Timeseries DB engine + sessions
│   ├── models_snapshot.py
│   ├── models_timeseries.py
│   ├── processed_writer_snapshot.py
│   ├── processed_writer_timeseries.py
│   ├── raw_writer_snapshot.py
│   └── raw_writer_timeseries.py
│
├── tests
│   └── test_ingestion.py
│
├── db-init/
│   ├── 01_create_databases.sql
│   ├── 02_create_users.sql
│   ├── 03_snapshot_schema.sql
│   └── 04_timeseries_schema.sql
│
├── config/
│   ├── logging.yaml
│   └── settings.py                 # Environment-driven config
│
├── utils/
│   ├── datetime_utils.py
│   ├── json_utils.py
│   ├── logger.py
│   └── validator.py
│
├── docker/
│   └── DockerFile
│
├── docker-compose.yml
└── requirements.txt


Each directory exists for a single responsibility, which is crucial for maintainability and theoretical soundness.

## System Design Philosophy
### 1️. Separation of Concerns (SoC)
|Layer	        |   Responsibility            |
|---------------|-----------------------------|
|Airflow DAG	|   When something runs       |
|Pipeline	    |   What computation happens  |
|Storage	    |   How data is persisted     |
|SQL Init	    |   One-time system invariants|
|Docker	        |   Environment determinism   |

This mirrors operating system design where:
- Scheduler ≠ Process
- Memory manager ≠ CPU
- Kernel ≠ User space

### 2. Data Flow (End-to-End)
**Snapshot Pipeline**
```nginx
API → Python ingestion → ORM session → snapshot tables

**Time-Series Pipeline**
```nginx
API → Transformation → ORM session → append-only timeseries tables
```

**Airflow Execution Order**
```nginx
run_market_snapshot → run_market_timeseries
```

This ensures *temporal correctness*:
Time-series data depends on snapshot availability.

## Orchestration with Apache Airflow
### DAG Definition
```python
run_snapshot >> run_timeseries
```

This models a Directed Acyclic Graph, where:
- Nodes = deterministic computations
- Edges = dependency constraints
- No cycles = no temporal paradoxes
This directly maps to graph theory and topological sorting.

**Scheduling Semantics**
- */30 * * * * → Every 30 minutes
- catchup=False → Real-time system, not batch replay
- LocalExecutor → Process-based parallelism

## Database Architecture
Why Multiple Databases?
|Database	         |  Purpose                    |
|--------------------|-----------------------------|
|airflow	         |  Airflow metadata           |
|airflow_snapshot	 |  State-at-time data         |
|airflow_timeseries	 |  Append-only historical data|

This prevents:
- Schema coupling
- Accidental joins
- Write amplification
This mirrors *CQRS (Command Query Responsibility Segregation)*.

## SQLAlchemy Design Choice
### Why ORM + Explicit Init?
- Tables are created via:

```python
Base.metadata.create_all(bind=engine)
```

- Initialization is explicit, not magical
- Sessions are generator-based for safe commit/rollback

This mirrors transaction theory and ACID guarantees.

## Computer Networking Perspective
### Docker Networking
- *postgres* hostname resolves via Docker DNS
- Airflow communicates over a bridge network
- No hardcoded IPs → location transparency

**This follows distributed systems principles:**
*“Communicate via names, not addresses.”*

## Theory of Computation Mapping
### DAGs as Computational Graphs
Airflow DAG is equivalent to:
- A static computation graph
- Nodes = pure functions
- Edges = data/control dependencies

This aligns with:
- Lambda calculus evaluation order
- Dataflow programming models
- Functional execution graphs

### Idempotency & Determinism
- Re-running a task does not corrupt state
- Inserts are controlled via session boundaries
- Initialization is one-time, not repeated
This is foundational in:
- Distributed systems
- Fault tolerance
- Replayable computation

## One-Time Initialization vs Runtime Logic
|Concern	        |   Location          |
|-------------------|---------------------|
|Database creation	|   db-init/*.sql     |
|Schema creation	|   SQL or ORM        |
|Privileges	        |   SQL only          |
|Data insertion	    |   Pipeline runtime  |

This is critical for correctness and scalability.