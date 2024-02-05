from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
from queries.create_base_tables import base_records_tb, finance_report_tb
from queries.finance_report import base_records,finance_report

args = {
    'owner': 'Diego',
    'email_on_failure': True,
    'email': ['diealejo96@gmail.com'],
    'retry_delay':timedelta(minutes=5),
    'retries' : 2
    
}

with DAG(
    dag_id="finance_report",
    default_args=args,
    schedule_interval=None,
    start_date=datetime(2024,1,1)
) as dag:

    base_records_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="create_base_records_tb",
        sql = base_records_tb,
    )

    finance_report_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="finance_report_tb",
        sql = finance_report_tb,
    )

    populate_base_records_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="populate_base_records_tb",
        sql = base_records
    )

    populate_finance_report_tb = PostgresOperator(
        postgres_conn_id="postgresconn",
        task_id="populate_finance_report_tb",
        sql = finance_report
    )

    [base_records_tb, finance_report_tb] >> populate_base_records_tb >> populate_finance_report_tb