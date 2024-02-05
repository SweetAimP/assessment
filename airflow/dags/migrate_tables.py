from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta
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

    graded_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_graded_products_tb",
        sql = build_query(
                "graded_products",
                "/opt/airflow/inputs/graded_products.csv"
        )
    )

    grading_fees_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_grading_fees_tb",
        sql = build_query(
                "grading_fees",
                "/opt/airflow/inputs/grading_fees.csv"
        )
    )

    sold_products_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_sold_products_tb",
        sql = build_query(
                "sold_products",
                "/opt/airflow/inputs/sold_products.csv"
        )
    )

    transport_cost_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="transport_cost_tb",
        sql = build_query(
                "transport_cost",
                "/opt/airflow/inputs/transport_cost.csv"
        )
    )

    platform_fees_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="platform_fees_tb",
        sql = build_query(
                "platform_fees",
                "/opt/airflow/inputs/platform_fees.csv"
        )
    )

    wait_for_tasks = ExternalTaskSensor(
        task_id='wait_for_tasks',
        external_dag_id='migrate_data',
        external_task_ids =["graded_products_tb", "grading_fees_tb", "sold_products_tb", "transport_cost_tb", "platform_fees_tb"],  
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

    [graded_products_tb, grading_fees_tb, sold_products_tb, transport_cost_tb, platform_fees_tb] >> wait_for_tasks >> trigger_child_dag