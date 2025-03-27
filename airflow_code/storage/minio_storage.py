

from .storage_base import StorageBase
from deltalake import DeltaTable, write_deltalake

import pandas as pd

class MinioStorage(StorageBase):
    def __init__(self):
        super().__init__()
        # Initialize MinIO client
        self.endpoint = "minio:9000"
        self.access_key = "adminMinio"
        self.secret_key = "adminMinio"
        
    def append(self, df, bucket, object_name):
        try:


            # Construct the S3 path for the Delta table
            delta_table_path = f"s3://{bucket}/{object_name}"

            # Configure S3 storage options for MinIO
            storage_options = {
                "endpoint_url": f"http://{self.endpoint}",
                "AWS_REGION": "us-east-1",
                'AWS_ACCESS_KEY_ID': self.access_key,
                'AWS_SECRET_ACCESS_KEY': self.secret_key,
                'AWS_ALLOW_HTTP': 'true'  # Important for non-HTTPS connections
            }
            print("Storage options:", storage_options)


            try:
                # Try to open the existing Delta table
                delta_table = DeltaTable(delta_table_path, storage_options=storage_options)
                # Append the new data directly
                write_deltalake(delta_table, df, mode="append")
            except Exception as e:
                # If the table doesn't exist or other error, create it
                write_deltalake(delta_table_path, df, mode="overwrite", 
                               storage_options=storage_options)
            return True
        
        except Exception as e:
            print(f"Error appending to Delta table: {e}")
            return False
        
    def overwrite(self, df, bucket, object_name):
        try:
            # Construct the S3 path for the Delta table
            delta_table_path = f"s3://{bucket}/{object_name}"

            # Configure S3 storage options for MinIO
            storage_options = {
                "endpoint_url": f"http://{self.endpoint}",
                "AWS_REGION": "us-east-1",
                'AWS_ACCESS_KEY_ID': self.access_key,
                'AWS_SECRET_ACCESS_KEY': self.secret_key,
                'AWS_ALLOW_HTTP': 'true'  # Important for non-HTTPS connections
            }
            

            # Write the DataFrame to the Delta table
            write_deltalake(delta_table_path, df, mode="overwrite", 
                           storage_options=storage_options)
            return True
        except Exception as e:
            print(f"Error overwriting Delta table: {e}")
            return False
        
    def read(self, bucket, object_name):
        try:
            # Construct the S3 path for the Delta table
            delta_table_path = f"s3://{bucket}/{object_name}"

            # Configure S3 storage options for MinIO
            storage_options = {
                "endpoint_url": f"http://{self.endpoint}",
                "AWS_REGION": "us-east-1",
                'AWS_ACCESS_KEY_ID': self.access_key,
                'AWS_SECRET_ACCESS_KEY': self.secret_key,
                'AWS_ALLOW_HTTP': 'true'  # Important for non-HTTPS connections
            }
            print("Storage options:", storage_options)

            # Read the Delta table from MinIO
            df = DeltaTable(delta_table_path, storage_options=storage_options).to_pandas()
            return df
        except Exception as e:
            print(f"Error reading Delta table: {e}")
            return None

        

if __name__ == "__main__":
    storage = MinioStorage()
    df= pd.DataFrame({"num": [11, 22], "letter": ["aa", "bb"]})
    storage.append(df, "demobucket", "loremtable")
    
    df = storage.read("demobucket", "loremtable")
    print(df)