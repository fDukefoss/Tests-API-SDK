import requests
import time
import sys
import json

def run_obis_api():
    dataset_id = "8ba043fd-a7c5-4562-a56b-dc1225d03937"

    base_url = "https://api.obis.org/v3/occurrence"

    params = {
        "datasetid": dataset_id,
        "size": 4745,  
        "offset": 0    
    }


    start_time = time.time()


    total_records = 0
    total_data_size = 0  

    while total_data_size < 300:
        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break

        response_size = sys.getsizeof(response.content)  
        total_data_size += response_size / (1024 * 1024)  # Convert to MB

        data = response.json()

        if "results" in data and data["results"]:
            batch_size = len(data["results"])
            total_records += batch_size

            print(f"Fetched {batch_size} records (Total: {total_records}) - Downloaded {total_data_size:.2f} MB")

            params["offset"] += params["size"]
        else:
            print("No more data to fetch.")
            break  

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Query completed in {elapsed_time:.2f} seconds")
    print(f"Total records retrieved: {total_records}")
    print(f"Total data downloaded: {total_data_size:.2f} MB")
    
    return elapsed_time

if __name__ == "__main__":
    print(run_obis_api())