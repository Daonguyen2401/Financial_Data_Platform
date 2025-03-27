from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def check_minio_connection() -> bool:
    """Check if MinIO connection is working"""
    try:
        s3_hook = S3Hook(aws_conn_id="minio_conn")
        s3_hook.get_conn()
        # Optional: Try a simple operation to verify
        buckets = s3_hook.check_for_bucket("haha")
        print(f"Successfully connected!,the buckets are {buckets}")
        return True
    except Exception as e:
        raise Exception(f"Failed to connect to MinIO: {str(e)}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'miniodag',
    default_args=default_args,
    description='A simple DAG that prints Hello, Airflow!',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Define the task
checkminio_task = PythonOperator(
    task_id='CheckWS3Connection',
    python_callable=check_minio_connection,
    dag=dag,
)

# Define task dependencies
checkminio_task