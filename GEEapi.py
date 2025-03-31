import time
import ee
import requests
import os

def run_gee_api():
    # Authenticate and initialize GEE
    ee.Authenticate()
    ee.Initialize(project='testapi-453521')

    # Select a dataset (e.g., Sentinel-2 imagery)
    dataset = ee.ImageCollection("COPERNICUS/S2") \
        .filterDate("2023-01-01", "2023-01-31") \
        .filterBounds(ee.Geometry.Point([-122.335, 37.792])) \
        .sort("CLOUDY_PIXEL_PERCENTAGE", False) \
        .first()  # Get the best image

    tiles = [
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1]),
        ee.Geometry.Rectangle([-123.0, 37.0, -122.15, 37.1])
    ]

    # Folder to save downloaded images
    output_folder = "GEE_Downloads"
    os.makedirs(output_folder, exist_ok=True)

    # Start timing after authentication & search
    start_time = time.time()
    total_download_size = 0  # Track total downloaded size in MB

    # Download each tile
    for i, tile in enumerate(tiles):
        try:
            # Generate direct download URL
            url = dataset.getDownloadURL({
                "scale": 30,  # 30m resolution
                "region": tile.getInfo()
            })

            print(f"Downloading Tile {i+1}...")

            # Start timing download
            tile_start_time = time.time()

            # Use requests to download the file
            response = requests.get(url, stream=True)
            output_file = os.path.join(output_folder, f"tile_{i+1}.tif")

            # Get file size from response headers (in bytes)
            file_size_bytes = int(response.headers.get("Content-Length", 0))
            file_size_mb = file_size_bytes / (1024 * 1024)
            total_download_size += file_size_mb

            # Stop timing for this tile
            tile_end_time = time.time()
            tile_elapsed_time = tile_end_time - tile_start_time

            print(f"Tile {i+1} downloaded: {output_file} ({file_size_mb:.2f} MB) in {tile_elapsed_time:.2f} seconds.")

        except Exception as e:
            print(f" Failed to download Tile {i+1}: {e}")

    # Stop total timing
    end_time = time.time()
    total_elapsed_time = end_time - start_time

    print("\nAll downloads completed!")
    print(f"Total size of downloaded files: {total_download_size:.2f} MB")
    print(f"Total execution time (after search): {total_elapsed_time:.2f} seconds")
    
    return total_elapsed_time

if __name__ == "__main__":
    print(run_gee_api())