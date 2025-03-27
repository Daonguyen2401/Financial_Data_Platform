from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from source_system.vnstock.stock_listing import Stock_Listing
import logging



stock = Stock_Listing()

def get_stocks_listing_by_exchange():
    try:
        listing = stock.get_stocks_listing_by_exchange()
        logging.info("Stock listing by exchange is done")
        return True
    except Exception as e:
        print("Error getting stocks listing by exchange", e)
        logging.error("Error getting stocks listing by exchange: %s", e)
        return False

# Default arguments for the DAG
default_args = {
    'owner': 'daonguyen',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'bronze_stock_listing_dag',
    default_args=default_args,
    description='Danh sách mã chứng khoán, nhóm ngành',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Define the task
task_get_stocks_listing_by_exchange = PythonOperator(
    task_id='get_stocks_listing_by_exchange',
    python_callable=get_stocks_listing_by_exchange,
    dag=dag,
)

# Define task dependencies
task_get_stocks_listing_by_exchange