import pendulum
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator
from hydra import compose, initialize
from omegaconf import OmegaConf

initialize(config_path="configuration")
dags_cfg = OmegaConf.to_object(compose(config_name="dag"))

with DAG(start_date=pendulum.datetime(2022, 8, 21, tz="UTC"), **dags_cfg) as dag:

    empty_1 = DummyOperator(task_id="empty_1")

    triggers = [
        TriggerDagRunOperator(
            task_id=f"trigger_{_[0]}",
            trigger_dag_id=f"dummy_{_[0]}",
            wait_for_completion=True,
            execution_date="{{ds}}",
            reset_dag_run=True,
            poke_interval=10,
            conf={"delay": _[1]},
        )
        for _ in [
            ("1", 1),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5),
            ("6", 6),
            ("7", 7),
            ("8", 8),
            ("9", 9),
            ("10", -1),
            ("11",11),
            ("12",12)
        ]
    ]

    empty_2 = DummyOperator(task_id="empty_2", trigger_rule="all_done")

    empty_1 >> triggers >> empty_2
