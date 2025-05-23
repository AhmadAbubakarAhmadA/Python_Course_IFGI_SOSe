# Exercise 6.1
# reading a CSV file and creating a vector layer in QGIS
csv_path = r"C:\Users\User\Desktop\PIQAA\Data for Session 6\standard_land_value_muenster.csv"

# Importing the required libraries
from qgis.core import QgsProject, QgsField, QgsVectorLayer
from PyQt5.QtCore import QVariant
from qgis.core import QgsFeature, QgsGeometry
import csv, sys

# Trying to increase the maximum size of the csv field to avoid errors when reading the files
max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)   # setting the maximum size of the csv field
        break                           # if successful
    except OverflowError:               # to catch the error if the size is too large
        max_int //= 10                  # reduce the size by a factor of 10

# Creating a new vector layer using the uri string
# "polygon" is the geometry type
# "EPSG:25832" is the coordinate reference system (CRS)
# "field=standard_land_value:double" defines a new field called "standard_land_value" of type double
# "field=type:string(50)" defines a new field called "type" of type string with a maximum length of 50 characters
uri = "polygon?crs=EPSG:25832&field=standard_land_value:double&field=type:string(50)&field=district:string(50)"

# Creating a new vector layer
layer = QgsVectorLayer(uri, "temp_standard_land_value_muenster", "memory")

# Adding the layer to the map
QgsProject.instance().addMapLayer(layer)

# Getting access to the layer's data provider
provider = layer.dataProvider()
# Getting access to the layers fields
fields = layer.fields()  # this is a QgsFields object

features = []  # a list to store the features

# setting up to read and parse the csv file
with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
    # ← tell Python it’s semicolon-delimited
    reader = csv.reader(csvfile, delimiter=';')
    # Skip the header row
    next(reader)
    # Loop through each row in the CSV file
    for row in reader:
        raw = row[0]                             
        normalized = raw.strip().strip('"').replace(',', '.')  # to replace the comma with a dot
        value = float(normalized)                      # new standard_land_value               
        type_     = row[1]                             # type
        district  = row[2]                             # district
        geometry  = row[3]                             # WKT format geometry

        # Creating new feature to set its field and geometry
        feature = QgsFeature(fields)
        # Setting the attributes for the feature
        feature.setAttribute("standard_land_value",value)
        feature.setAttribute("type",type_)
        feature.setAttribute("district",district)
        feature.setGeometry(QgsGeometry.fromWkt(geometry))

        # Adding the feature to the list of features
        features.append(feature)

# Using the data provider to add **all** features to the layer
provider.addFeatures(features)
# Updating the layer to reflect the changes
layer.updateExtents()
# Refreshing the layer to show the changes in the map canvas
layer.triggerRepaint()
