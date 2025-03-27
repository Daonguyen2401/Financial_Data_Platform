from pyspark.sql import SparkSession

# Connect to Spark Cluster
spark = SparkSession.builder \
    .appName("DockerSparkClusterApp") \
    .master("spark://localhost:7077") \
    .config("spark.submit.deployMode", "client") \
    .getOrCreate()

# Sample DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["Name", "Age"])

import numpy as np
fax_num = np.array([1, 2, 3, 4, 5])


###
from boltons.iterutils import chunked, windowed
from boltons.dictutils import OMD  # Ordered MultiDict

# Chunking a list into smaller parts
data = list(range(10))
print("Chunked list:", list(chunked(data, 3)))

# Sliding window example
print("Sliding window (size=3):", list(windowed(data, 3)))

# Ordered MultiDict (like a dict but supports multiple values per key)
omd = OMD()
omd.add('fruit', 'apple')
omd.add('fruit', 'banana')
omd.add('fruit', 'cherry')

print("Ordered MultiDict items:", omd.getlist('fruit'))

###

# Show DataFrame
df.show()

# Stop Spark
spark.stop()
