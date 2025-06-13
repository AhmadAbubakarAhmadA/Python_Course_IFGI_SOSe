# -*- coding: utf-8 -*-
"""
Export Dialog
Allows users to choose between CSV and PDF export options
"""

import os
import csv
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox
from qgis.core import QgsProject
from .pdf_generator import DistrictPDFGenerator

# load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'export_dialog.ui'))


class ExportDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, selected_features, parent=None):
        """
        Constructor.
        
        :param selected_features: List of selected district features
        """
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        self.selected_features = selected_features
        
        # connect buttons
        self.btnExportCSV.clicked.connect(self.export_csv)
        self.btnExportPDF.clicked.connect(self.export_pdf)
        
    def export_csv(self):
        """Export selected features to CSV file"""
        try:
            # get file path from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save CSV File",
                "",
                "CSV files (*.csv)"
            )
            
            if not file_path:
                QMessageBox.information(self, "Export Cancelled", "User cancelled the process.")
                return
                
            # create CSV file
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # write header
                writer.writerow(['District Name', 'Size (km²)', 'Parcels', 'Schools'])
                
                # write data for each selected feature
                for feature in self.selected_features:
                    district_name = feature["Name"]
                    geometry = feature.geometry()
                    
                    # calculate area in km²
                    area_m2 = geometry.area()
                    area_km2 = round(area_m2 / 1_000_000, 2)
                    
                    # count parcels and schools
                    parcels_count = self._count_points_in_district("Muenster_Parcels", geometry)
                    schools_count = self._count_points_in_district("Schools", geometry)
                    
                    # write row
                    writer.writerow([district_name, area_km2, parcels_count, schools_count])
            
            QMessageBox.information(self, "Export Successful", "Process finished successfully.")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Error exporting CSV: {str(e)}")
    
    def export_pdf(self):
        """Export selected feature to PDF profile"""
        try:
            # check if only one feature is selected
            if len(self.selected_features) > 1:
                QMessageBox.warning(
                    self,
                    "Multiple Features Selected",
                    "Only one feature should be selected to run the process."
                )
                return
            
            # get file path from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF File",
                "",
                "PDF files (*.pdf)"
            )
            
            if not file_path:
                QMessageBox.information(self, "Export Cancelled", "User cancelled the process.")
                return
            
            # generate PDF
            pdf_generator = DistrictPDFGenerator()
            success = pdf_generator.generate_district_profile(self.selected_features[0], file_path)
            
            if success:
                QMessageBox.information(self, "Export Successful", "Process finished successfully.")
                self.accept()
            else:
                QMessageBox.critical(self, "Export Error", "Error generating PDF profile.")
                
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Error exporting PDF: {str(e)}")
    
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