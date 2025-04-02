import time
import traceback
import csv
import signal

# Import the functions from the other scripts
from arcGISAPI import run_arcgis_api
from GEEapi import run_gee_api
from OBISAPItest import run_obis_api
from PlanetaryComputerAPI import run_planetary_computer_api
from arcGISSDK import run_arcgis_sdk
from CopernicusAPI import run_copernicus_toolbox
from HUBOceanAPItest import run_hubocean_api
from HUBOceanSDK import run_hubocean_sdk    
from GFWAPI import run_GFWAPI
from HUBOceanSDKTabv2 import run_hubocean_sdktabv2

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def test_api(api_function, api_name, iterations=5):
    times = []
    failures = 0

    for i in range(iterations):
        try:
            print(f"Running {api_name} - Iteration {i+1}")
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(300)  # Set the timeout to 5 minutes (300 seconds)
            start_time = time.time()
            elapsed_time = api_function()
            end_time = time.time()
            signal.alarm(0)  # Disable the alarm
            times.append(elapsed_time)
            print(f"{api_name} - Iteration {i+1} completed in {elapsed_time:.2f} seconds")
        except TimeoutException:
            failures += 1
            print(f" {api_name} - Iteration {i+1} failed: Timeout after 5 minutes")
        except Exception as e:
            failures += 1
            print(f" {api_name} - Iteration {i+1} failed: {e}")
            traceback.print_exc()

    return times, failures

def main():
    apis = [
        (run_arcgis_api, "ArcGIS API"),
        (run_gee_api, "GEE API"),
        (run_obis_api, "OBIS API"),
        (run_planetary_computer_api, "Planetary Computer API"),
        (run_arcgis_sdk, "ArcGIS SDK"),
        (run_copernicus_toolbox, "Copernicus Toolbox"),
        (run_hubocean_api, "HUB Ocean API"),
        (run_hubocean_sdk, "HUB Ocean SDK"),
        (run_GFWAPI, "GFW API"),
        (run_hubocean_sdktabv2, "HUB Ocean SDK Tab v2")
        
    ]

    results = {api_name: {"times": [], "failures": 0} for _, api_name in apis}
    total_start_time = time.time()  # Start measuring total time
    iterations = 20

    # Open CSV file once and write incrementally
    with open("api_test_results.csv", "w", newline="") as csvfile:
        fieldnames = ["API Name", "Iteration", "Time (seconds)", "Failures"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(iterations):
            print(f"\nStarting iteration {i+1} of {iterations}")
            for api_function, api_name in apis:
                times, failures = test_api(api_function, api_name, 1)
                results[api_name]["times"].extend(times)
                results[api_name]["failures"] += failures

                # Write results for this iteration
                for timePer in times:
                    writer.writerow({
                        "API Name": api_name,
                        "Iteration": i+1,
                        "Time (seconds)": timePer,
                        "Failures": results[api_name]["failures"]
                    })

    total_end_time = time.time()  # End measuring total time
    total_elapsed_time = total_end_time - total_start_time
    print(f"\nTotal time spent running all tests: {total_elapsed_time:.2f} seconds")

    print("\nTest Results:")
    for api_name, result in results.items():
        print(f"\n{api_name}:")
        print(f"  Times: {result['times']}")
        print(f"  Failures: {result['failures']}")

if __name__ == "__main__":
    main()
