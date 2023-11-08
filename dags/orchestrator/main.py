"""# This is a example of Dynamic DAG
## Usage
### Skip tasks
```json
{
    "skip_tasks": [
        "Group_1.trigger_dummy_1",
        "Group_2.trigger_dummy_2"
    ],
    ...
}
```
The names contained in this list are skipped at execution.
The task id is defined as `<group.task>`, be careful not to confuse the **task** with the **name** of the flow you want to execute, the task as such has the prefix `trigger_`.
> `skip_tasks` and `only_execute_tasks` are mutually exclusive, you can only define one.
### Only execute tasks
```json
{
    ...
    "only_execute_tasks": [
        "Group_1.trigger_dummy_1",
        "Group_2.trigger_dummy_2"
    ],
    ...
}
```
Only the tasks in this list will be executed, all others will be skipped.
The task id is defined as `<group.task>`, be careful not to confuse the **task** with the **name** of the flow you want to execute, the task as such has the prefix `trigger_`.
> `skip_tasks` and `only_execute_tasks` are mutually exclusive, you can only define one.
### General parameters
```json
{
    "general_parameters": {
        "delay": null,
        "startDate": null,
        "message": null
    },
    ...
}
```
If `delay` is set, the orchestrator will take all general parameters and apply them to all flows. This is especially useful when we want to reprocess two or more pipelines for a specific date range.
"""
import json
import os
import pathlib

import pendulum
from airflow import DAG
from airflow.exceptions import AirflowSkipException, AirflowConfigException
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from hydra import compose, initialize
from omegaconf import OmegaConf

initialize(config_path="configuration", version_base=None)
dags_cfg = OmegaConf.to_object(compose(config_name="dag"))

with open(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "configuration", "conf.json"),
    mode="r",
    encoding="utf-8",
) as config_file:
    config: dict = json.loads(config_file.read())


def skip_if_specified(context):
    """
    Skip the task if specified in the context.

    Args:
        context: The context dictionary containing task and dag_run information.

    Raises:
        AirflowConfigException: If both `skip_tasks` and `only_execute_tasks` are defined.
        AirflowSkipException: If the task is in the `skip_tasks` list or not in the `only_execute_tasks` list.
    """
    task_id = context["task"].task_id
    conf = context["dag_run"].conf or {}
    skip_tasks = conf.get("skip_tasks", [])
    only_execute_tasks = conf.get("only_execute_tasks", [])
    if skip_tasks and only_execute_tasks:
        raise AirflowConfigException(
            "`skip_tasks` and `only_execute_tasks` are mutually exclusive, you can only define one."
        )
    if skip_tasks and task_id in skip_tasks:
        raise AirflowSkipException()
    if only_execute_tasks and task_id not in only_execute_tasks:
        raise AirflowSkipException()


with DAG(
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    params=config,
    render_template_as_native_obj=True,
    doc_md=__doc__,
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
            trigger_run_id="from_orchestrator__{{ logical_date }}",
            wait_for_completion=True,
            execution_date="{{ logical_date }}",
            reset_dag_run=True,
            poke_interval=10,
            conf=f"{{{{ params.general_parameters if params.general_parameters.delay else params.flow.{key}.params }}}}",
            pre_execute=skip_if_specified,
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
