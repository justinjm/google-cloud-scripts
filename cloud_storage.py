from google.cloud import storage
from google.cloud.exceptions import NotFound

def check_and_create_bucket(bucket_name):
    client = storage.Client()
    try:
        client.get_bucket(bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except NotFound:
        bucket = client.create_bucket(bucket_name)
        print(f"Bucket {bucket_name} created.")