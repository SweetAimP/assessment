from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
from queries.create_base_tables import base_records_tb, finance_report_tb
from queries.finance_report import base_records,finance_report

args = {
    'owner': 'Diego',
    'email_on_failure': True,
    'email': ['diealejo96@gmail.com'],
    'retry_delay':timedelta(minutes=5),
    'retries' : 2

}

def _export_report():
    query = """
        Select * from finance_report;
    """
    hook = PostgresHook(postgres_conn_id="postgresconn")
    conn = hook.get_conn()
    res = pd.read_sql(query,conn)
    res.to_csv('/opt/airflow/outputs/finance_report.csv')


with DAG(
    dag_id="finance_report",
    default_args=args,
    description='Dag that creates the final report for finance',
    schedule_interval=None,
    start_date=datetime.now()
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

    export_report = PythonOperator(
        task_id="export_report",
        python_callable=_export_report
    )

    [base_records_tb, finance_report_tb] >> populate_base_records_tb >> populate_finance_report_tb >> export_report