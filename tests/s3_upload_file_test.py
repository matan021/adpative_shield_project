from minio import Minio
from minio.error import S3Error

# Function to create a sample file
def create_sample_file(file_path):
    with open(file_path, 'w') as file:
        file.write("Hello, MinIO! This is a sample file.")

# Path to the file to be uploaded
file_path = "sample_file.txt"
create_sample_file(file_path)

# Initialize the Minio client
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Create a bucket if it doesn't exist
bucket_name = "my-bucket"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
else:
    print(f"Bucket '{bucket_name}' already exists")

# Upload the file
object_name = "sample_file.txt"

try:
    client.fput_object(bucket_name, object_name, file_path)
    print(f"'{file_path}' is successfully uploaded as '{object_name}' to bucket '{bucket_name}'.")
except S3Error as e:
    print(f"An error occurred: {e}")
