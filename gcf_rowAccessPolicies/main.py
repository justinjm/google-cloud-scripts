import json


def get_row_access_polices(request):
    request_json = request.get_json(silent=True)
    replies = []
    calls = request_json['calls']
    for call in calls:
        # set tableId as variable for passing into rowAccessPolicies API cal

        table_name = call[0]

        # get rowAccessPolicies
        # TODO - add logic here

        # append results to replies (output)
        # TODO
        replies.append({
            'table_name': f'{table_name}'
        })
    return json.dumps({
        'replies': [json.dumps(reply) for reply in replies]
    })
