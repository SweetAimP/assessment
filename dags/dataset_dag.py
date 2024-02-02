import datetime
import os

from airflow import DAG
from airflow.operators.bash import BashOperator

DATASET_NAME = "darl_dataset_test"
TABLE_NAME = "darl_test_table"
DAG_ID = "BigQueryWorkflow"

with DAG(
    dag_id=DAG_ID,
    schedule_interval="@once",
    start_date=datetime.datetime(2023,10,23),
    catchup=False,
    tags=["BigQuery"],
) as dag:
    # Define default_args and other DAG configurations here

    output_file_path = '/opt/airflow/outputs/output_file.txt'

    # BashOperator that runs a command and redirects its output to a file
    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo "pepe" > {}'.format(output_file_path),
        dag=dag,
    )
