# https://github.com/statmike/vertex-ai-mlops/blob/main/08%20-%20R/08b_gcs%20Training%20Job%20-%20Vertex%20AI%20Custom%20Model%20-%20R%20-%20Training%20Pipeline%20With%20Custom%20Container.ipynb

from google.cloud import aiplatform
from datetime import datetime
import os
import shutil
import glob
import pkg_resources
from IPython.display import Markdown as md
from google.cloud import service_usage_v1
from google.cloud.devtools import cloudbuild_v1
from google.cloud import artifactregistry_v1
from google.cloud import storage
from google.cloud import bigquery
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import json
import numpy as np
import pandas as pd

aiplatform.init(project=PROJECT_ID, location=REGION)
bq = bigquery.Client()
gcs = storage.Client()
su_client = service_usage_v1.ServiceUsageClient()
ar_client = artifactregistry_v1.ArtifactRegistryClient()
cb_client = cloudbuild_v1.CloudBuildClient()



PROJECT_ID = 'your-project-id'
REGION = 'us-central1'
EXPERIMENT = '08b_gcs'
SERIES = '08'

# source data
BQ_PROJECT = PROJECT_ID
BQ_DATASET = 'fraud'
BQ_TABLE = 'fraud_prepped'

# Resources
TRAIN_COMPUTE = 'n1-standard-4'
DEPLOY_COMPUTE = 'n1-standard-4'

# Model Training
VAR_TARGET = 'Class'
VAR_OMIT = 'transaction_id' # add more variables to the string with space delimiters


## Artifact registry
artifactregistry = su_client.get_service(
    request = service_usage_v1.GetServiceRequest(
        name = f'projects/{PROJECT_ID}/services/artifactregistry.googleapis.com'
    )
).state.name


if artifactregistry == 'DISABLED':
    print(f'Artifact Registry is currently {artifactregistry} for project: {PROJECT_ID}')
    print(f'Trying to Enable...')
    operation = su_client.enable_service(
        request = service_usage_v1.EnableServiceRequest(
            name = f'projects/{PROJECT_ID}/services/artifactregistry.googleapis.com'
        )
    )
    response = operation.result()
    if response.service.state.name == 'ENABLED':
        print(f'Artifact Registry is now enabled for project: {PROJECT_ID}')
    else:
        print(response)
else:
    print(f'Artifact Registry already enabled for project: {PROJECT_ID}')



## Cloud build 
cloudbuild = su_client.get_service(
    request=service_usage_v1.GetServiceRequest(
        name=f'projects/{PROJECT_ID}/services/cloudbuild.googleapis.com'
    )
).state.name


if cloudbuild == 'DISABLED':
    print(f'Cloud Build is currently {cloudbuild} for project: {PROJECT_ID}')
    print(f'Trying to Enable...')
    operation = su_client.enable_service(
        request=service_usage_v1.EnableServiceRequest(
            name=f'projects/{PROJECT_ID}/services/cloudbuild.googleapis.com'
        )
    )
    response = operation.result()
    if response.service.state.name == 'ENABLED':
        print(f'Cloud Build is now enabled for project: {PROJECT_ID}')
    else:
        print(response)
else:
    print(f'Cloud Build already enabled for project: {PROJECT_ID}')
