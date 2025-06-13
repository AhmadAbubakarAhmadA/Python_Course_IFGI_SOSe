# -*- coding: utf-8 -*-
"""
PDF Generator for Muenster City District Profile
This module handles the creation of PDF reports for city districts
"""

from qgis.core import QgsProject, QgsFeature, QgsGeometry
from qgis.utils import iface
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
import tempfile
import time


class DistrictPDFGenerator:
    """Class to generate PDF profiles for city districts"""
    
    def __init__(self):
        pass
    
    def generate_district_profile(self, district_feature, output_path):
        """
        Generate a PDF profile for the given district feature
        
        :param district_feature: The district feature to generate profile for
        :param output_path: Path where the PDF should be saved
        :return: True if successful, False otherwise
        """
        try:
            # extract district information
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
            
            # generate map image
            map_image_path = self._generate_map_image(district_name, geometry)
            
            # create PDF
            self._create_pdf(
                output_path,
                district_name,
                parent_name,
                area_km2,
                households_count,
                parcels_count,
                schools_count,
                pools_count,
                map_image_path
            )
            
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False
    
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
    
    def _generate_map_image(self, district_name, geometry):
        """
        Generate a map image for the district
        
        :param district_name: Name of the district
        :param geometry: Geometry of the district
        :return: Path to the generated image
        """
        # set map canvas to district extent
        iface.mapCanvas().setExtent(geometry.boundingBox())
        iface.mapCanvas().refresh()
        time.sleep(1)  # wait for refresh to complete
        
        # save map image
        image_path = str(Path(tempfile.gettempdir()) / f"{district_name}_map.png")
        iface.mapCanvas().saveAsImage(image_path)
        
        return image_path
    
    def _create_pdf(self, output_path, district_name, parent_name, area_km2, 
                    households_count, parcels_count, schools_count, pools_count, map_image_path):
        """
        Create the actual PDF document
        
        :param output_path: Path where PDF should be saved
        :param district_name: Name of the district
        :param parent_name: Name of the parent district
        :param area_km2: Area in square kilometers
        :param households_count: Number of households
        :param parcels_count: Number of parcels
        :param schools_count: Number of schools
        :param pools_count: Number of pools
        :param map_image_path: Path to the map image
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        
        # set title
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 50, f"City District Profile: {district_name}")
        
        # add district information
        c.setFont("Helvetica", 12)
        text_lines = [
            f"Parent District: {parent_name}",
            f"District Name: {district_name}",
            f"Area: {area_km2} km²",
            f"Households: {households_count}",
            f"Parcels: {parcels_count}",
            f"Schools: {schools_count}",
            f"Pools: {pools_count}"
        ]
        
        # write text lines
        y = height - 100
        for line in text_lines:
            c.drawString(100, y, line)
            y -= 20
        
        # add map image
        try:
            c.drawImage(map_image_path, 50, 200, width=500, preserveAspectRatio=True, mask="auto")
        except Exception as e:
            print(f"Error adding map image: {str(e)}")
        
        # save PDF
        c.showPage()
        c.save()