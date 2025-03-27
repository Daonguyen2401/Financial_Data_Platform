from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType



def create_spark_session():
    return SparkSession.builder \
        .appName("SparkMinIOTest") \
        .master("spark://localhost:7077") \
        .config("spark.submit.deployMode", "client") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")\
        .config("spark.hadoop.fs.s3a.access.key", "adminMinio") \
        .config("spark.hadoop.fs.s3a.secret.key", "adminMinio") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")\
        .config("spark.hadoop.fs.s3a.committer.name", "directory")\
        .config("spark.hadoop.fs.s3a.committer.staging.tmp.path", "/tmp/staging")\
        .config("spark.hadoop.fs.s3a.committer.threads", "4")\
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true") \
        .getOrCreate()

def test_minio_interaction():
    spark = create_spark_session()
    #spark.sparkContext.setLogLevel("debug")
    # Create sample data
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), False)
    ])
    
    data = [(1, "John"), (2, "Jane"), (3, "Bob")]
    df = spark.createDataFrame(data, schema)

    
    try:
        # Write to MinIO
        df.write.mode("overwrite").parquet("s3a://spark-bucket/testdata")
        print("Data written to MinIO successfully.")
    except Exception as e:
        print(f"Error writing to MinIO: {e}")
    
    # Read from MinIO
    # read_df = spark.read.parquet("s3a://spark-bucket/test-data")
    # read_df.show()
    
    spark.stop()

if __name__ == "__main__":
    test_minio_interaction()