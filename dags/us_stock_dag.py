from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import os

# CONFIGURATION
STOCK_SYMBOLS = ['NVDA', 'MSFT', 'GOOGL', 'TSLA']
BUCKET_NAME = "wallstreet-data-lake-ananyot"
DATASET_NAME = "wallstreet_warehouse"
TABLE_NAME = "raw_stock_prices"
GCP_CONN_ID = "google_cloud_default"

# PYTHON FUNCTIONS
def extract_stock_data(**kwargs):
    """
    Extracts daily stock data using yfinance library.
    Saves the data locally as CSV file.
    """
    try:
        # Get execution date (logical date) to fetch data for specific day
        # In practice, yfinance fetches history, here we fetch last 1 day for simplicity
        print(f"Fetching data for: {STOCK_SYMBOLS}")

        df_list = []
        for symbol in STOCK_SYMBOLS:
            ticker = yf.Ticker(symbol)
            # Fetch data for the last 1 day
            data = ticker.history(period="1d")
            data.reset_index(inplace=True)
            data['Symbol'] = symbol
            df_list.append(data)

        # Combine all dataframes
        final_df = pd.concat(df_list)

        # Formatting Date
        final_df['Date'] = final_df['Date'].dt.strftime('%Y-%m-%d')

        # Define output path
        file_name = f"stock_data_{datetime.now().strftime('%Y%m%d')}.csv"
        file_path = f"/tmp/{file_name}"

        # Save to CSV
        final_df.to_csv(file_path, index=False)
        print(f"Saved data to {file_path}")

        # Push file name to XCom for next tasks
        return file_name
    
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        raise e
    
# DAG DEFINITION
default_args = {
    'owner': 'Ananyot',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'wallstreet_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    # Task 1: Extract Data
    t0_extract = PythonOperator(
        task_id='extract_stock_data',
        python_callable=extract_stock_data
    )

    # Task 2: Upload to GCS (Data Lake)
    t1_upload_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_to_gcs',
        src='/tmp/{{ ti.xcom_pull(task_ids="extract_stock_data") }}',
        dst='raw/{{ ti.xcom_pull(task_ids="extract_stock_data") }}',
        bucket=BUCKET_NAME,
        gcp_conn_id=GCP_CONN_ID
    )

    # Task 3: Load to BigQuery (Data Warehouse - Raw Layer)
    t2_load_bq = GCSToBigQueryOperator(
        task_id='load_to_bq',
        bucket=BUCKET_NAME,
        source_objects=['raw/{{ ti.xcom_pull(task_ids="extract_stock_data") }}'],
        destination_project_dataset_table=f"{DATASET_NAME}.{TABLE_NAME}",
        schema_fields=[
            {'name': 'Date', 'type': 'DATE'},
            {'name': 'Open', 'type': 'FLOAT'},
            {'name': 'High', 'type': 'FLOAT'},
            {'name': 'Low', 'type': 'FLOAT'},
            {'name': 'Close', 'type': 'FLOAT'},
            {'name': 'Volume', 'type': 'INTEGER'},
            {'name': 'Dividends', 'type': 'FLOAT'},
            {'name': 'Stock_Splits', 'type': 'FLOAT'},
            {'name': 'Symbol', 'type': 'STRING'}
        ],
        write_disposition='WRITE_APPEND',
        source_format='CSV',
        skip_leading_rows=1,
        gcp_conn_id=GCP_CONN_ID
    )

    t0_extract >> t1_upload_gcs >> t2_load_bq