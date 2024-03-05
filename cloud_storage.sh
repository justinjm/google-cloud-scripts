#!/bin/bash

BUCKET_NAME="demos-vertex-ai-test-2024-03-05"

## create gcs bucket
# check if a bucket exists and if not, create one
echo "Checking if bucket $BUCKET_NAME exists..."

if gsutil ls -b gs://$BUCKET_NAME &> /dev/null; then
  echo "Bucket $BUCKET_NAME already exists:"
  gsutil ls -b gs://$BUCKET_NAME
else
  echo "Bucket does not exist. Creating...."
  gsutil mb -l us-central1 gs://$BUCKET_NAME
  echo "Bucket created."
  gsutil ls -b gs://$BUCKET_NAME
fi

## delete bucket
# delete the bucket, prompting user first with a yes / no for sanity check
# echo "Deleting bucket $BUCKET_NAME..."

# gsutil rm -r gs://$BUCKET_NAME
