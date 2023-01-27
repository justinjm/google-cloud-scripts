library(bigrquery)
library(gargle)

options(
  gargle_oauth_email = Sys.getenv("GARGLE_EMAIL"),
  gargle_oauth_cache = TRUE
)

scope <- c("https://www.googleapis.com/auth/cloud-platform")
token <- token_fetch(scopes = scope)

bq_auth(token = token)

project_id <- Sys.getenv("GCP_PROJECT_ID")

dataset <- paste(project_id, "bigrquerytest1", sep = ".")
table <- paste(dataset, "loan", sep = ".")

bq_project_datasets(project_id)

bq_dataset_create(dataset, location = "US")

bq_dataset_exists(dataset)
bq_dataset_tables(dataset)

bq_table_load(table,
              fields = list(
                bq_field("id",              "INTEGER"),
                bq_field("member_id",       "INTEGER"),
                bq_field("loan_amnt",       "INTEGER"),
                bq_field("term_in_months",  "INTEGER"),
                bq_field("interest_rate",   "FLOAT"),
                bq_field("payment",         "FLOAT"),
                bq_field("grade",           "STRING"),
                bq_field("sub_grade",       "STRING"),
                bq_field("employment_length", "INTEGER"),
                bq_field("home_owner",      "INTEGER"),
                bq_field("income",          "FLOAT"),
                bq_field("verified",        "INTEGER"),
                bq_field("default",         "INTEGER"),
                bq_field("purpose",         "STRING"),
                bq_field("zip_code",        "STRING"),
                bq_field("addr_state",      "STRING"),
                bq_field("open_accts",      "INTEGER"),
                bq_field("credit_debt",     "INTEGER")
              ),
              nskip = 1,
              source_format = "CSV",
              source_uris = "gs://demos-vertex-ai-bq-staging/loan_200k.csv",
              create_disposition = "CREATE_IF_NEEDED", 
              write_disposition = "WRITE_TRUNCATE")

bq_table_fields(table)

bq_table_delete(table)





## Gargle 
# https://github.com/r-lib/gargle
# https://gargle.r-lib.org/articles/how-gargle-gets-tokens.html#credentials_app_default
# https://gargle.r-lib.org/articles/how-gargle-gets-tokens.html#credentials_service_account

## bigrquery
# https://github.com/r-dbi/bigrquery

## misc
# https://stackoverflow.com/questions/51181966/r-to-bigquery-data-upload-error