from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.bash import BashOperator
from queries.create_base_tables import *
from airflow.datasets import Dataset


default_args = {
    'owner': 'Diego',
    'start_date': datetime.now(),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'create_tables',
    default_args=default_args,
    description='Dag that creates the base tables',
    schedule_interval="@once",
    catchup=True
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


    signal = BashOperator(
        task_id="producer", 
        outlets=[Dataset("s3://dataset/dataset1.csv")],
        bash_command='echo "pepe"'
    )

    [create_last_update_dim, create_graded_products_tb, create_grading_fees_tb, create_sold_products_tb, create_transport_cost_tb, create_platform_fees_tb] >> signal