import json
import os
import pathlib

import pendulum
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from hydra import compose, initialize
from omegaconf import OmegaConf

initialize(config_path="configuration")
dags_cfg = OmegaConf.to_object(compose(config_name="dag"))

with open(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "configuration", "groups.json"),
    mode="r",
    encoding="utf-8",
) as config_file:
    groups_config: dict = json.loads(config_file.read())

with open(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "configuration", "subgroups.json"),
    mode="r",
    encoding="utf-8",
) as config_file:
    subgroups_config: dict = json.loads(config_file.read())

with open(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "configuration", "tasks.json"),
    mode="r",
    encoding="utf-8",
) as config_file:
    tasks_config: dict = json.loads(config_file.read())

with open(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "configuration", "links.json"),
    mode="r",
    encoding="utf-8",
) as config_file:
    links_config: dict = json.loads(config_file.read())

with DAG(
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    # params=config,
    # render_template_as_native_obj=True,
    **dags_cfg,
) as dag:
    ## Creating groups
    keys = list(groups_config.keys())
    values = list(groups_config.values())
    groups = {i: TaskGroup(group_id=values[keys.index(i)]["group_id"], dag=dag) for i in keys}
    ## Creating sub groups
    keys = list(subgroups_config.keys())
    values = list(subgroups_config.values())
    for j in keys:
        groups[j] = TaskGroup(
            group_id=values[keys.index(j)]["group_id"],
            parent_group=groups[values[keys.index(j)]["parent"]],
            dag=dag,
        )

    ## Creating Tasks
    keys = list(tasks_config.keys())
    values = list(tasks_config.values())
    tasks = {
        k: TriggerDagRunOperator(
            task_id=f'trigger_{values[keys.index(k)]["task_id"]}',
            task_group=groups[values[keys.index(k)]["parent"]],
            dag=dag,
            trigger_dag_id=values[keys.index(k)]["task_id"],
            wait_for_completion=True,
            execution_date="{{ ds }}",
            reset_dag_run=True,
            poke_interval=10,
            conf={"delay": 1},
        )
        for k in keys
    }
    ## Creating Dependencies
    task_keys = list(tasks.keys())
    task_values = list(tasks.values())
    task_group_keys = list(groups.keys())
    task_group_values = list(groups.values())
    keys = list(links_config.keys())
    values = list(links_config.values())
    for l in keys:
        if values[keys.index(l)]["type"] == "task":
            (
                task_values[task_keys.index(values[keys.index(l)]["parent"])]
                >> task_values[task_keys.index(l)]
            )
        elif values[keys.index(l)]["type"] == "group":
            (
                task_group_values[task_group_keys.index(values[keys.index(l)]["parent"])]
                >> task_group_values[task_group_keys.index(l)]
            )
