import time
import planetary_computer
import pystac_client
import requests

def run_planetary_computer_api():
    # Initialize the STAC API client
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    # Define search parameters for GNATSgo Rasters dataset
    search = catalog.search(
        collections=["gnatsgo-rasters"],  # Dataset collection ID
        datetime="2020-07-01/2020-07-01",  # Example date range
    )

    # Retrieve matching items
    items = list(search.get_items())

    start_time = time.time()

    if not items:
        print("No items found for the given search parameters.")
    else:
        # Select the first item
        item = items[0]
        
        asset_key = "tk20_50a"  
        total_mb = 0

        while total_mb < 300:
            if asset_key in item.assets:
                asset = item.assets[asset_key]

                # Sign the asset URL for access
                signed_href = planetary_computer.sign(asset.href)

                # Download the asset
                session = requests.Session()
                response = session.get(signed_href, stream=True)

                # Get file size from response headers
                file_size_bytes = int(response.headers.get("Content-Length", 0))
                file_size_mb = file_size_bytes / (1024 * 1024)
                total_mb += file_size_mb

                print(f"✅ Asset downloaded: ({file_size_mb:.2f} MB) (Total: {total_mb:.2f} MB)")

                if response.status_code != 200:
                    print(f"Failed to download asset. Status code: {response.status_code}")
                    break
            else:
                print("No valid asset found in the dataset.")
                break

    # Stop total timing
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\nScript execution completed.")
    print(f"Total size of downloaded files: {total_mb:.2f} MB")
    print(f"Total execution time (after search): {elapsed_time:.2f} seconds")
    
    return elapsed_time

if __name__ == "__main__":
    print(run_planetary_computer_api())