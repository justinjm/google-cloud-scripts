
# check if bucket exists
def check_bucket_existence(PROJECT_ID, BUCKET_PATH):
    from google.cloud import storage
    from google.cloud.storage import Bucket

    client = storage.Client(project=PROJECT_ID)
    exists = Bucket(client, BUCKET_PATH).exists()
    return exists

# create bucket if needed
if check_bucket_existence(PROJECT_ID, BUCKET_NAME) == False:
    ! gsutil mb -c standard -l $REGION -b on -p $PROJECT_ID $BUCKET_PATH
    ! gsutil ls
else:
    print(f"Bucket {BUCKET_NAME} already exists")