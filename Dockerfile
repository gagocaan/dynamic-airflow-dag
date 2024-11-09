FROM apache/airflow:latest
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" hydra-core loguru dbt-duckdb