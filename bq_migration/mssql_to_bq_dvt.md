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

install MSSQL driver on cloud shell

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

* spin up MSQL server instance

```sh
gcloud beta sql instances create mssqlserverinstance \
--database-version=SQLSERVER_2017_STANDARD \
--cpu=2 \
--memory=4GB \
--root-password=password123 \
--zone=us-central1-a
```

* Create instance doc: <https://cloud.google.com/sql/docs/sqlserver/create-instance>
* gcloud doc: <https://cloud.google.com/sdk/gcloud/reference/sql/instances/create>


* get info from instance 

```json
{
    # Configuration Required for All Data Sources
    "source-type": "MSSQL",

    # Connection Details
    "host": "127.0.0.1",
    "port": 1433,
    "user": "my-user",
    "password": "my-password",
    "database": "my-db",

}
```

DVT doc: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md#mssql-server>

* test access to instance 