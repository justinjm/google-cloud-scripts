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
bq show --location=US --connection gcf-conn
```

## Setup Google Cloud Function 

* Cloud function v1 
* https 
* defaults 
* source: copy `main.py` into the source 
* change entry point to `get_row_access_polices`
* click deploy 

## make test call 

after deployment, test with sample values:

```txt
{
  "calls": [
      ["table1"],
      ["table2"],
      ["table3"]
  ]
}

```