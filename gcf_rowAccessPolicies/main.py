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
        tableId = call[0]
        # get rowAccessPolicies
        ## set constants
        projectId = "demos-vertex-ai"
        datasetId = "z_test"
        # tableId = "crm_account_rsl"

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
        # print(json.dumps(response.json(), indent=4))

        # append results to replies (output)
        # TODO
        replies.append({
            'rowAccessPolicies': f'{response.json()}'
        })
    return json.dumps({
        'replies': [json.dumps(reply) for reply in replies]
    })
