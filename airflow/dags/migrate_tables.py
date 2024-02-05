from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta
from queries.merge_last_update_dim import merge_last_update_dim

args = {
    'owner': 'Diego',
    'email_on_failure': True,
    'email': ['diealejo96@gmail.com'],
    'retry_delay':timedelta(minutes=5),
    'retries' : 2
    
}

def build_query(path,db_table):
    return """COPY {} FROM '{}' delimiter ',' CSV HEADER""".format(path, db_table)

with DAG(
    dag_id="migrate_data",
    default_args=args,
    schedule_interval=None,
    start_date=datetime(2024,1,1)
) as dag:

    migrate_graded_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="migrate_graded_products_tb",
        sql = build_query(
                "graded_products",
                "/opt/airflow/inputs/graded_products.csv"
        )
    )

    migrate_grading_fees_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="migrate_grading_fees_tb",
        sql = build_query(
                "grading_fees",
                "/opt/airflow/inputs/grading_fees.csv"
        )
    )

    migrate_sold_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="migrate_sold_products_tb",
        sql = build_query(
                "sold_products",
                "/opt/airflow/inputs/sold_products.csv"
        )
    )

    migrate_transport_cost_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="migrate_transport_cost_tb",
        sql = build_query(
                "transport_cost",
                "/opt/airflow/inputs/transport_cost.csv"
        )
    )

    migrate_platform_fees_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="migrate_platform_fees_tb",
        sql = build_query(
                "platform_fees",
                "/opt/airflow/inputs/platform_fees.csv"
        )
    )

    merge_last_update = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="merge_last_update",
        sql = merge_last_update_dim
    )

    wait_for_tasks = ExternalTaskSensor(
        task_id='wait_for_tasks',
        external_dag_id='migrate_data',
        external_task_id="merge_last_update",  
        check_existence = True,
        mode='poke', 
        timeout=600, 
        retries=0,  
        poke_interval=60,
        dag=dag,
    )

    trigger_child_dag = TriggerDagRunOperator(
        task_id='trigger_child_dag',
        trigger_dag_id='finance_report',
        dag=dag,
    )

    [migrate_graded_products_tb, migrate_grading_fees_tb, migrate_sold_products_tb, migrate_transport_cost_tb, migrate_platform_fees_tb] >> merge_last_update >> wait_for_tasks >> trigger_child_dag