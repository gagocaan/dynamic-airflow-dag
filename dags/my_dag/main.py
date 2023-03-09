import json
import os
import pathlib

import pendulum
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.helpers import chain
from hydra import compose, initialize
from omegaconf import OmegaConf

initialize(config_path="configuration")
dags_cfg = OmegaConf.to_object(compose(config_name="dag"))

with open(os.path.join(pathlib.Path(__file__).parent.resolve(), "configuration", "conf.json"), mode="r", encoding="utf-8") as config_file:
    config = json.loads(config_file.read())

with DAG(start_date=pendulum.datetime(2023, 1, 1, tz="UTC"), params=config, render_template_as_native_obj=True, **dags_cfg) as dag:
    empty_1 = DummyOperator(task_id="empty_1")

    for key in config:
        trigger = TriggerDagRunOperator(
            task_id=f"trigger_{key}",
            trigger_dag_id=key,
            wait_for_completion=True,
            execution_date="{{ds}}",
            reset_dag_run=True,
            poke_interval=10,
            conf=config[key],
        )

        empty_1 >> trigger
