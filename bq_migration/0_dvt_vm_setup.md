# DVT VM Setup

[Automate Validation using the Data Validation Tool (DVT) | Google Cloud Skills Boost](https://www.cloudskillsboost.google/focuses/45997?parent=catalog)

## create VM 

Debian GNU/Linux 11 (bullseye)

```sh
gcloud compute instances create data-validator --project=demos-vertex-ai --zone=us-central1-a --machine-type=e2-medium --network-interface=network-tier=PREMIUM,subnet=default --metadata=enable-oslogin=true --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=746038361521-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=http-server,https-server --create-disk=auto-delete=yes,boot=yes,device-name=data-validator,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230206,mode=rw,size=10,type=projects/demos-vertex-ai/zones/us-central1-a/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any
```

## Add VM IP to Cloud SQL instance 

add 
name: data-validator
Range: `<IP ADDRESS>`

## install dvt and dependcies 

SSH into instance and run the following

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
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
#Debian 11
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev
# optional: kerberos library for debian-slim distributions
sudo apt-get install -y libgssapi-krb5-2
```


<https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline>

#### pyodbc

```sh
pip install pyodbc
```



## create source and target connections 

GCP doc: <https://cloud.google.com/sql/docs/sqlserver/connect-overview>
DVT doc: <https://github.com/GoogleCloudPlatform/professional-services-data-validator/blob/develop/docs/connections.md>

### MSSQL

* create a connection to MS SQL Server Cloud SQL instance:

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