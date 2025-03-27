from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, when
from datetime import datetime, timedelta

class ETLProcessor:
    def __init__(self):
        self.spark = SparkSession.builder.appName("Complex_Transform_Example").getOrCreate()
        self.df = None

    def extract(self, source_path):
        # Đọc dữ liệu từ nguồn
        self.df = self.spark.read.csv(source_path, header=True, inferSchema=True)
        # Cache dữ liệu vì sẽ dùng lại nhiều lần
        self.df.cache()
        return self

    def transform_step1_filter(self):
        # Bước 1: Lọc các đơn hàng > 100
        self.df = self.df.filter(col("amount") > 100)
        return self

    def transform_step2_aggregate(self):
        # Bước 2: Tính tổng chi tiêu theo customer_id
        agg_df = self.df.groupBy("customer_id").agg(sum("amount").alias("total_spent"))
        # Join lại với self.df để giữ thông tin đơn hàng gốc
        self.df = self.df.join(agg_df, "customer_id", "left")
        return self

    def transform_step3_classify(self):
        # Bước 3: Thêm cột phân loại khách hàng dựa trên total_spent
        self.df = self.df.withColumn(
            "customer_type",
            when(col("total_spent") > 1000, "VIP")
            .when(col("total_spent") > 500, "Regular")
            .otherwise("Basic")
        )
        return self

    def transform_step4_recent_orders(self):
        # Bước 4: Tạo DataFrame riêng cho các đơn hàng gần đây (giả sử có cột date)
        current_date = datetime.now()
        thirty_days_ago = current_date - timedelta(days=30)
        recent_df = self.df.filter(col("date") > thirty_days_ago.strftime("%Y-%m-%d"))
        return recent_df

    def load(self, output_path_main, output_path_recent):
        # Ghi dữ liệu chính (self.df) và dữ liệu đơn hàng gần đây
        self.df.write.mode("overwrite").parquet(output_path_main)
        recent_df = self.transform_step4_recent_orders()
        recent_df.write.mode("overwrite").parquet(output_path_recent)
        return self

    def run(self, source_path, output_path_main, output_path_recent):
        # Chạy toàn bộ pipeline
        (self.extract(source_path)
             .transform_step1_filter()
             .transform_step2_aggregate()
             .transform_step3_classify()
             .load(output_path_main, output_path_recent))
        # Giải phóng cache sau khi hoàn tất
        self.df.unpersist()

# Sử dụng class
if __name__ == "__main__":
    etl = ETLProcessor()
    etl.run("input_orders.csv", "output_main.parquet", "output_recent.parquet")