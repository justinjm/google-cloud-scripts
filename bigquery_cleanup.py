from google.cloud import bigquery

# Replace with your project ID and the list of dataset IDs to delete
project_id = 'your-project-id'
dataset_ids_to_delete = ['dataset2', 'dataset2']

# Create a BigQuery client object
client = bigquery.Client(project=project_id)

# Loop through each dataset ID to delete
for dataset_id in dataset_ids_to_delete:
    # Construct the full dataset ID
    dataset_ref = client.dataset(dataset_id)

    # Delete the dataset and its underlying tables
    client.delete_dataset(dataset_ref, delete_contents=True)

    print(f'Deleted dataset {dataset_id} and its contents.')
