DO
$$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname='snapshot_user' 
    ) THEN
        CREATE USER snapshot_user WITH PASSWORD 'snapshot_pass';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname='timeseries_user'
    ) THEN
        CREATE USER timeseries_user WITH PASSWORD 'timeseries_pass';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE airflow_snapshot TO airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow_timeseries TO airflow;