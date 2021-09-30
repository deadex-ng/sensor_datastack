from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import psycopg2
def create_connection():
    try:
        conn = psycopg2.connect(user='dbtuser',
                                password='pssd',
                                host= 'postgres-dbt',
                                port = '5432',
                                database = 'dbtdb')

    except psycopg2.Error as e:
        print(e)


"""insert or update database"""
def execute_command():
    #query =" COPY public.districts FROM '/sample_data/data/districts.csv' DELIMITER ',' CSV HEADER;"
    #query ="COPY public.station_summary FROM '/sample_data/data/station_summary.csv' DELIMITER ',' CSV HEADER;"
    #query ="COPY public.I80_stations FROM '/sample_data/data/I80_stations.csv' DELIMITER ',' CSV HEADER;"
    query ="COPY public.traffic_data FROM '/sample_data/data/traffic_data.csv' DELIMITER ',' CSV HEADER;"
    #query = "SELECT datname FROM pg_database;"
    con = psycopg2.connect(user='dbtuser',
                           password = 'pssd',
                           host ='postgres-dbt',
                           port = '5432',
                           database = 'dbtdb')
    #con = create_connection()
    cur = con.cursor()
    try:
        cur.execute(query)
        con.commit()
        print("saved")
        return cur.lastrowid
    except Exception as e:
        print(e)
        return None
    finally:
        cur.close()
        con.close()

with DAG(
    'python_dag', 
     description='Python DAG', 
     schedule_interval=None,
     start_date=datetime(2018, 11, 1), 
     catchup=False
     ) as dag:
          dummy_task 	= DummyOperator(task_id='dummy_task', retries=3)
          python_task	= PythonOperator(task_id='python_task', python_callable=execute_command)
dummy_task >> python_task
