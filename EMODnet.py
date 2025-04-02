import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def get_depth_line(longitude_start, longitude_end, latitude, base_url):
    """
    Retrieves depth information along a line of constant latitude from the EMODnet Bathymetry REST service.
    """
    wkt_linestring = f'LINESTRING({longitude_start} {latitude}, {longitude_end} {latitude})'
    params = {'geom': wkt_linestring}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json(), len(response.content) / (1024 * 1024)  # Depth profile and size in MBs

def frange(start, stop, step):
    """
    A range function for floating-point numbers.
    """
    while start < stop:
        yield start
        start += step

def process_latitude(lat, lon_min, lon_max, base_url, total_data_size_mb, data_limit_mb):
    """
    Processes a single latitude to retrieve depth data.
    """
    if total_data_size_mb[0] >= data_limit_mb:
        return None
    depth_profile, response_size_mb = get_depth_line(lon_min, lon_max, lat, base_url)
    total_data_size_mb[0] += response_size_mb
    return {'Latitude': lat, 'LongitudeStart': lon_min, 'LongitudeEnd': lon_max, 'DepthProfile': depth_profile, 'ResponseSizeMB': response_size_mb}

def gather_depth_data():
    """
    Gathers depth data for a predefined square area by retrieving line depths per latitude until the total response size reaches the specified limit.
    Uses concurrency for faster data retrieval.

    Returns:
        pd.DataFrame: DataFrame containing lat, lon_start, lon_end, depth values, and total data size in MBs.
    """
    lon_min, lon_max = -90.0, 90.0   # Longitude range
    lat_min, lat_max = -90.0, 90.0   # Latitude range
    step = 0.005                     # Step size (smaller = more data points)
    data_limit_mb = 100              # Stop after gathering 100MB of data
    base_url = 'https://rest.emodnet-bathymetry.eu/depth_profile'

    latitudes = [round(lat, 6) for lat in frange(lat_min, lat_max, step)]
    depth_data = []
    total_data_size_mb = [0]  # Use a list to allow modification inside process_latitude

    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda lat: process_latitude(lat, lon_min, lon_max, base_url, total_data_size_mb, data_limit_mb), latitudes)

    for result in results:
        if result:
            depth_data.append(result)
        if total_data_size_mb[0] >= data_limit_mb:
            break

    return pd.DataFrame(depth_data)

if __name__ == "__main__":
    depth_df = gather_depth_data()

