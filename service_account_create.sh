
# Set the name of your service account
SA_NAME="my-service-account"

# Set the name of your project
PROJECT_ID="my-project-id"

# Create the service account
gcloud iam service-accounts create $SA_NAME --project $PROJECT_ID

# Grant the service account project editor permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member "serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role "roles/editor"