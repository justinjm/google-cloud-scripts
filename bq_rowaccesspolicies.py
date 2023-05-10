import requests
from google.auth import default
from google.auth.transport.requests import Request
import json

projectId = "demos-vertex-ai"
datasetId = "z_test"
tableId = "crm_account_rsl"

# Set the URL for the BigQuery API endpoint
url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"

# Use the default credentials to obtain an access token
creds, _ = default(scopes=["https://www.googleapis.com/auth/bigquery"])
creds.refresh(Request())

# Set the authorization header using the access token
headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}

# Send the query using the requests module
response = requests.get(url, headers=headers)

# Print the response
print(json.dumps(response.json(), indent=4))

# as of 2023-05-10 - not able to view row-level access policies within BQ UI programmatically 
# https://cloud.google.com/bigquery/docs/managing-row-level-security#create_or_update_a_row-level_access_policy
# https://cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list
# https://towardsdatascience.com/remote-functions-in-bigquery-af9921498438
