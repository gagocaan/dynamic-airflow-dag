import time

import pendulum
from airflow import DAG
from airflow.decorators import task

with DAG(
    "dummy_5",
    start_date=pendulum.datetime(2022, 8, 21, tz="UTC"),
    schedule_interval=None,
    default_args={"depends_on_past": False, "owner": "Carlos Garzon", "retries": 1},
    catchup=False,
    description="Dummy DAG",
    tags=["version:0.1.0"],
) as dag:

    @task(task_id="sleep")
    def my_sleeping_function(delay: int) -> None:
        time.sleep(delay)

    sleeping_task = my_sleeping_function(10)
