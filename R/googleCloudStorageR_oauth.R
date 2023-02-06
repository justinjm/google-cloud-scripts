
## set default project and bucket via environment in .Renviron 
project_id <- Sys.getenv("GCP_PROJECT_ID")
bucket <- Sys.getenv("GCS_DEFAULT_BUCKET")
email <- Sys.getenv("GARGLE_AUTH_EMAIL")

# install required packages if not already 
packages <- c("googleCloudStorageR", "gargle")
install.packages(setdiff(packages, rownames(installed.packages())))

# load packages 
library(googleCloudStorageR)
library(gargle)
# options(gargle_verbosity = "debug")

## Fetch token. See: https://developers.google.com/identity/protocols/oauth2/scopes
scope <- c("https://www.googleapis.com/auth/cloud-platform")
token <- token_fetch(scopes = scope,
                     email = email) # set email to auth without browser dance

## Pass your token to gcs_auth
gcs_auth(token = token)

gcs_list_buckets(projectId = project_id)

gcs_get_bucket(bucket = bucket)
