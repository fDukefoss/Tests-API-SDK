# Import modules
import copernicusmarine
import time

#doc to create the configuration file
#https://help.marine.copernicus.eu/en/articles/8185007-copernicus-marine-toolbox-credentials-configuration
def run_copernicus_toolbox():
    # Measure the download time
    start_time = time.time()
    copernicusmarine.get(
    dataset_id = "cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m"
    )
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":
    run_copernicus_toolbox()