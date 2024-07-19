FROM apache/airflow:2.9.3
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" hydra-core loguru