import json
import requests
from google.auth import default
from google.auth.transport.requests import Request


def get_row_access_polices(request):
    request_json = request.get_json(silent=True)
    replies = []
    calls = request_json['calls']
    for call in calls:
        # set tableId as variable for passing into rowAccessPolicies API call
        projectId = call[0]
        datasetId = call[1]
        tableId = call[2]

        # get rowAccessPolicies
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

        # append results to replies (output)
        replies.append(response.json())

    return json.dumps({
        'replies': [json.dumps(reply) for reply in replies]
    })
