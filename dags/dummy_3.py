import time

import pendulum
from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param

with DAG(
    "dummy_3",
    start_date=pendulum.datetime(2022, 8, 21, tz="UTC"),
    schedule_interval=None,
    default_args={"depends_on_past": False, "owner": "The User", "retries": 0},
    catchup=False,
    description="Dummy DAG",
    tags=["version:0.1.3"],
    params={"delay": Param(1, type="integer", minimum=0)},
    render_template_as_native_obj=True,
) as dag:

    @task(task_id="sleep", trigger_rule="all_done")
    def my_sleeping_function(delay: int) -> None:
        time.sleep(delay)

    sleeping_task = my_sleeping_function("{{params.delay}}")
