# multi-auth.R ---------------------------------------------------------------
## set constants 
### defaults from .Renviron 
project_id <- Sys.getenv("GCP_PROJECT_ID")
email <- Sys.getenv("GARGLE_AUTH_EMAIL")

bucket <- Sys.getenv("GCS_DEFAULT_BUCKET")
dataset <- Sys.getenv("BQ_DEFAULT_DATASET")

## load packages
library(googleCloudStorageR)
library(bigrquery)
library(gargle)

## authenticate 
### GCS
scope <- c("https://www.googleapis.com/auth/cloud-platform")
token <- token_fetch(scopes = scope,
                     email = email)
gcs_auth(token = token)

### BQ 
bq_auth(email = email)

## check authentication
gcs_list_buckets(projectId = project_id)
bq_project_datasets(project_id)


## References 
### gargle 
# https://cran.r-project.org/web/packages/gargle/vignettes/gargle-auth-in-client-package.html#getting-that-first-token

## gcs 
# https://code.markedmondson.me/googleCloudStorageR/reference/gcs_auth.html

## bq 
# [bq\_auth()](https://github.com/r-dbi/bigrquery/blob/main/R/bq-auth.R#L59) calls 
# [gargle::token\_fetch](https://github.com/r-lib/gargle/blob/main/R/token-fetch.R) function.
# This function uses multiple methods to fetch the auth token.
# 
# On GCE instances [credentials\_gce]() function will be used.
# 

### other  
# multi auth question - https://github.com/r-lib/gargle/issues/49