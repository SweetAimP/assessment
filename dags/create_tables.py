from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from queries.create_base_tables import *

default_args = {
    'owner': 'Diego',
    'start_date': datetime(2024,1,1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'create_tables',
    default_args=default_args,
    description='A simple DAG to load a CSV file into PostgreSQL',
    schedule_interval=None,
) as dag:

    graded_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_graded_products_tb",
        sql = graded_products,
    )

    grading_fees_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_grading_fees_tb",
        sql = grading_fees,
    )

    sold_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_sold_products_tb",
        sql = sold_products,
    )

    transport_cost_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_transport_cost_tb",
        sql = transport_cost,
    )

    trigger_child_dag = TriggerDagRunOperator(
        task_id='trigger_child_dag',
        trigger_dag_id='migrate_data',
        dag=dag,
    )

    wait_for_tasks = ExternalTaskSensor(
        task_id='wait_for_tasks',
        external_dag_id='create_tables',
        external_task_ids =["create_graded_products_tb", "create_grading_fees_tb", "create_sold_products_tb", "create_transport_cost_tb"],  
        check_existence = True,
        mode='poke', 
        timeout=600, 
        retries=0,  
        poke_interval=60,
        dag=dag,
    )

    [graded_products_tb, grading_fees_tb, sold_products_tb, transport_cost_tb] >> wait_for_tasks >> trigger_child_dag