import scipy
import numpy as np
import openeo

from openeo.extra.spectral_indices import compute_indices

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as mpatches
import rasterio
from rasterio.plot import show

connection = openeo.connect("openeo.dataspace.copernicus.eu").authenticate_oidc()

extent = {"west": 2.06341, "south": 41.55454, "east": 2.07341, "north": 41.56454}

true_color = connection.load_collection(
    "SENTINEL2_L1C",
    temporal_extent=["2024-09-13", "2024-09-13"],
    spatial_extent=extent,
    bands=["B02", "B03", "B04", "B08"],
    max_cloud_cover=30,
)

true_color.download("true_color.tiff")

with rasterio.open("true_color.tiff") as src:
    band_blue = src.read(1)
    band_green = src.read(2)
    band_red = src.read(3)
    band_nir = src.read(4)

def normalize(array):
    array_min, array_max = np.nanmin(array), np.nanmax(array)
    return (array - array_min) / (array_max - array_min)

band_blue_norm = normalize(band_blue)
band_green_norm = normalize(band_green)
band_red_norm = normalize(band_red)

rgb_image = np.dstack((band_red_norm, band_green_norm, band_blue_norm))

ndvi = (band_nir - band_red) / (band_nir + band_red)

plt.figure(figsize=(10, 10))
plt.imshow(rgb_image)
plt.title("Imagen RGB (True Color)")
plt.axis('off')
plt.show()

plt.imsave("imagen_rgb.tiff", rgb_image)

plt.figure(figsize=(10, 10))
plt.imshow(ndvi, cmap="RdYlGn")
plt.title("NDVI")
plt.colorbar(label="NDVI Value")
plt.axis('off')
plt.show()

plt.imsave("ndvi_image.tiff", ndvi, cmap="RdYlGn")
plt.imsave("ndvi_image2.tiff", ndvi, cmap="RdYlGn")
def Corridor_checker(filtered_image,threshold1,threshold2):

    mask = np.logical_or(filtered_image <= threshold1, filtered_image >= threshold2)

    rgb_ndvi = np.zeros((filtered_image.shape[0], filtered_image.shape[1], 3))

    rgb_ndvi[..., 0] = np.where(filtered_image <= threshold1, 1, 0)

    rgb_ndvi[..., 1] = np.where(filtered_image >= threshold2, 1, 0)

    rgb_ndvi[~mask] = 1

    # Display the image
    plt.figure(figsize=(10, 10))
    plt.imshow(rgb_ndvi)
    plt.title("filtered_image Urban vs Vegetation")
    plt.axis('off')
    plt.show()
    plt.imsave("Miquel_nvdi.tiff", rgb_ndvi)
Corridor_checker(ndvi,0.3,0.5)