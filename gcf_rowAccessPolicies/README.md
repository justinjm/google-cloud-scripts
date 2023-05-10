# Google CLoud Function - BQ Remote function for Row Level Access Policies 

Since as of 2023-05-10, Row Level Access Policies are only viewable via the API and `bq` CLI 

To begin, Open Cloud shell and follow the steps below

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor)


## enable apis


```sh
gcloud services enable bigqueryconnection.googleapis.com
```

## Setup connection

```sh
gcloud components update
bq mk --connection --display_name='get_row_access_policies' --connection_type=CLOUD_RESOURCE --project_id=$(gcloud config get-value project) --location=US  gcf-conn
```

Show connection info and copy service account, you will need this in a later step

```sh
bq show --location=US --connection gcf-conn
```


## Setup Google Cloud Function 

* Cloud function v1 
* https 
* defaults 
* source: copy `main.py` into the source 
* change entry point to `get_row_access_polices`
* click deploy 

### Grant service accounts acccess 

While GCF is deploying, grant account access in 2 places 


1. the app engine default service account BigQuery permissions (you can remove/adjust this later) so that the cloud 

```sh
gcloud projects add-iam-policy-binding demos-vertex-ai \
    --member=serviceAccount:demos-vertex-ai@appspot.gserviceaccount.com \
    --role=roles/bigquery.admin
```

2. Grant 

```sh
gcloud functions add-iam-policy-binding bq-table-row-access-policies \
    --member=serviceAccount:bqcx-746038361521-agnk@gcp-sa-bigquery-condel.iam.gserviceaccount.com \
    --role=roles/cloudfunctions.invoker
```

## make test call 

after deployment, test with sample values:

```txt
{
  "calls": [
      ["crm_account_rsl"]
  ]
}

```

## Create BigQuery UDF

```sql
CREATE OR REPLACE FUNCTION z_test.get_row_access_policies(table_catalog STRING, table_schema STRING, table_name STRING) RETURNS STRING
REMOTE WITH CONNECTION `demos-vertex-ai.us.gcf-conn` -- change this to reflect your PROJECT ID
OPTIONS (
    -- change this to reflect the Trigger URL of your cloud function (look for the TRIGGER tab)
    endpoint = 'https://us-central1-demos-vertex-ai.cloudfunctions.net/bq-table-row-access-policies'
)
```

## Invoke remote function from BigQuery


```sql
SELECT
  table_name,
  `z_test`.get_row_access_policies(table_name) as rowAccessPolicies
FROM
  z_test.INFORMATION_SCHEMA.TABLES
```

<https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#string_for_json>


## Resources

* [Working with Remote Functions  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#sample_code)
* [Remote Functions in BigQuery. How it works, and what you can do with… | by Lak Lakshmanan | Towards Data Science](https://towardsdatascience.com/remote-functions-in-bigquery-af9921498438) - good tutorial by former Googler



[Use row-level security  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/managing-row-level-security#bq)
