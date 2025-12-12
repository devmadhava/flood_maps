import rasterio
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

def copy_raster_crs (output_file, input_file):
    with rasterio.open(input_file) as src:
      data = src.read(1)
      out_meta = src.meta.copy()
    with rasterio.open(output_file, 'w', **out_meta) as dst:
      dst.write(data, 1)

def copy_vector_crs (output_file, input_file):
  gdf_source = gpd.read_file(input_file)
  gdf_new = gdf_source[gdf_source['attribute'] == 'value'].copy()
  gdf_new.crs = gdf_source.crs
  # gdf_new = gdf_new.to_crs("EPSG:4326")
  # Save the new GeoDataFrame with the correct CRS
  gdf_new.to_file(output_file)

def calc_raster_percentile(path, percentile=95):
    with rasterio.open(path) as r:
        arr = r.read(1, masked=True)

    return float(np.percentile(arr.compressed(), percentile))

def plot_vector(input_path, title):
    gdf = gpd.read_file(input_path)
    plt.figure(figsize=(8, 8))
    gdf.plot(edgecolor="black", facecolor="red", linewidth=0.5)
    plt.title(title)
    plt.grid(True)
    plt.show()
    
def validate_path(dir):
    if not os.path.exists(dir):
      return os.makedirs(dir, exist_ok=True)
