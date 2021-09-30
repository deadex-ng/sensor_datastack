from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime as dt
from datetime import timedelta

default_args = {
    'owner': 'dbtuser',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'start_date': dt(2021, 9, 13),
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'dbt_dag',
    default_args=default_args,
    description='An Airflow DAG to invoke simple dbt commands',
    schedule_interval='@once',
)

check_directory = BashOperator(
    task_id='bash_task', 
    bash_command='cd /dbt && dbt debug && dbt run && dbt docs generate && dbt docs serve', 
    do_xcom_push = True,
    dag=dag
)

check_directory
