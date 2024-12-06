import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from etl_pipeline import run_etl_script
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='etl_pipeline_dag',
    default_args=default_args,
    description='Run the ETL pipeline',
    schedule='@daily',
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:

    run_etl = PythonOperator(
        task_id='run_etl_pipeline',
        python_callable=run_etl_script,  # ETL Pipeline의 main() 함수
    )

    run_etl
