import requests
import time  # Import the time module

def run_GFWAPI():
    # Replace with your actual GFW API key
    API_KEY = ''

    # Define the API endpoint and parameters
    url = "https://gateway.api.globalfishingwatch.org/v3/download/datasets/public-fishing-effort-v1-v2-archived/download/mmsi-daily-csvs-10-v2-2016.zip"

    # Set the headers
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Start timing
    start_time = time.time()

    # Make the first API request
    response = requests.get(url, headers=headers)

    # Check if the first request was successful
    if response.status_code == 200:
        # Parse the response to extract the 'url'
        try:
            response_data = response.json()
            download_url = response_data.get('url')
            if not download_url:
                print("Error: 'url' not found in the response.")
            else:
                # Make the second API request to the extracted URL
                response = requests.get(download_url, headers=headers)
                if response.status_code == 200:
                    # Get and print the size of the response in MB
                    response_size_mb = len(response.content) / (1024 * 1024)
                    print(f"Size of the response: {response_size_mb:.2f} MB")
                else:
                    print(f"Second request failed with status code {response.status_code}: {response.text}")
        except ValueError:
            print("Error: Failed to parse JSON response.")
    else:
        print(f"First request failed with status code {response.status_code}: {response.text}")

    # End timing
    end_time = time.time()

    # Print the total time taken
    total_time = end_time - start_time
    return total_time

if __name__ == "__main__":
    print(run_GFWAPI())