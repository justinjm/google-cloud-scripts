from google.cloud import bigquery


dataset_name = 'z_test'

def bq_query_dataset(dataset_name, location='US'):
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

            print("Querying table {} to confirm data loaded...".format(table.table_id))
            for row in query_job:
                print("row_count: {}".format(row[0], row["count"]))

        return query_job
    except Exception as e:
        print('[ ERROR] {}'.format(e))


bq_query_dataset(dataset_name)
