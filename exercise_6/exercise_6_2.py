# Importing the required libraries
from qgis.core import QgsProject, QgsField, QgsVectorLayer
from PyQt5.QtCore import QVariant
from qgis.core import QgsFeature, QgsGeometry

# loading layers needed
# remove the stray leading quote in the layer name
pools     = QgsProject.instance().mapLayersByName('public_swimming_pools')[0]
districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]

# editing the layer
pools.startEditing()

# updating the type field values
identity_type = pools.fields().indexFromName('Type')
for feature in pools.getFeatures():
    value = feature['Type']
    if value == 'H':
        pools.changeAttributeValue(feature.id(), identity_type, 'Hallenbad')
    elif value == 'F':
        pools.changeAttributeValue(feature.id(), identity_type, 'Freibad')

# adding a new field to the layer called "district"
new_field = QgsField('district', QVariant.String, "string", 50) # 50 is the length of the string
pools.dataProvider().addAttributes([new_field]) # adding the field to the layer
pools.updateFields() # updating the layer to show the new field
# getting the index of the new field
identity_district = pools.fields().indexFromName('district')

# now we need to assign each pool to a district
for feature in pools.getFeatures():
    assigned = None
    for district in districts.getFeatures():
        # checking if the pool is in the district
        if district.geometry().contains(feature.geometry()):
            assigned = district['Name'] # get the district name
            break    # if the pool is in a district, stop checking
    # now we write the district value to the pool feature
    if assigned:
        pools.changeAttributeValue(feature.id(), identity_district, assigned)

# saving the changes
pools.commitChanges()

# Display a message to confirm the changes
QMessageBox.information(iface.mainWindow(), "Done", "Swimming pools updated successfully.")

#  refreshing the layer
pools.triggerRepaint()
