# Local Airflow

![Static Badge](https://img.shields.io/badge/apache-airflow?style=flat-square&logo=apache-airflow&label=Airflow)

Environment for testing and development purposes.

## Run

### With Docker Desktop

```bash
docker-compose up
```

### With Colima

```bash
./colima.sh
```

> It is highly recommended to use the script

## UI

Open the interface of Airflow on [http://localhost:8080/](http://localhost:8080/)

* **username:** `airflow`.
* **password:** `airflow`.

> Reference from: <https://www.architecture-performance.fr/ap_blog/dynamic-taskgroup-scalability-in-airflow-2-0/>

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
