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

## Setup Data 

Create 2 tables in a single dataset 

1. crm_account_rsl

```sql
CREATE ROW ACCESS POLICY crm_account_filter
ON `demos-vertex-ai.z_test.crm_account_rsl`
GRANT TO('user:bruce@justinjm.altostrat.com')
FILTER USING(State_Code='CA')
```

2. crm_user_rsl

```sql
CREATE ROW ACCESS POLICY crm_user_filter
ON `demos-vertex-ai.z_test.crm_user_rsl`
GRANT TO('user:bruce@justinjm.altostrat.com')
FILTER USING(Country_Code = 'US')
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
      ["demos-vertex-ai", "z_test", "crm_account_rsl"]
  ]
}

```

## Create BigQuery UDF

```sql
CREATE OR REPLACE FUNCTION
  z_test.get_row_access_policies(table_catalog STRING,
    table_schema STRING,
    table_name STRING)
  RETURNS STRING REMOTE
  -- change this to reflect your PROJECT ID
WITH CONNECTION `demos-vertex-ai.us.gcf-conn` OPTIONS (
    -- change this to reflect the Trigger URL of your cloud function (look for the TRIGGER tab)
    endpoint = 'https://us-central1-demos-vertex-ai.cloudfunctions.net/bq-table-row-access-policies' )
```

## Invoke remote function from BigQuery


```sql
SELECT
  table_catalog,
  table_schema,
  table_name,
  `z_test`.get_row_access_policies(table_catalog, table_schema, table_name) as rowAccessPolicies
FROM
  z_test.INFORMATION_SCHEMA.TABLES
```

<https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#string_for_json>


```sql
WITH data AS (
  SELECT
  table_catalog,
  table_schema,
  table_name,
  `z_test`.get_row_access_policies(table_catalog, table_schema, table_name) as reply
FROM
  z_test.INFORMATION_SCHEMA.TABLES
) 
SELECT
  * EXCEPT(reply),
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].rowAccessPolicyReference.policyId'), '"', '') AS policyId,
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].filterPredicate'), '"', '') AS filterPredicate,
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].creationTime'), '"', '') AS creationTime,
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].lastModifiedTime'), '"', '') AS lastModifiedTime

FROM data
```


## Resources

BigQuery Row Level Security

* [Use row-level security  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/managing-row-level-security#bq)
* [Method: rowAccessPolicies.list  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list#RowAccessPolicy)
* [HTTP Tutorial  |  Cloud Functions Documentation  |  Google Cloud](https://cloud.google.com/functions/docs/tutorials/http-1st-gen)

BigQuery Remote Functions

* [Working with Remote Functions  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#sample_code)
* [Remote Functions in BigQuery. How it works, and what you can do with… | by Lak Lakshmanan | Towards Data Science](https://towardsdatascience.com/remote-functions-in-bigquery-af9921498438) - good tutorial by former Googler

BigQuery Information Schema

* [TABLES view  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/information-schema-tables)
