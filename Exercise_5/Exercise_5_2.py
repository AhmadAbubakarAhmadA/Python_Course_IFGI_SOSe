from qgis.PyQt.QtWidgets       import QInputDialog, QMessageBox
from qgis.core          import ( QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsPointXY, QgsGeometry)
from qgis.utils                import iface

# Ask the user  to input Coordinates
parent = iface.mainWindow()
SimpleCoordinates, ok = QInputDialog.getText(
    parent,
      "Enter Coordinates", 
      "Enter coordinates as latitude, longitude", text="51.9694,7.5960"
      )

if not ok:
    QMessageBox.warning(parent, "Geoguesser_Game", "User cancelled the input.")
else:
    try:
        latitude_str, longitude_str = [s.strip() for s in SimpleCoordinates.split(",")]
        latitude, longitude = float(latitude_str), float(longitude_str)
    except Exception as e:
        QMessageBox.warning(parent, "Geoguesser_Game", "Invalid input format. Please enter coordinates as latitude, longitude.")
        raise e
    
# Transform the coordinates from WGS84 to the layer CRS
district_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
crs84 = QgsCoordinateReferenceSystem("EPSG:4326") #WGS84
crs_layer = district_layer.crs()       # Etrs89 / UTM zone 32N
transform = QgsCoordinateTransform(crs84, crs_layer, QgsProject.instance()) # creates a coordinate transform object

# Create a point geometry from the coordinates
point_in_wgs84 = QgsPointXY( longitude, latitude)
point_in_layer = transform.transform(point_in_wgs84) 
point_geometry = QgsGeometry.fromPointXY(point_in_layer)

# test if the point is within the district layer
found = None
for feature in district_layer.getFeatures():
    if feature.geometry().contains(point_geometry):
        found = feature['Name']
        break

# Display the result
if found:
    QMessageBox.information(parent, "Geoguesser_Game", f"The coordinates are within the district:\n\n{found}")
else:
    QMessageBox.information(parent, "Geoguesser_Game", f"The coordinates are not within any district.")