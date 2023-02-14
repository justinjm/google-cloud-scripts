# DVT VM Setup

[Automate Validation using the Data Validation Tool (DVT) | Google Cloud Skills Boost](https://www.cloudskillsboost.google/focuses/45997?parent=catalog)

## install dvt and dependcies 

### install dependencies for DVT

```sh
# Startup script for running DVT on GCE Debian 10 VM. Requires sudo
# Install or update needed software
sudo apt-get update
sudo apt-get install -yq git python3 python3-pip python3-distutils
sudo pip install --upgrade pip virtualenv
```

### Activate venv and install DVT 


```sh
virtualenv -p python3 env
source env/bin/activate

# Install below  packages required for MSSQL
# Install DVT
pip install google-pso-data-validator 
```

### install MSSQL dependenceis 

DVT doc: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md#mssql-server>

#### install microsft ODBC 18

```sh
sudo su
curl <https://packages.microsoft.com/keys/microsoft.asc> | apt-key add -
#Debian 11
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

<https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline>

#### pyodbc

```sh
pip install pyodbc
sudo apt-get install unixodbc-dev
```


## create source and target connections 

DVT doc: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md>



### MSSQL

```sh
data-validation connections add \
    --connection-name MY_MSSQL_CONN MSSQL \
    --host 34.172.120.100 \
    --port 1433 \
    --user sqlserver \
    --password password123 \
    --database demo
```


### bigquery


```sh
data-validation connections add \
    --connection-name MY_BQ_CONN BigQuery \
    --project-id demos-vertex-ai
```