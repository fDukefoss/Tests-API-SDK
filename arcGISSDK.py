from arcgis.gis import GIS
import time
import json

def run_arcgis_sdk():
    
    # Authenticate with ArcGIS Online (Replace with real credentials)
    gis = GIS("https://www.arcgis.com", "username", "password")

    # 📌 The dataset Item ID (311 Service Requests)
    item_id = '46a685dd1b284ff2a3bf68e062051635'
    start_time = time.time()

    # Get the dataset item
    item = gis.content.get(item_id)

    #  Check if the dataset contains tables
    if item.tables:
        print("✅ Found a table, attempting to download...")

        # Access the first table
        table = item.tables[0]

        #  Query the table (without `as_df=True`)
        features = table.query(where='1=1', out_fields='*')

        # Calculate data size
        data_size_bytes = sum(len(json.dumps(f.attributes)) for f in features.features)
        data_size_mb = data_size_bytes / (1024 * 1024)
        print(f"Data fetched: {data_size_mb:.2f} MB")

    else:
        print("No tables found in this dataset. It may not be queryable.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"⏳ Total execution time: {elapsed_time:.2f} seconds")
    return elapsed_time

if __name__ == "__main__":
    print(run_arcgis_sdk())
