# Google Cloud Storage to BigQuery and Data Validation Tool (DVT)

* [What is Cloud SQL?  |  Cloud SQL for SQL Server  |  Google Cloud](https://cloud.google.com/sql/docs/sqlserver/introduction)
  * [What is Cloud SQL?  |  Cloud SQL for SQL Server  |  Google Cloud](https://cloud.google.com/sql/docs/sqlserver/introduction)
* [gsutil tool  |  Cloud Storage  |  Google Cloud](https://cloud.google.com/storage/docs/gsutil)
  * [cp - Copy files and objects  |  Cloud Storage  |  Google Cloud](https://cloud.google.com/storage/docs/gsutil/commands/cp#synchronizing-over-os-specific-file-types-such-as-symlinks-and-devices)
* DVT - [GoogleCloudPlatform/professional-services-data-validator: Utility to compare data between homogeneous or heterogeneous environments to ensure source and target tables match](https://github.com/GoogleCloudPlatform/professional-services-data-validator)

## Overview

This file documents the steps to setup and run a workflow of validating data in the destination (BQ) against the original source (Cloud SQL - MSSQL Server)

## Setup

* Setup environment - local (part 1 of 2)
  * download source code to cloud shell

* Setup environment - GCP
  * enable APIS
  * create GCS bucket and grant permissions to default compute engine SA
  * locate sample dataset in GCS bucket

* Setup MSSQL 
  * Provision SQL Server VM instance [What is Cloud SQL?  |  Cloud SQL for SQL Server  |  Google Cloud](https://cloud.google.com/sql/docs/sqlserver/introduction)
  * Load sample data to SQL server

* Setup environment - local (part 2 of 2)
  * install and configure DVT <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/installation.md>
    * install connection for MSSQL Server 
      * DVT docs: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md#mssql-server>
      * MSSQL Server: <https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=debian18-install%2Cdebian17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline>
    * add connections
      * MSSQL Server
      * BQ

## Workflow: Validate data in destination table (BQ) with source table (MSSQL Server)

TODO

## DVT Hello world test: BQ source vs BQ target table

* create GCS bucket with sample dataset 

TODO

* load data into GCS bucket

```sh
curl https://raw.githubusercontent.com/sedeh/Datasets/main/loan_200k.csv | gsutil cp - gs://demos-vertex-ai-bq-staging/loan_200k.csv
```

* load data from GCS to BQ table

TODO (grab from `gcp-bigquery` repo)

* create copy of existing demo dataset for comparison. copy table in BQ `demo_dataset1` to `demo_dataset2`: 
  
```sh
bq cp demo_dataset1.loans demo_dataset2.loans
```

we now have `demo_dataset1.loans` as the source table and `demo_dataset2.loans` as the target table. 

* open cloud shell editor 
* download / install configure DVT per instructions here: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/installation.md>

```sh
sudo apt-get install python3
sudo apt-get install python3-dev
python -m venv venv
source venv/bin/activate
sudo apt-get update  && sudo apt-get install gcc -y && sudo apt-get clean
pip install --upgrade pip
pip install google-pso-data-validator
```

* Create a sample BQ connection 

```sh
data-validation connections add --connection-name MY_BQ_CONN BigQuery --project-id demos-vertex-ai
```

* view it to verify 

```sh 
cat /home/bruce/.config/google-pso-data-validator/MY_BQ_CONN.connection.json
```

* first validation: COUNT(*) on a table

```sh 
data-validation validate column \
  -sc MY_BQ_CONN -tc MY_BQ_CONN \
  -tbls bigquery-public-data.new_york_citibike.citibike_trips
```

* second validation: COUNT(*) between 2 tables 

```sh
data-validation validate column \
    --source-conn MY_BQ_CONN --target-conn MY_BQ_CONN \
    --tables-list demos-vertex-ai.demo_dataset1.loans=demos-vertex-ai.demo_dataset2.loans \
    --count '*'    
```

* third: COUNT(*) between 2 tables and save results as a BQ table  (reaactivate `venv` first if needed)

```sh
# source venv/bin/activate
data-validation validate column \
    --source-conn MY_BQ_CONN --target-conn MY_BQ_CONN \
    --tables-list demos-vertex-ai.demo_dataset1.loans=demos-vertex-ai.demo_dataset2.loans \
    --count '*' \
    --bq-result-handler demos-vertex-ai.pso_data_validator.results
```

See more examples here: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/examples.md>

## DVT Install Test - MSSQL Server 

### install MSSQL driver on cloud shell

```sh
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Download appropriate package for the OS version
#Debian 11
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
```

* install `pyodbc` package

```sh
# source venv/bin/activate
pip install pyodbc
```

### spin up MSQL server instance

* create instance

```sh
gcloud beta sql instances create mssqls-instance \
  --database-version=SQLSERVER_2017_STANDARD \
  --cpu=2 \
  --memory=4GB \
  --root-password=password123 \
  --zone=us-central1-a
```

Create instance doc: <https://cloud.google.com/sql/docs/sqlserver/create-instance>  
gcloud doc: <https://cloud.google.com/sdk/gcloud/reference/sql/instances/create>

* create VM to connect to instance 

```sh
gcloud compute instances create instance-1 --project=demos-vertex-ai --zone=us-central1-a --machine-type=e2-medium --network-interface=network-tier=PREMIUM,subnet=default --metadata=enable-oslogin=true --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=746038361521-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=http-server --create-disk=auto-delete=yes,boot=yes,device-name=instance-1,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230206,mode=rw,size=10,type=projects/demos-vertex-ai/zones/us-central1-a/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any
```

* add IP to instance connections 

UI: Cloud SQL -> Instance -> connections -> authorized network 

Copy paste external IP from VM instance 

* configure VM - install `sqlcmd`

```sh
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update
sudo apt-get install mssql-tools unixodbc-dev
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
```

<https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools?view=sql-server-2017&tabs=ubuntu-install%2Credhat-offline#ubuntu>

* create a password for user `sqlserver` 

<https://cloud.google.com/sql/docs/sqlserver/create-manage-users#user-root>

* Connect to the instance 

```
# sqlcmd -S <IP-ADDRESS> -U <USERNAME> -P '<PASSWORD>'
sqlcmd -S 34.172.120.100 -U sqlserver -P 'password123'
```

* create new database for loading data 

UI: Databases -> Create Database  `demo`

* create SQL dump file from CSV for `loans_200.csv` via [convertcsv.com](https://www.convertcsv.com/csv-to-sql.htm). There is also an API version that was not used for this tutorial: <https://www.convertcsv.io/products/csv2sql>

input: `loan_200.csv`
output: `loans.sql` 

<https://www.sqlservertutorial.net/load-sample-database/>
<https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-2017>

* upload loans.sql file to GCS bucket

```sh
gsutil cp loans.sql gs://demos-vertex-ai-bq-staging/loans.sql
```

* grant service account access to GCS bucket (get service account from UI, instance overview page)

```sh
gsutil iam ch serviceAccount:p746038361521-irmwld@gcp-sa-cloud-sql.iam.gserviceaccount.com:objectAdmin \
  gs://demos-vertex-ai-bq-staging/
```

* execute data loading: load data (SQL file) to SQL instance from GCS 

```sh
gcloud sql import sql mssqls-instance gs://demos-vertex-ai-bq-staging/loans.sql \
  --database=demo
```

<https://cloud.google.com/sql/docs/sqlserver/import-export/import-export-sql#gcloud>


* view databases

```sh
SELECT s.name as schema_name, s.schema_id, u.name as schema_owner from sys.schemas s inner join sys.sysusers u on u.uid = s.principal_id order by s.name;
GO
```

* create dataset in BQ for validation against MSSQL (no default column)

```sql
CREATE OR REPLACE TABLE `demo.loans`
AS (SELECT * EXCEPT(`default`) FROM `demos-vertex-ai.demo_dataset1.loans`)
```

#### DVT 

* get info from SQL instance
  * IP address 


```sh
source venv/bin/activate
sudo apt-get install unixodbc-dev
```

* create DVT connection for MSSQL

```sh
data-validation connections add --connection-name MSSQL_CONN MSSQL --host 34.172.120.100 --port 1433 --user sqlserver --password password123 --database demo
```

DVT doc: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md#mssql-server>

* test access to instance - `count(*)` on table

```
data-validation validate column \
  -sc MSSQL_CONN \
  -tbls demo.demo.loans
```


* execute validation

```sh

data-validation validate column \
    --source-conn MY_BQ_CONN --target-conn MY_BQ_CONN \
    --tables-list demos-vertex-ai.demo_dataset1.loans=demos-vertex-ai.demo_dataset2.loans \
    --count '*' \
    --bq-result-handler demos-vertex-ai.pso_data_validator.results
```