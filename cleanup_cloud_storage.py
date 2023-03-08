from google.cloud import storage

# Replace with your project ID and the list of bucket names to delete
project_id = 'demos-vertex-ai'
bucket_names_to_delete = [
    'demos-vertex-ai-bqmlga4-demo', 'demos-vertex-ai-bqmlga4']

# Create a storage client object
client = storage.Client(project=project_id)

# Loop through each bucket name to delete
for bucket_name in bucket_names_to_delete:
    # Get a reference to the bucket object
    bucket = client.get_bucket(bucket_name)

    # Delete all objects in the bucket before deleting the bucket
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()

    # Delete the bucket itself
    bucket.delete()

    print(f'Deleted bucket {bucket_name} and its contents.')
