# Google Cloud Storage to BigQuery and Data Validation Tool (DVT)

* Remote functions - [Working with Remote Functions  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions)

* Data Transfer - [Cloud Storage transfers  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/cloud-storage-transfer#bq)
* DVT - [GoogleCloudPlatform/professional-services-data-validator: Utility to compare data between homogeneous or heterogeneous environments to ensure source and target tables match](https://github.com/GoogleCloudPlatform/professional-services-data-validator)

## Outline

### Setup

* Setup environment - local
  * download source code to cloud shell
  
* Setup environment - GCP 
  * enable APIS 
  * create GCS bucket and grant permissions to default compute engine SA 

* Setup MSSQL 
  * Provision SQL Server VM instance
  * Load sample data to SQL server 

* Setup BQ - Remote function
  * create 
  * create remote function connection
  * create remote function `CREATE FUNCTION` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_function_statement>

* setup DVT
  * install DVT <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/installation.md>
  * install connection - MSSQL Server -  <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md#mssql-server>
  * add connections 

### Automation

* extract data
* load data
* run validation

template: 
```
data-validation validate column \
    --source-conn MY_BQ_CONN --target-conn MY_SQL_CONN \
    --tables-list project.dataset.source_table=database.target_table
```

## DVT - initial test (BQ to BQ validation test)


* copy table in BQ `demo_dataset1` to `demo_dataset2`: 
  
```
bq cp demo_dataset1.loans demo_dataset2.loans
```

* open cloud shell editor 
* download / install configure DVT <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/installation.md>

```
sudo apt-get install python3
sudo apt-get install python3-dev
python -m venv venv
source venv/bin/activate
sudo apt-get update  && sudo apt-get install gcc -y && sudo apt-get clean
pip install --upgrade pip
pip install google-pso-data-validator
```

* Create a sample BQ connection 

```
data-validation connections add --connection-name MY_BQ_CONN BigQuery --project-id demos-vertex-ai
```

* view it 

```
cat /home/bruce/.config/google-pso-data-validator/MY_BQ_CONN.connection.json
```

* first validation: COUNT(*) on a table

```
data-validation validate column -sc MY_BQ_CONN -tc MY_BQ_CONN -tbls bigquery-public-data.new_york_citibike.citibike_trips
```

<https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/examples.md>

* second

```
data-validation validate column \
    --source-conn MY_BQ_CONN --target-conn MY_BQ_CONN \
    --tables-list demos-vertex-ai.demo_dataset1.loans=demos-vertex-ai.demo_dataset2.loans \
    --count '*'    
```

* third - save results as bq table  (reaactivate `venv` first)

```
source venv/bin/activate
```

```
data-validation validate column \
    --source-conn MY_BQ_CONN --target-conn MY_BQ_CONN \
    --tables-list demos-vertex-ai.demo_dataset1.loans=demos-vertex-ai.demo_dataset2.loans \
    --count '*' \
    -bqrh demos-vertex-ai.pso_data_validator.results
```
