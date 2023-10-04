# https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/use-cases/applying-llms-to-data/bigquery_ml_llm.ipynb

## pre-requ
# %pip install --upgrade --user google-cloud-bigquery-connection google-cloud-aiplatform

from google.cloud import bigquery
from google.cloud import bigquery_connection_v1 as bq_connection
import pandas as pd

pd.set_option('display.max_colwidth', 1000)

PROJECT_ID = "[your-project-id]"
REGION = "US"  
DATASET_ID = "bqml_llm"
CONN_NAME = "bqml_llm_conn"
LLM_MODEL_NAME = "bqml-vertex-llm"


### Create BigQuery Cloud resource connection[¶](https://6e61c7346065dae0-dot-us-east1.notebooks.googleusercontent.com/lab/tree/generative-ai/language/use-cases/applying-llms-to-data/bigquery_ml_llm.ipynb#Create-BigQuery-Cloud-resource-connection)
## You will need to create a [Cloud resource connection](https://cloud.google.com/bigquery/docs/create-cloud-resource-connection) to enable BigQuery to interact with Vertex AI services.
## You may need to first [enable the BigQuery Connection API](https://console.developers.google.com/apis/api/bigqueryconnection.googleapis.com/overview).


client = bq_connection.ConnectionServiceClient()
new_conn_parent = f"projects/{PROJECT_ID}/locations/{REGION}"
exists_conn_parent = f"projects/{PROJECT_ID}/locations/{REGION}/connections/{CONN_NAME}"
cloud_resource_properties = bq_connection.CloudResourceProperties({})

# Try to use an existing connection if one already exists. If not, create a new one.
try:
    request = client.get_connection(
        request=bq_connection.GetConnectionRequest(name=exists_conn_parent)
    )
    CONN_SERVICE_ACCOUNT = f"serviceAccount:{request.cloud_resource.service_account_id}"
except Exception:
    connection = bq_connection.types.Connection(
        {"friendly_name": CONN_NAME, "cloud_resource": cloud_resource_properties}
    )
    request = bq_connection.CreateConnectionRequest(
        {
            "parent": new_conn_parent,
            "connection_id": CONN_NAME,
            "connection": connection,
        }
    )
    response = client.create_connection(request)
    CONN_SERVICE_ACCOUNT = (
        f"serviceAccount:{response.cloud_resource.service_account_id}"
    )
print(CONN_SERVICE_ACCOUNT)

## set service account permissions 
gcloud_serviceusage = f"""
gcloud projects add-iam-policy-binding {PROJECT_ID} --condition=None --no-user-output-enabled --member="{CONN_SERVICE_ACCOUNT}" --role="roles/serviceusage.serviceUsageConsumer"
"""

gcloud_bigquery = f"""
gcloud projects add-iam-policy-binding {PROJECT_ID} --condition=None --no-user-output-enabled --member="{CONN_SERVICE_ACCOUNT}" --role="roles/bigquery.connectionUser"
"""

gcloud_aiplatform = f"""
gcloud projects add-iam-policy-binding {PROJECT_ID} --condition=None --no-user-output-enabled --member="{CONN_SERVICE_ACCOUNT}" --role="roles/aiplatform.user"
"""

print(gcloud_serviceusage)
!$gcloud_serviceusage #execute gcloud script

print(gcloud_bigquery)
!$gcloud_bigquery #execute gcloud script

print(gcloud_aiplatform)
!$gcloud_aiplatform #execute gcloud script


## confirm roles set
# !gcloud projects get-iam-policy $PROJECT_ID  \
#     --flatten="bindings[].members" \
#     --format="table(bindings.role)" \
#     --filter="bindings.members:$CONN_SERVICE_ACCOUNT"

## create dataset
# client = bigquery.Client(project=PROJECT_ID)

# dataset_id = f"""{PROJECT_ID}.{DATASET_ID}"""
# dataset = bigquery.Dataset(dataset_id)
# dataset.location = REGION

# dataset = client.create_dataset(dataset, exists_ok=True)

# print(f"Dataset {dataset.dataset_id} created.")