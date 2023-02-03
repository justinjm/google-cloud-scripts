# %%writefile src/test.R 
library(tidyverse)
library(dplyr)

sessionInfo()

library(googleCloudStorageR)
library(gargle)
# options(gargle_verbosity = "debug")

scope <- c("https://www.googleapis.com/auth/cloud-platform")
token <- token_fetch(scopes = scope)

gcs_auth(token = token)

gcs_list_objects(bucket = "vertex-r")