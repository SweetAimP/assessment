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
    description='Dag that creates the base tables',
    schedule_interval=None,
) as dag:

    create_last_update_dim = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_last_update_dim",
        sql = last_update_dim,
    )

    create_graded_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_graded_products_tb",
        sql = graded_products_tb,
    )

    create_grading_fees_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_grading_fees_tb",
        sql = grading_fees_tb,
    )

    create_sold_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_sold_products_tb",
        sql = sold_products_tb,
    )

    create_transport_cost_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_transport_cost_tb",
        sql = transport_cost_tb,
    )

    create_platform_fees_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_platform_fees_tb",
        sql = platform_fees_tb,
    )

    trigger_child_dag = TriggerDagRunOperator(
        task_id='trigger_child_dag',
        trigger_dag_id='migrate_data',
        dag=dag,
    )

    wait_for_tasks = ExternalTaskSensor(
        task_id='wait_for_tasks',
        external_dag_id='create_tables',
        external_task_ids =["create_graded_products_tb", "create_grading_fees_tb", "create_sold_products_tb", "create_transport_cost_tb","create_platform_fees_tb"],  
        check_existence = True,
        mode='poke', 
        timeout=600, 
        retries=0,  
        poke_interval=60,
        dag=dag,
    )

    [create_last_update_dim, create_graded_products_tb, create_grading_fees_tb, create_sold_products_tb, create_transport_cost_tb, create_platform_fees_tb] >> wait_for_tasks >> trigger_child_dag