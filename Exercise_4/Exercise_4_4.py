# Exercise 4.4
# Count the number of schools in each district

# Importing the necessary libraries
import processing
from qgis.core import QgsProject

# Setting up the layers
schools_layer   = QgsProject.instance().mapLayersByName('Schools')[0]
districts_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
# Setting  up the parameters
params = {
    'POLYGONS': districts_layer,
    'POINTS':   schools_layer,
    'FIELD':    'school_count',   # name of the new count field
    'OUTPUT':   'memory:'         # keep the result in memory
}
#processing.run('qgis:countpointsinpolygon', params)
result = processing.run('qgis:countpointsinpolygon', params)
out_layer = result['OUTPUT']
for feat in out_layer.getFeatures():
    name  = feat['Name']           # or whatever your district-name field is
    count = feat['school_count']   # the count field you specified
    print(f"{name}: {count}")
