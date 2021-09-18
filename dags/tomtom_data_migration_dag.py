from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    'tomtom_data_migration',
    default_args=default_args,
    description='Tomtom Data Migration',
    schedule_interval="@once",
    start_date=datetime.strptime("2021-09-10", '%Y-%m-%d'),
    catchup=False
) as dag:

    t1 = BashOperator(
        task_id='tomtom_data_migration',
        bash_command='python /opt/airflow/dags/tomtom_data_migration.py --connection %s' % Variable.get("data_dev_connection")
    )
