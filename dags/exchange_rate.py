from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator


def api_call():
    from airflow.models import Variable
    import requests
    import psycopg2

    url = 'https://api.exchangerate.host/latest?base=BTC&symbols=USD&source=crypto'
    response = requests.get(url)
    data = response.json()

    conn = psycopg2.connect(database="postgres", user='postgres', password='postgres', host=Variable.get("pg_ip"), port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO rates(pair, date, rate, timestamp) VALUES ('BTC/USD', {data['date']}, {data['rates']['USD']}, current_timestamp)''')
    conn.close()

    print('Run successfully')
    

with DAG(
    'best_dag_ever',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description='A simple tutorial DAG',
    schedule_interval='0 */3 * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example']
) as dag:
    t0 = PythonOperator(task_id='get_rate', python_callable=api_call)