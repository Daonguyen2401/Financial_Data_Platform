from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from source_system.vnstock.stock_listing import Stock_Listing
import logging
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import os
import glob

from common import utils


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
    'silver_stock_listing_dag',
    default_args=default_args,
    description='tesing_silver',
    schedule_interval=timedelta(days=1),
    catchup=False,
)
# Path to spark.conf file
spark_conf_path = './config/spark.conf'
# Read configurations from spark.conf file
spark_conf = utils.read_spark_conf(spark_conf_path)

jars = utils.read_jars_file('./spark_jobs/jars')

# Define the Spark Submit Operator

# python_job_conf = PythonOperator(
#     task_id='python_job_conf',
#     python_callable=lambda: print("SparkCONFI",spark_conf),
#     dag=dag
# )
# python_job_jar = PythonOperator(
#     task_id='python_job_jar',
#     python_callable=lambda: print("JARS",jars),
#     dag=dag
# )

spark_bash_job = BashOperator(
    task_id='spark_delta_job_bash',
    bash_command="""spark-submit --master spark://spark-master:7077 --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 --conf spark.hadoop.fs.s3a.access.key=adminMinio --conf spark.hadoop.fs.s3a.secret.key=adminMinio --conf spark.hadoop.fs.s3a.path.style.access=true --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog --conf spark.jars.packages=io.delta:delta-spark_2.12:3.3.0 --conf spark.network.timeout=600s --conf spark.connector.name=hive --conf spark.hadoop.hive.metastore.uris=thrift://hive-metastore:9083 --conf spark.sql.hive.thriftServer.singleSession=true --conf spark.sql.warehouse.dir=s3a://spark-bucket/warehouse --jars /opt/***/spark_jobs/jars/aws-java-sdk-bundle-1.12.262.jar,/opt/***/spark_jobs/jars/hadoop-aws-3.3.4.jar,/opt/***/spark_jobs/jars/hadoop-cloud-storage-3.3.4.jar,/opt/***/spark_jobs/jars/hadoop-common-3.3.4.jar,/opt/***/spark_jobs/jars/hadoop-mapreduce-client-core-3.3.4.jar --executor-cores 2 --executor-memory 1gb --driver-memory 2g --name spark_delta_job --verbose --deploy-mode client /opt/airflow/spark_jobs/testspark_delta.py""",
    dag=dag
)

# spark_job = SparkSubmitOperator(
#     task_id='spark_delta_job',
#     conn_id='spark',  # Configure this connection in Airflow
#     application='/opt/airflow/spark_jobs/testspark_delta.py',
#     name='spark_delta_job',
#     verbose=True,
#     deploy_mode='client',  # Client mode as specified
#     jars=jars,
#     conf= spark_conf,  # Apply configurations from spark.conf
#     # Add these options to potentially help:
#     total_executor_cores='2',
#     num_executors='1',
#     driver_memory='2g',  # Adjust as needed for Airflow worker
#     executor_memory='1gb',
#     executor_cores='2',
#     dag=dag
# )

spark_bash_job