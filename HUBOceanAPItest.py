import requests
import json
import time

def run_hubocean_api():
    dataset_uuid = "ab673425-b205-4e00-aeaf-4271adf6756e"

    API_KEY = ""

    # Headers for authentication
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    params = {
        'limit': 120,
    }

    url = f"https://api.hubocean.earth/data/{dataset_uuid}/list"

    total_size = 0  # Initialize total size
    target_size = 300 * 1024 * 1024  # 300 MB in bytes
    start_time = time.time()  # Start timing the entire process

    while total_size < target_size:
        request_start_time = time.time()  # Start timing the request
        response = requests.post(url, headers=HEADERS, params=params)
        request_elapsed_time = time.time() - request_start_time  # Calculate elapsed time for the request
        if response.status_code == 200:
            try:
                response_size = len(response.content)  # Get size of the response in bytes
                total_size += response_size
                response_size_mb = response_size / (1024 * 1024)  # Convert to MB
                total_size_mb = total_size / (1024 * 1024)  # Convert to MB
                print(f"Response size: {response_size_mb:.2f} MB, Total size: {total_size_mb:.2f} MB")
            except Exception as e:
                print(f"Error processing response: {e}")
                break
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}, Response text: {response.text}")
            break

        print(f"Time taken for the request: {request_elapsed_time:.2f} seconds")

    total_elapsed_time = time.time() - start_time  # Calculate total elapsed time
    print(f"Total size of responses: {total_size / (1024 * 1024):.2f} MB")
    print(f"Total time taken to fetch 300 MB: {total_elapsed_time:.2f} seconds")

    return total_elapsed_time

if __name__ == "__main__":
    run_hubocean_api()
