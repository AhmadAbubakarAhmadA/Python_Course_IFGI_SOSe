# -*- coding: utf-8 -*-
"""
District Profile Dialog
Shows detailed information about a selected district
"""

import os
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsProject

# load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'district_profile_dialog.ui'))


class DistrictProfileDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(DistrictProfileDialog, self).__init__(parent)
        self.setupUi(self)
        
    def set_district_data(self, district_feature):
        """
        Set the district data to display in the dialog
        
        :param district_feature: The district feature to display information for
        """
        # extract basic district information
        district_name = district_feature["Name"]
        parent_name = district_feature["P_District"]
        geometry = district_feature.geometry()
        
        # calculate area in km²
        area_m2 = geometry.area()
        area_km2 = round(area_m2 / 1_000_000, 2)
        
        # count objects in district
        households_count = self._count_points_in_district("House_Numbers", geometry)
        parcels_count = self._count_points_in_district("Muenster_Parcels", geometry)
        schools_count = self._count_points_in_district("Schools", geometry)
        pools_count = self._count_points_in_district("public_swimming_pools", geometry)
        
        # update the UI labels
        self.lblTitle.setText(f"District Profile: {district_name}")
        self.lblDistrictNameValue.setText(district_name)
        self.lblParentDistrictValue.setText(parent_name)
        self.lblAreaValue.setText(f"{area_km2} km²")
        self.lblHouseholdsValue.setText(str(households_count))
        self.lblParcelsValue.setText(str(parcels_count))
        self.lblSchoolsValue.setText(str(schools_count))
        self.lblPoolsValue.setText(str(pools_count))
        
    def _count_points_in_district(self, layer_name, district_geometry):
        """
        Count points from a layer that fall within the district geometry
        
        :param layer_name: Name of the layer to count points from
        :param district_geometry: Geometry of the district
        :return: Number of points within the district
        """
        layer_list = QgsProject.instance().mapLayersByName(layer_name)
        if not layer_list:
            print(f"Warning: Layer '{layer_name}' not found, returning count = 0")
            return 0
            
        layer = layer_list[0]
        count = 0
        
        for feature in layer.getFeatures():
            if district_geometry.contains(feature.geometry()):
                count += 1
                
        return count