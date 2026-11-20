## Airflow Orchestration with Docker

### Overview

The BrewBeats data pipeline uses Apache Airflow to orchestrate dbt transformations and validate sales data stored in Snowflake.

Airflow runs in a Docker container using WSL2 Ubuntu on Windows 11. The dbt project is maintained separately on Windows and mounted into the container.

**Pipeline execution:**

```text
Snowflake Bronze (RAW_COFFEE_SALES)
              |
              v
Airflow Task 1: run_dbt_project
              |
              v
dbt build
   |-- Silver: STG_COFFEE_SALES
   |-- Gold: FCT_DAILY_REVENUE
   |-- dbt data quality tests
              |
              v
Airflow Task 2: check_todays_sales
              |
              v
Validate current-day records in Snowflake
```

### Technology Stack

| Component | Version / Configuration |
|---|---|
| Apache Airflow | 3.3.2 |
| Python (Docker) | 3.13 |
| dbt Core | 1.11.16 |
| dbt Snowflake adapter | 1.11.1 |
| dbt DuckDB adapter | 1.11.1 |
| Snowflake | Cloud data warehouse |
| Docker | Docker Desktop with WSL2 |

### Dockerfile Configuration

The existing Airflow image was extended to include the dbt Snowflake adapter.

```dockerfile
FROM apache/airflow:3.3.2-python3.13

USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow==3.3.2" \
    "dbt-core==1.11.16" \
    "dbt-duckdb==1.11.1" \
    "dbt-snowflake==1.11.1" \
    pandas \
    sqlalchemy \
    pymysql \
    && pip check
```

This example reflects the shared development image. Some dependencies are used by other Airflow exercises.

### Docker Compose Configuration

The following is a minimal reference configuration for BrewBeats, not a complete replacement for the existing Airflow environment.

```yaml
services:
  sleek-airflow:
    build:
      context: .
      dockerfile: Dockerfile.airflow-dbt

    image: my-airflow:dbt

    volumes:
      - ./airflow:/opt/airflow

      # Mount the local BrewBeats dbt project
      - /mnt/d/IronHack_DE/Week7_Day3-5_MiniProject/brewbeats_dbt:/opt/airflow/brewbeats_dbt

      # Mount dbt credentials configuration (read-only)
      - /mnt/c/Users/<windows-user>/.dbt:/opt/airflow/.dbt:ro

    ports:
      - "8080:8080"

    environment:
      DBT_PROFILES_DIR: /opt/airflow/.dbt
      SNOWFLAKE_PASSWORD: "${SNOWFLAKE_PASSWORD:?SNOWFLAKE_PASSWORD is required}"

    command: airflow standalone
```

The paths shown are specific to the development environment and must be adapted on another machine.

### Snowflake Authentication

Snowflake authentication is configured through dbt's `profiles.yml`.

The Snowflake password is accessed through the environment variable:

```yaml
password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
```

For local development, the password can be supplied interactively in WSL:

```bash
read -rsp "Snowflake password: " SNOWFLAKE_PASSWORD
echo
export SNOWFLAKE_PASSWORD
```

Passwords, private keys, `.env` files and other credentials must not be committed to Git.

### Running the Pipeline

Build and start the Docker container:

```bash
docker compose up -d --build
```

Verify dbt's Snowflake connection:

```bash
docker compose exec sleek-airflow dbt debug \
  --project-dir /opt/airflow/brewbeats_dbt \
  --profiles-dir /opt/airflow/.dbt
```

Confirm that Airflow has discovered the DAG:

```bash
docker compose exec sleek-airflow airflow dags list
```

Trigger the BrewBeats DAG:

```bash
docker compose exec sleek-airflow airflow dags trigger brewbeats_daily_pipeline
```

The Airflow UI is accessible at `http://localhost:8080`.

### DAG Tasks

| Task | Description |
|---|---|
| `run_dbt_project` | Executes `dbt build`, creating the Silver and Gold models and running dbt tests |
| `check_todays_sales` | Queries the Gold mart for records matching the current date and fails if none exist |

The DAG is scheduled to run daily at 07:00 Europe/Berlin time.

### Execution Results

The Airflow-to-dbt-to-Snowflake integration was successfully tested.

- Both dbt models were created successfully.
- All five dbt data-quality tests passed.
- The Snowflake connection from the Airflow task succeeded.
- The current-day data validation correctly detected missing records.

**Dataset coverage:** March 1, 2024 – March 23, 2025, covering 381 distinct sales dates.

The freshness validation failed for November 20, 2026 because the historical dataset contains no transactions for that date.

This is an expected data-quality finding rather than an orchestration or connectivity failure.

### Limitations

The current DAG rebuilds dbt models from existing Snowflake Bronze data. It does not ingest new daily transactions.

For a production implementation, the workflow could be extended with an ingestion task before dbt execution, automated credentials management, and freshness checks based on the expected reporting date.
