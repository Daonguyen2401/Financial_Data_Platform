from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from abc import ABC, abstractmethod



class SparkBase(ABC):
    def __init__(self, app_name="SparkBase", master="spark://spark-master:7077", deploy_mode="client"):
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .master(master) \
            .config("spark.submit.deployMode", deploy_mode) \
            .getOrCreate()
        
    @abstractmethod
    def create_source_des(self,from_layer,from_table,to_layer,to_table):
        """Create a source and destination table."""
        self.source_path = f"s3a://{from_layer}/{from_table}"
        self.destination_path = f"s3a://{to_layer}/{to_table}"
        
    @abstractmethod
    def extract(self)-> DataFrame:
        """Extract data from the source."""
        return self.spark.read.format("delta").load(self.source_path)
    
    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        """Transform the data."""
        return df
    
    @abstractmethod
    def load(self, df: DataFrame, mode = "overwrite"):
        '''Load to MiniO'''
        df.write.format("delta").mode(mode).save(self.destination_path)
        
    @abstractmethod
    def run(self):
        """Run the entire ETL pipeline."""
        df = self.extract()
        transformed_df = self.transform(df)
        self.load(transformed_df)
