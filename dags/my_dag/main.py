import pendulum
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from hydra import compose, initialize
from omegaconf import OmegaConf

initialize(config_path="configuration")
dags_cfg = OmegaConf.to_object(compose(config_name="dag"))

with DAG(start_date=pendulum.datetime(2022, 8, 21, tz="UTC"), **dags_cfg) as dag:

    empty_1 = EmptyOperator(task_id="empty_1")

    triggers = [
        TriggerDagRunOperator(task_id=f"trigger_{_}", trigger_dag_id=f"dummy_{_}")
        for _ in range(1, 5)
    ]

    empty_2 = EmptyOperator(task_id="empty_2")

    empty_1 >> triggers >> empty_2
