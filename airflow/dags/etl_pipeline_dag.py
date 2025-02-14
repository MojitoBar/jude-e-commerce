import sys
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# 상대 경로로 scripts 디렉토리 추가
dag_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(dag_dir)
scripts_dir = os.path.join(project_dir, 'scripts')
sys.path.append(scripts_dir)

# import 경로 수정
from etl_pipeline import run_etl_script

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
        python_callable=run_etl_script,
    )

    run_etl 