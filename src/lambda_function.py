import os
import io
import csv
import boto3
import logging
import psycopg2
import urllib.parse


s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print(f'event ==== {event}')
    
    object_key = event['Records'][0]['s3']['object']['key']
    bucket_name = 'healthdata-bucket'

    # Call the function to read CSV from S3
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        csv_data = list(csv.reader(io.StringIO(content)))
        print(f'csv_data ==== {csv_data}')
        
        # Insert data into Redshift
        insert_data_to_redshift(csv_data, key)

    except Exception as e:
        print(f"Error reading CSV from S3: {str(e)}")
        logger.error(f"An error occurred: {str(e)}")
        

def insert_data_to_redshift(csv_data, key):
    # Redshift connection parameters
    dbname = os.environ.get('DATABASE')
    user = os.environ.get('USER_NAME')
    password = os.environ.get('PASSWORD')
    host = os.environ.get('HOST')
    port = '5439'
    
    conn_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'"
    
    try:
        conn = psycopg2.connect(conn_string)
        print("Connected to Redshift successfully!")
        
        # Get columns from the CSV data (first row)
        columns = csv_data[0]
        
        # Get table name from the key
        table_name = key.split('.csv')[0] 
        
        # Create table query based on columns in CSV
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(f'{col} VARCHAR(255)' for col in columns)});"
        
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        
        # Prepare INSERT query
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(columns))});"
        
        # Skip the first row (header) and insert remaining rows into Redshift
        with conn.cursor() as cursor:
            for row in csv_data[1:]:
                print(f'row ==== {row}')
                print(f'insert_query ==== {insert_query}')
                cursor.execute(insert_query, row)
                conn.commit()
        
        
        cursor.close()
        conn.close()
        print("Closed Redshift connection successfully!")

    except Exception as e:
        print("Error:", e)
        logger.error(f"Error inserting data into Redshift: {str(e)}")