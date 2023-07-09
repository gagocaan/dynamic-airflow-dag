import datetime
import time

import pendulum
from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param

with DAG(
    "dummy_5",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval=None,
    default_args={"depends_on_past": False, "owner": "The User", "retries": 0},
    catchup=False,
    description="Dummy DAG",
    tags=["version:0.2.0"],
    params={
        "delay": Param(1, type="integer", minimum=0),
        "startDate": Param(None, type=["null", "string"], format="date"),
        "message": Param(None, type=["null", "string"]),
    },
    render_template_as_native_obj=True,
) as dag:

    @task(task_id="sleep", trigger_rule="all_done")
    def my_sleeping_function(delay: int, start_date=str, msg=str) -> None:
        if msg:
            print(msg)
        else:
            print("No message!...")
        if start_date:
            print(start_date)
        else:
            print("No date!...")
        time.sleep(delay)

    sleeping_task = my_sleeping_function(
        "{{params.delay}}",
        "{{params.startDate}}",
        "{{params.message}}",
    )
