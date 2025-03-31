import concurrent.futures
import time
import os
import json
import csv

# Import the API functions
from arcGISAPI import run_arcgis_api
from GEEapi import run_gee_api
from OBISAPItest import run_obis_api
from PlanetaryComputerAPI import run_planetary_computer_api
from arcGISSDK import run_arcgis_sdk
from CopernicusAPI import run_copernicus_toolbox
from HUBOceanAPItest import run_hubocean_api
from HUBOceanSDK import run_hubocean_sdk
from GFWAPI import run_GFWAPI

def log_results(api_name, duration, error=None):
    log_entry = {
        "api_name": api_name,
        "duration": duration,
        "error": str(error) if error else None
    }
    log_file = 'concurrency_test_log.json'
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append(log_entry)

    with open(log_file, 'w') as file:
        json.dump(logs, file, indent=4)

def test_concurrency(api_name, api_function, num_concurrent_downloads):
    durations = []
    failures = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(api_function) for _ in range(num_concurrent_downloads)]
        for future in concurrent.futures.as_completed(futures):
            try:
                duration = future.result()
                durations.append(duration)
                log_results(api_name, duration)
                print(f"{api_name} completed in {duration:.2f} seconds")
            except Exception as e:
                failures += 1
                log_results(api_name, 0, error=e)
                print(f"{api_name} failed with error: {e}")
    return durations, failures

def main():
    apis = [
        (run_hubocean_api, "HUB Ocean API"),
        (run_arcgis_api, "ArcGIS API"),
        (run_gee_api, "GEE API"),
        (run_obis_api, "OBIS API"),
        (run_planetary_computer_api, "Planetary Computer API"),
        (run_arcgis_sdk, "ArcGIS SDK"),
        (run_copernicus_toolbox, "Copernicus Toolbox"),
        (run_hubocean_sdk, "HUB Ocean SDK")
        (run_GFWAPI, "GFW API"),
    ]

    num_concurrent_downloads = 5  # Number of concurrent downloads to simulate
    results = {}

    # Open CSV file once and write incrementally
    with open("concurrency_test_results.csv", "w", newline="") as csvfile:
        fieldnames = ["API Name", "Download", "Duration (seconds)", "Failures"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for api_function, api_name in apis:
            durations, failures = test_concurrency(api_name, api_function, num_concurrent_downloads)
            results[api_name] = {
                "durations": durations,
                "failures": failures
            }

            # Write results for this API incrementally
            for i, duration in enumerate(durations):
                writer.writerow({
                    "API Name": api_name,
                    "Download": i+1,
                    "Duration (seconds)": duration,
                    "Failures": failures
                })

    print("\nConcurrency Test Results:")
    for api_name, result in results.items():
        print(f"\n{api_name}:")
        print(f"  Durations: {result['durations']}")
        print(f"  Failures: {result['failures']}")

if __name__ == "__main__":
    main()
