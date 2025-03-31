import pandas as pd
import time  # Added for timing
from odp.client import OdpClient
from odp.dto import MetadataDto
from odp.dto.catalog import DatasetDto, DatasetSpec
from odp.dto.common.contact_info import ContactInfo  


def run_hubocean_sdk():
    dataset_uuid = 'ab673425-b205-4e00-aeaf-4271adf6756e'
    client = OdpClient()
    # Start timing
    start_time = time.time()

    # Getting Tabular dataset whose data we want to see
    my_dataset = client.catalog.get(dataset_uuid)

    # OQS filter
    filter_query = {}

    limit = 190000

    # Fetch data
    data = client.tabular.select_as_stream(my_dataset, filter_query, limit)
    data_list = list(data)  # Force full data retrieval
    print(len(data_list))
    # End timing
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time

    # Calculate size of the data in MB
    data_size_mb = sum(len(str(row)) for row in data_list) / (1024 * 1024)  # Approximate size in MB

    print(f"Time taken to fetch data: {elapsed_time:.2f} seconds")
    print(f"Size of the data retrieved: {data_size_mb:.2f} MB")

    return elapsed_time

if __name__ == "__main__":
    run_hubocean_sdk()