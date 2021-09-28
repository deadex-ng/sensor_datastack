from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import datetime

# [START default_args]
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 9, 28),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}
# [END default_args]

# [START instantiate_dag]
load_initial_data_dag = DAG(
    '1_load_initial_data',
    default_args=default_args,
    schedule_interval = None,
)

t1 = PostgresOperator(task_id='create_schema',
                      sql="CREATE SCHEMA IF NOT EXISTS dbt_raw_data;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t2 = PostgresOperator(task_id='drop_table_districts',
                      sql="DROP TABLE IF EXISTS districts;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t3 = PostgresOperator(task_id='create_districts',
                      sql="create table if not exists dbt_raw_data.districts (ID integer, Name varchar(100) );",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t4 = PostgresOperator(task_id='load_districts',
                      sql="COPY dbt_raw_data.districts FROM '/sample_data/data/districts.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)
t5 = PostgresOperator(task_id='drop_table_station_summary',
                      sql="DROP TABLE IF EXISTS station_summary;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t6 = PostgresOperator(task_id='create_station_summary',
                      sql="create table if not exists dbt_raw_data.station_summary(ID numeric, flow_99 integer, flow_max integer, flow_median integer,flow_total integer, n_obs integer);",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

#t7 = PostgresOperator(task_id='load_station_summary',
#                      sql="	COPY dbt_raw_data.station_summary FROM '/sample_data/data/station_summary.csv' DELIMITER ',' CSV HEADER;",
#                      postgres_conn_id='dbt_postgres_instance_raw_data',
#                      autocommit=,
#                      database="dbtdb",
#                      dag=load_initial_data_dag)                     

t1 >> t2 >> t3 >> t4
t1 >> t5 >> t6 

