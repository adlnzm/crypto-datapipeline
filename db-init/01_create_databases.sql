SELECT 'CREATE DATABASE airflow_snapshot'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname='airflow_snapshot'
)\gexec

SELECT 'CREATE DATABASE airflow_timeseries'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname='airflow_timseseries'
)\gexec