"""
Cloud storage utilities for reading and uploading data from Azure Storage.
"""

import pandas as pd
from azure.storage.blob import BlobServiceClient


def read_csv_from_azure(connection_string, container_name, blob_name):
    """
    Read a CSV file from Azure Blob Storage.

    connection_string(str): Azure Storage connection string
    container_name(str): Name of the container
    blob_name(str): Name of the blob (file path in the container)

    pandas.DataFrame : DataFrame with the CSV content
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    content = blob_client.download_blob().content_as_bytes()
    return pd.read_csv(pd.compat.StringIO(content.decode('utf-8')))


def upload_csv_to_azure(df, connection_string, container_name, blob_name):
    """
    Upload a DataFrame as CSV to Azure Blob Storage.

    df(pandas.DataFrame): DataFrame to upload
    connection_string(str): Azure Storage connection string
    container_name(str): Name of the container
    blob_name(str): Name of the blob (file path in the container)
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    csv_content = df.to_csv(index=False)
    blob_client.upload_blob(csv_content, overwrite=True)
    print(f"File uploaded to Azure: {container_name}/{blob_name}")