from minio import Minio
from minio.error import S3Error

def list_minio_buckets():
    try:
        # Initialize MinIO client
        minio_client = Minio(
            "localhost:9000",  # Replace with your MinIO server endpoint
            access_key="adminMinio",  # Access with Root User
            secret_key="adminMinio",  # Access with Root User
            secure=False  # Set to True if using HTTPS
        )
        
        # List all buckets
        buckets = minio_client.list_buckets()
        
        # Print bucket names
        print("List of buckets:")
        for bucket in buckets:
            print(f"- {bucket.name} (Created: {bucket.creation_date})")
            
    except S3Error as err:
        print(f"Error occurred: {err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

if __name__ == "__main__":
    list_minio_buckets()