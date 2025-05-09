import os
import sys
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsProject
)

# Configuring the QGIS install path 
QGIS_PREFIX = r"C:\OSGeo4W\apps\qgis" 

# Staring up QGIS’s resources
# False = no GUI; if you need to show maps in a window, set True
qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX, True)
qgs.initQgis()

# setting up Paths for data and project read and write
data_folder  = r"C:\Users\User\Desktop\PIQAA\Muenster"
project_path = r"C:\Users\User\Desktop\PIQAA\myFirstProject.qgs"

# Iterating all .shp files
shp_files = [
    os.path.join(data_folder, fn)
    for fn in os.listdir(data_folder)
    if fn.lower().endswith(".shp")
]

# start up a fresh project
project = QgsProject.instance()
project.clear()

# Load each shapefile
for shp in shp_files:
    layer_name = os.path.splitext(os.path.basename(shp))[0]
    layer = QgsVectorLayer(shp, layer_name, "ogr")
    if not layer.isValid():
        print(f" Failed to load {layer_name}")
        continue
    project.addMapLayer(layer)
    print(f" Loaded {layer_name}")

# Save the project
if project.write(project_path):
    print(f" Project saved to {project_path}")
else:
    print("  Failed to save project")

# Clean up QGIS
qgs.exitQgis()
