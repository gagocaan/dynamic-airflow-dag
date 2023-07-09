"""# This is a example of Dynamic DAG"""
import json
import os
import pathlib

import pendulum
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from hydra import compose, initialize
from omegaconf import OmegaConf

initialize(config_path="configuration")
dags_cfg = OmegaConf.to_object(compose(config_name="dag"))

with open(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "configuration", "conf.json"),
    mode="r",
    encoding="utf-8",
) as config_file:
    config: dict = json.loads(config_file.read())

with DAG(
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    params=config,
    render_template_as_native_obj=True,
    **dags_cfg,
) as dag:
    ## Creating groups
    group_list = list({values["group_id"] for _, values in config["flow"].items()})
    groups = {group: TaskGroup(group_id=group, dag=dag) for group in group_list}

    tasks = {
        key: TriggerDagRunOperator(
            task_id=f"trigger_{key}",
            task_group=groups[values["group_id"]],
            dag=dag,
            trigger_dag_id=key,
            wait_for_completion=True,
            execution_date="{{ execution_date }}",
            reset_dag_run=True,
            poke_interval=10,
            conf=f"{{{{ params.general_parameters if params.general_parameters.delay else params.flow.{key}.params }}}}",
            **values["kwargs"],
        )
        for key, values in config["flow"].items()
    }

    for key, values in config["flow"].items():
        if values["parents"]:
            for id in values["parents"]["ids"]:
                if values["parents"]["type"] == "task":
                    tasks[id] >> tasks[key]
                elif values["parents"]["type"] == "group":
                    groups[id] >> tasks[key]
        else:
            tasks[key]
