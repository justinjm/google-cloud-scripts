# Google Cloud Storage to BigQuery and Data Validation Tool (DVT)

* [What is Cloud SQL?  |  Cloud SQL for SQL Server  |  Google Cloud](https://cloud.google.com/sql/docs/sqlserver/introduction)
  * [What is Cloud SQL?  |  Cloud SQL for SQL Server  |  Google Cloud](https://cloud.google.com/sql/docs/sqlserver/introduction)
* [gsutil tool  |  Cloud Storage  |  Google Cloud](https://cloud.google.com/storage/docs/gsutil)
  * [cp - Copy files and objects  |  Cloud Storage  |  Google Cloud](https://cloud.google.com/storage/docs/gsutil/commands/cp#synchronizing-over-os-specific-file-types-such-as-symlinks-and-devices)
* DVT - [GoogleCloudPlatform/professional-services-data-validator: Utility to compare data between homogeneous or heterogeneous environments to ensure source and target tables match](https://github.com/GoogleCloudPlatform/professional-services-data-validator)

## Overview

## Setup

* Setup environment - local
  * download source code to cloud shell
  
* Setup environment - GCP
  * enable APIS
  * create GCS bucket and grant permissions to default compute engine SA
  * locate sample dataset in GCS bucket

* Setup MSSQL 
  * Provision SQL Server VM instance [What is Cloud SQL?  |  Cloud SQL for SQL Server  |  Google Cloud](https://cloud.google.com/sql/docs/sqlserver/introduction)
  * Load sample data to SQL server

* setup DVT
  * install DVT <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/installation.md>
  * install connection - MSSQL Server -  <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md#mssql-server>
  * add connections

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
