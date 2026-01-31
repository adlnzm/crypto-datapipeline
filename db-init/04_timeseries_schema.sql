\connect airflow_timeseries;

CREATE SCHEMA IF NOT EXISTS timeseries AUTHORIZATION airflow;

GRANT USAGE ON SCHEMA timeseries TO airflow;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA timeseries TO airflow;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA timeseries TO airflow;