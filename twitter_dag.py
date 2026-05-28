from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from twitter_etl import run_twitter_etl


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='twitter_etl_dag',
    default_args=default_args,
    description='Run Twitter ETL pipeline to fetch tweets from a userand store in S3',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['twitter', 'etl'],
) as dag:

    extract_and_load = PythonOperator(
        task_id='run_twitter_etl',
        python_callable=run_twitter_etl,
    )

    extract_and_load
