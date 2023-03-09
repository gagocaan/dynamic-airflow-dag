import pendulum
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator
from hydra import compose, initialize
from omegaconf import OmegaConf
from airflow.utils.helpers import chain

initialize(config_path="configuration")
dags_cfg = OmegaConf.to_object(compose(config_name="dag"))

with DAG(start_date=pendulum.datetime(2023, 1, 1, tz="UTC"), **dags_cfg) as dag:
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
            ("1", "1"),
            ("2", "1"),
            ("3", "1"),
            ("4", "1"),
            ("5", "1"),
            ("6", "-1"),
            ("7", "1"),
            ("8", "1"),
            ("9", "-1"),
            ("10", "1"),
            ("11", "1"),
            ("12", "1"),
        ]
    ]

    empty_2 = DummyOperator(task_id="empty_2", trigger_rule="none_failed_min_one_success")

    chain(
        [triggers[0], triggers[1]],
        empty_1,
        [
            triggers[2],
            triggers[3],
        ],
        [
            triggers[4],
            triggers[5],
        ],
        [
            triggers[6],
            triggers[7],
        ],
        [
            triggers[8],
            triggers[9],
        ],
        empty_2,
        [triggers[10], triggers[11]],
    )
