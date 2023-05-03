from google.cloud import bigquery
from google.cloud import storage


# set constants
bucket_name = 'your-bucket-name'
file_names = ['file_1.csv', 'file_2.csv']
dataset_name = 'z_test'

# define function
def load_csv_to_bigquery(bucket_name, file_names, dataset_name):
    """Load CSV files from Google Cloud Storage to their own BigQuery tables."""
    # Create a BigQuery client
    client = bigquery.Client()

    # Create the dataset if it doesn't exist
    dataset_ref = client.dataset(dataset_name)
    dataset = bigquery.Dataset(dataset_ref)
    try:
        dataset = client.create_dataset(dataset)
    except:
        pass

    # Load each CSV file to its own BigQuery table
    for file_name in file_names:
        # Create the table name from the file name
        table_name = file_name.split('.')[0]
        # ensure safe names - replace "." with _ and "-" with "_"
        table_name = table_name.replace(".", "_").replace("-", "_")

        # Create the table schema from the first row of the CSV file
        bucket = storage.Client().get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        first_row = blob.download_as_string().split(b'\n')[0].decode('utf-8')
        # ensure safe names - replace "." and " " with "_"
        first_row = first_row.replace(".", "_").replace(" ", "_")

        schema = [bigquery.SchemaField(field_name, 'STRING')
                  for field_name in first_row.split(',')]

        # Create the table if it doesn't exist
        table_ref = dataset_ref.table(table_name)
        table = bigquery.Table(table_ref, schema=schema)
        try:
            table = client.create_table(table)
        except:
            pass

        # Load the CSV file to the table
        uri = f'gs://{bucket_name}/{file_name}'
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        load_job = client.load_table_from_uri(
            uri, table_ref, job_config=job_config)
        load_job.result()

        print(f'File {file_name} loaded to table {table_name}.')


def bq_check_rows(dataset_name, location='US'):
    """Query all tables in a BigQuery dataset to check results"""
    try:
        client = bigquery.Client()

        # Get the list of tables in the dataset
        tables = client.list_tables(dataset_name)

        # Loop through the tables and query each one
        for table in tables:
            query = """SELECT COUNT(*) AS count FROM `{}.{}`""".format(
                dataset_name, table.table_id)
            query_job = client.query(query, location=location)

            print("Querying table {}".format(table.table_id))
            for row in query_job:
                print("row_count: {}".format(row[0], row["count"]))

        return query_job
    except Exception as e:
        print('[ ERROR] {}'.format(e))


# run ingestion
load_csv_to_bigquery(bucket_name, file_names, dataset_name)

# run queries to check 
bq_check_rows(dataset_name)


