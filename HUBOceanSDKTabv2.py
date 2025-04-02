import pandas as pd
import time  # Added for timing
from odp.client import OdpClient
from odp.dto import MetadataDto
from odp.dto.catalog import DatasetDto, DatasetSpec
from odp.dto.common.contact_info import ContactInfo  


def run_hubocean_sdktabv2():
    dataset_uuid = 'ab673425-b205-4e00-aeaf-4271adf6756e'
    client = OdpClient()
    # Start timing
    start_time = time.time()
    # Getting Tabular dataset whose data we want to see
    my_dataset = client.catalog.get(dataset_uuid)
    # Fetch data
    tab = client.table_v2(my_dataset)
    ct = 0
    for batch in tab.select().batches():
        ct += batch.num_rows
    print(ct)
    # End timing
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time

    # Calculate size of the data in MB
    print(ct.__sizeof__())

    print(f"Time taken to fetch data: {elapsed_time:.2f} seconds")

    return elapsed_time

if __name__ == "__main__":
    run_hubocean_sdktabv2()