import requests
import json
import time


def run_arcgis_api():
    start_time = time.time()    
    # Define the Feature Layer REST API URL (Replace with your own dataset URL)
    feature_layer_url = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/1/query"

    # Define query parameters
    params = {
        "where": "1=1",  # Get all features (modify for filtering)
        "outFields": "*",  # Get all fields
        "f": "json"  # Request data as GeoJSON (or use 'json' for raw JSON)
    }

    total_data_size = 0

    while total_data_size < 300:
        # Send request
        response = requests.get(feature_layer_url, params=params)

        # Check response
        if response.status_code == 200:
            data = response.json()

            # Calculate JSON data size
            data_size_bytes = len(json.dumps(data))
            data_size_mb = data_size_bytes / (1024 * 1024)
            total_data_size += data_size_mb
            end_time = time.time()


            print(f"Data fetched: {data_size_mb:.2f} MB (Total: {total_data_size:.2f} MB)")
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break

    return end_time - start_time

if __name__ == "__main__":
    print(run_arcgis_api())