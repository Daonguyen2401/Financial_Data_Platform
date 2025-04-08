from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType



def create_spark_session():
    return SparkSession.builder \
        .appName("SparkMinIOTest") \
        .master("spark://localhost:7077") \
        .config("spark.submit.deployMode", "client") \
        .getOrCreate()

def test_minio_delta_interaction():
    spark = create_spark_session()
    #spark.sparkContext.setLogLevel("debug")
    # Create sample data
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), False)
    ])
    
    data = [(1, "Nguyen"), (2, "Linh"), (3, "Bob")]
    df = spark.createDataFrame(data, schema)

    
    try:
        # Write to MinIO in Delta format
        df.write \
          .format("delta") \
          .mode("overwrite") \
          .save("s3a://spark-bucket/demo")
        print("Delta table written to MinIO successfully.")
    except Exception as e:
        print(f"Error writing Delta table to MinIO: {e}")
    
    # Read Delta table from MinIO
    try:
        read_df = spark.read.format("delta").load("s3a://silver/silver_listing_by_exchange_new-1d1e0ec77a5a49dc97db6f6fc79428a4")
        print("Reading Delta table from MinIO:")
        read_df.show()
    except Exception as e:
        print(f"Error reading Delta table from MinIO: {e}")
    
    spark.stop()

if __name__ == "__main__":
    test_minio_delta_interaction()