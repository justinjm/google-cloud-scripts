# https://cloud.google.com/sdk/gcloud/reference/notebooks/instances/create

gcloud notebooks instances create automl-object-detection \
  --vm-image-project=deeplearning-platform-release \
  --vm-image-family=common-cpu-notebooks \
  --machine-type=n1-standard-4 \
  --location=us-central1-a \
  --boot-disk-type=PD_SSD


gcloud notebooks instances create vertex-pipelines-r \
    --vm-image-project=deeplearning-platform-release \
    --vm-image-family=common-cpu-notebooks \
    --machine-type=n1-standard-8 \
    --location=us-central1-a 