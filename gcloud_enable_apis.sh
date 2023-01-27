export PROJECT=$DEVSHELL_PROJECT_ID

gcloud services enable --project $PROJECT composer.googleapis.com
gcloud services enable --project $PROJECT compute.googleapis.com
gcloud services enable --project $PROJECT bigquery-json.googleapis.com
gcloud services enable --project $PROJECT dataproc.googleapis.com
gcloud services enable --project $PROJECT pubsub.googleapis.com
gcloud services enable --project $PROJECT storage-api.googleapis.com
gcloud services enable --project $PROJECT dataflow.googleapis.com
gcloud services enable --project $PROJECT drive.googleapis.com
gcloud services enable --project $PROJECT stackdriver.googleapis.com
gcloud services enable --project $PROJECT logging.googleapis.com
gcloud services enable --project $PROJECT monitoring.googleapis.com
gcloud services enable --project $PROJECT datafusion.googleapis.com
gcloud services enable --project $PROJECT bigtable.googleapis.com


# https://cloud.google.com/sdk/gcloud/reference/services/enable?hl=en