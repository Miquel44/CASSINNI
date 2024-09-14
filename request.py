import scipy
import numpy as np
import cv2
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
    bands=["B02", "B03", "B04", "B08", "B11"],
    max_cloud_cover=30,
)

true_color.download("true_color.tiff")


# Leer el archivo TIFF descargado con las bandas B02 (azul), B03 (verde) y B04 (rojo)
with rasterio.open("true_color.tiff") as src:
    # Leer las bandas
    band_blue = src.read(1)  # B02 - Azul
    band_green = src.read(2)  # B03 - Verde
    band_red = src.read(3)  # B04 - Rojo
    band_nir = src.read(4)  # B08 - NIR
    band_swir = src.read(5)  # B11 - SWIR

# Función para normalizar las bandas (ajustar a 0-1 para visualización)
def normalize(array):
    array_min, array_max = np.nanmin(array), np.nanmax(array)
    return (array - array_min) / (array_max - array_min)

# Normalizar las bandas
band_blue_norm = normalize(band_blue)
band_green_norm = normalize(band_green)
band_red_norm = normalize(band_red)

# Crear una imagen RGB combinando las bandas normalizadas
rgb_image = np.dstack((band_red_norm, band_green_norm, band_blue_norm))

# Calcular ndvi
ndvi = (band_nir - band_red) / (band_nir + band_red)
ndbi = (band_swir - band_nir) / (band_swir + band_nir)
baei = (band_swir / band_red)
ui = (band_nir - band_swir) / (band_nir + band_swir)

# Visualizar la imagen RGB
plt.figure(figsize=(10, 10))
plt.imshow(rgb_image)
plt.title("Imagen RGB (True Color)")
plt.axis('off')
plt.show()

# Guardar la imagen RGB en formato PNG
plt.imsave("imagen_rgb.tiff", rgb_image)


# plt.figure(figsize=(10, 10))
# plt.imshow(ndvi, cmap="RdYlGn")
# plt.title("NDVI")
# plt.colorbar(label="NDVI Value")
# plt.axis('off')
# plt.show()



fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Ajustar el espacio entre subgráficas
plt.subplots_adjust(wspace=0.3, hspace=0.3)

axs[0, 0].imshow(ndvi, cmap='RdYlGn')
axs[0, 0].set_title("NDVI")
axs[0, 0].axis('off')  # Desactivar los ejes

# Mostrar la segunda imagen
axs[0, 1].imshow(ndbi, cmap='RdYlGn')
axs[0, 1].set_title("NDBI")
axs[0, 1].axis('off')  # Desactivar los ejes

# Mostrar la tercera imagen
axs[1, 0].imshow(baei, cmap='RdYlGn')
axs[1, 0].set_title("BAEI")
axs[1, 0].axis('off')  # Desactivar los ejes

# Mostrar la cuarta imagen
axs[1, 1].imshow(ui, cmap='RdYlGn')
axs[1, 1].set_title("UI")
axs[1, 1].axis('off')  # Desactivar los ejes

# Mostrar la figura
plt.show()

# Guardar la imagen de NDVI como PNG
plt.imsave("ndvi_image.tiff", ndvi, cmap="RdYlGn")


