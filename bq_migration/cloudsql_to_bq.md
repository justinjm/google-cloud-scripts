# Cloud SQL to GCS to BigQuery



## Outline


* create SQL instance
* load data
  * export to GCS 
  * load into SQL
* 

```sh
gcloud sql instances create dev-instance --database-version=POSTGRES_9_6 --cpu=2 --memory=4GiB --zone=us-west1-a --root-password=password123
```
