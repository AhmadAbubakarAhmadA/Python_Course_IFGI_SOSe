#Exercise 5.1 - Find schools in a district
# The Task is to find schools in a selected district and calculates the distance from the district centroid to each school.

# Importing necessary modules
from qgis.PyQt.QtWidgets import QInputDialog, QMessageBox
from qgis.core import QgsProject, QgsVectorLayer, QgsPointXY, QgsFeatureRequest, QgsDistanceArea
from qgis.utils import iface

# first thing is to get the layers ready
districts_Layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
schools_Layer   = QgsProject.instance().mapLayersByName("Schools")[0]

# Now we Extract district names to build a sorted list
names = [features["Name"] for features in districts_Layer.getFeatures()]
names.sort()

# Now we ask the user to select a district
parent = iface.mainWindow()
sDistrict, ok = QInputDialog.getItem(parent, "Select a district", "Districts:", names, editable=False)

# this handles the case when the user cancels the dialog
if not ok:
    QMessageBox.warning(parent, "schools", "user cancelled the dialog")
else:
    # Now we select the district
    exp = f"\"Name\" = '{sDistrict}'" # this builds a QGIS expression 
    districts_Layer.selectByExpression(exp, QgsVectorLayer.SetSelection)
    # zoom to selected features
    iface.mapCanvas().zoomToSelected()

    # NoW Find the selected districts geometry and centroid
    selected = districts_Layer.selectedFeatures()
    district_geometry = selected[0].geometry()
    district_centroid = district_geometry.centroid().asPoint()

    # Filter schools within the selected district
    request = QgsFeatureRequest().setFilterRect(district_geometry.boundingBox())
    inside = [
        feature for feature in schools_Layer.getFeatures(request)
        if district_geometry.contains(feature.geometry())
    ]
    if not inside:
        QMessageBox.information(parent, f"schools in {sDistrict}", "No schools found in this district")
    else:
        # try to sort school names
        inside.sort(key=lambda feature: feature["Name"])

        # Now we build display text
        lines = []
    
        # Distance calculation Task
        da = QgsDistanceArea()
        da.setSourceCrs(schools_Layer.crs(), QgsProject.instance().transformContext())
        da.setEllipsoid(schools_Layer.crs().ellipsoidAcronym())
        for feature in inside:
            # Get the school name
            school_name = feature["Name"]
            stype = feature["SchoolType"] 
            # centriod distance
            dist = da.measureLine(
                QgsPointXY(feature.geometry().asPoint()),
                QgsPointXY(district_centroid.x(), district_centroid.y())
            ) / 1000
            dist = round(dist, 2)
            # build the line
            lines.append(f"{school_name} ({stype}) - {dist} km")
            # Now select the school
            schools_Layer.selectByExpression(f"\"Name\" = '{school_name}'", QgsVectorLayer.AddToSelection)

        # To show some results
        QMessageBox.information(
            iface.mainWindow(),
            f"Schools in {sDistrict}",
            "\n".join(lines)
        )
        iface.mapCanvas().zoomToSelected()  # Zoom to selected features
