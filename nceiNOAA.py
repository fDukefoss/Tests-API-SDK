import requests
import time
import csv

def run_nceiNOAA_api_until_100mb():
        """
        Downloads data from NOAA NCEI Access Data Service API until 100MB of data is received.
        Retries on 503 errors with exponential backoff.

        Returns:
            Total time spent fetching 100MB of data.
        """
        dataset = 'daily-summaries'
        stations = ['USC00030006']  # Replace with your desired station IDs
        start_date = '1941-01-01'
        end_date = '2024-12-31'
        data_types = ['TMIN', 'TMAX', 'PRCP', 'SNOW', 'SNWD', 'AWND', 'WDF2', 'WDF5', 'WSF2', 'WSF5', 'PGTM', 'EVAP', 'MDSF', 'DAPR', 'MDPR', 'DSNW', 'DTSN', 'DX32', 'DX70', 'DX90']
        data_format = 'json'  # Options: 'csv', 'json', 'pdf', 'netcdf'
        max_retries = 5
        retry_delay = 5
        base_url = 'https://www.ncei.noaa.gov/access/services/data/v1'
        total_data_mb = 0
        total_time_spent = 0

        while total_data_mb < 50:
            params = {
                'dataset': dataset,
                'stations': ','.join(stations),
                'startDate': start_date,
                'endDate': end_date,
                'dataTypes': ','.join(data_types),
                'format': data_format
            }

            attempt = 0
            while attempt < max_retries:
                try:
                    start_time = time.time()
                    response = requests.get(base_url, params=params)
                    elapsed_time = time.time() - start_time

                    if response.status_code == 503:
                        attempt += 1
                        wait_time = retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                        print(f"⚠️ 503 Error: Service Unavailable. Retrying in {wait_time} seconds... (Attempt {attempt}/{max_retries})")
                        time.sleep(wait_time)
                        continue  # Retry

                    response.raise_for_status()  # Raise other errors (400, 500, etc.)

                    response_size_mb = len(response.content) / (1024 * 1024)  # Convert bytes to MB
                    total_data_mb += response_size_mb
                    total_time_spent += elapsed_time

                    print(f"Response time: {elapsed_time:.2f} seconds")
                    print(f"Response size: {response_size_mb:.2f} MB")
                    print(f"Total data received: {total_data_mb:.2f} MB")

                    break  # Exit retry loop if successful

                except requests.exceptions.RequestException as e:
                    if attempt >= max_retries - 1:
                        print(f"API request failed after {max_retries} attempts: {e}")
                        return None  # Stop if max retries exceeded
                    attempt += 1
                    time.sleep(retry_delay * (2 ** (attempt - 1)))  # Exponential backoff

        return total_time_spent

def run_benchmark():
    """
    Runs the NCEI NOAA API benchmark test 20 times and logs results to a CSV file.
    """
    
    failures = 0
    total_times = []

    # Open CSV file for logging results
    with open('nceiNOAAdata.csv', mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Run', 'Status', 'Time (seconds)', 'Error'])  # Write header

        for i in range(1, 21):
            try:
                print(f"\n📡 Run {i}...")
                total_time = run_nceiNOAA_api_until_100mb()
                
                if total_time is None:
                    raise Exception("Max retries exceeded for 503 errors.")

                total_times.append(total_time)
                print(f"✅ Run {i} completed in {total_time:.2f} seconds")
                csv_writer.writerow([i, 'Success', f"{total_time:.2f}", ''])  # Log success

            except Exception as e:
                failures += 1
                print(f"❌ Run {i} failed with error: {e}")
                csv_writer.writerow([i, 'Failure', '', str(e)])  # Log failure

    # Final Summary
    print("\n📊 Summary:")
    print(f"✅ Total runs: 20")
    print(f"❌ Failures: {failures}")
    if total_times:
        print(f"⏳ Average time for successful runs: {sum(total_times) / len(total_times):.2f} seconds")
    else:
        print("⚠️ No successful runs.")

if __name__ == "__main__":
    run_benchmark()
