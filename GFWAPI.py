import requests
import time  # Import the time module

def run_GFWAPI():
    # Replace with your actual GFW API key
    API_KEY = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9.eyJkYXRhIjp7ImZpcnN0TmFtZSI6IkZyaWtrIiwibGFzdE5hbWUiOiJEdWtlZm9zcyIsImVtYWlsIjoiRnJpa2suZHVrZWZvc3NAZ21haWwuY29tIiwicGhvdG8iOm51bGwsImxhbmd1YWdlIjoiZW4iLCJpZCI6NDQzMTksInR5cGUiOiJ1c2VyIn0sImlhdCI6MTc0MzQyMTMyOCwiZXhwIjoxNzQzNDIzMTI4LCJhdWQiOiJnZnciLCJpc3MiOiJnZncifQ.KOED7wuLmdeH1vpyDwnu5dvsqwUjC3AuAy-ER7DYdVMesMiOFvEZZYVt1k8xm-tKgN8SBZOa1mkAfk7el3atMOV-_pfJpd5470sID271343M5sJ2BpjAXZAOfbbEM4NbG7MMN_OwZPTKvL0PgOSrdpOijTV41fFbS94XEuYxGbRe3YhV3SoJGM5vVoP8l9bw4VQtLAL-7rZwKfdbfkk7ymmtG2l48kd233T1iycJy1pJkA-Lw4khezzekiVyN-qieImGn_cFBWu6i9pJHX6H9zDPQMh1nUfe5SJmBK-NivybQePM8SUNnml3ZNPvyAqCkX5i6zNeSciGlhB7HIPakonc7JP3WZqhx_iOfzEfbqqaB2ZA4ddjs5RkdxWjP-hQ8ThZzwYSY7U2UZOcOobfhDKjvPitG5wTmIoXxOiU9vpZJxKeeTCprH1-FAMkH1MbYdcezr9m93oFiV-HNLqmQ2158-VVXpf7t_WmduURY2U0eRCgUow3xRdaEYzcJE1m'

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