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

While GCF is deploying, grant the app engine default service account BigQuery permissions (you can remove/adjust this later)

```sh
gcloud projects add-iam-policy-binding demos-vertex-ai \
    --member=serviceAccount:demos-vertex-ai@appspot.gserviceaccount.com \
    --role=roles/bigquery.admin
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


```sh
gcloud projects add-iam-policy-binding demos-vertex-ai \
    --member=serviceAccount:bqcx-746038361521-agnk@gcp-sa-bigquery-condel.iam.gserviceaccount.com \
    --role=roles/bigquery.admin
```
