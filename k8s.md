# Kubernetes

```sh
docker-buildx build --pull --tag "registry.cg-homeserver.duckdns.org/airflow:local1" . -f - <<EOF
FROM apache/airflow:2.8.3

RUN pip install apache-airflow==2.8.3 hydra-core loguru

USER root

COPY --chown=airflow:root ./dags/ \${AIRFLOW_HOME}/dags/

USER airflow

EOF
```
