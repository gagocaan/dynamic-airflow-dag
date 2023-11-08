FROM apache/airflow:latest
# ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} loguru hydra-core