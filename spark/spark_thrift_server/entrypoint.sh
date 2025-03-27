#!/bin/bash

# Start Spark Thrift Server
${SPARK_HOME}/sbin/start-thriftserver.sh \
  --master spark://spark-master:7077 \
  --conf spark.driver.bindAddress=0.0.0.0 \
  --packages org.apache.spark:spark-hive_${SCALA_VERSION}:${SPARK_VERSION}

# Keep the container running
tail -f /dev/null