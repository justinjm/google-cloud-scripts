import requests
from google.auth import default
from google.auth.transport.requests import Request

projectId = "demos-vertex-ai"

# Set the URL for the BigQuery API endpoint
url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/queries"

# Use the default credentials to obtain an access token
creds, _ = default(scopes=["https://www.googleapis.com/auth/bigquery"])
creds.refresh(Request())

# Set the authorization header using the access token
headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}

# Set the query
query = """
#standardSQL
SELECT * FROM `bigquery-public-data.samples.natality`
LIMIT 100
"""

# Send the query using the requests module
response = requests.post(url, headers=headers, json={"query": query})

# Print the response
print(response.json())
