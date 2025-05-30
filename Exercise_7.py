# importing necessary libraries
from qgis.core import (
    QgsProject,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
    QgsProcessingException
)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.utils import iface
from pathlib import Path
import tempfile, time
from qgis.core import QgsFeature, QgsGeometry
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Helper function to get the list of districts from the project
def getDistrictNames():
    """
    Returns a sorted list of district names Alphabetically
    from the layer 'Muenster_City_Districts'
    """
    layer_list = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
    if not layer_list:
        raise ValueError("Layer 'Muenster_City_Districts' not found.")
    layer = layer_list[0]
    district_names = [feature["Name"] for feature in layer.getFeatures()]
    district_names.sort()
    return district_names

# This class defines the custom processing algorithm built for creating a city district profile.
class CreateCityDistictsProfile(QgsProcessingAlgorithm):
    
    
    def __init__(self):
        super().__init__()

    def name(self):
        return "create_city_districts_profile"

# This function returns the unique identifier for the algorithm
    def displayName(self):
        return QCoreApplication.translate(
            "CreateCityDistrictsProfile",
            "Create City Districts Profile"
        )
# This function returns the group name for the algorithm
    def group(self):
        return QCoreApplication.translate(
            "CreateCityDistrictsProfile",
            "Districts Analysis"
        )
# This function returns the unique identifier for the algorithm group
    def groupId(self):
        return "districts_analysis"

# This function returns a short help string for the algorithm
    def shortHelpString(self):
        return QCoreApplication.translate(
            "CreateCityDistrictsProfile",
            "This algorithm generates a PDF summarizing objects and a map for the selected city district."
        )

    # To override the abstract initAlgorithm so that the class can be instantiated
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterEnum(
                "DISTRICT",
                QCoreApplication.translate(
                    "CreateCityDistrictsProfile",
                    "Select District"
                ),
                options=getDistrictNames(),
            )
        )
        # Adding a parameter for the theme selection (Schools or Pools)
        self.addParameter(
            QgsProcessingParameterEnum(
                "THEME",
                QCoreApplication.translate(
                    "CreateCityDistrictsProfile",
                    "Include Information About"
                ),
                options=["Schools", "Pools"]
            )
        )
        # Adding a file destination parameter for the output PDF
        self.addParameter(
            QgsProcessingParameterFileDestination(
                "OUTPUT",
                QCoreApplication.translate(
                    "CreateCityDistrictsProfile",
                    "Save PDF to"
                ),
                fileFilter="PDF files (*.pdf)",
            )
        )

    # This function will read the parameters and execute the algorithm
    def processAlgorithm(self, parameters, context, feedback):
        district_index = self.parameterAsEnum(parameters, "DISTRICT", context)
        district_list = getDistrictNames()
        district_name = district_list[district_index]

        # Getting the theme index and corresponding theme name
        theme_index = self.parameterAsEnum(parameters, "THEME", context)
        themes = ["Schools", "Pools"]
        theme = themes[theme_index]

        # Getting the output file path from the parameters
        output_file = self.parameterAsFileOutput(parameters, "OUTPUT", context)
        
        # Checking if the output file path is valid
        feedback.pushInfo(f"District: {district_name}")
        feedback.pushInfo(f"Theme: {theme}")
        feedback.pushInfo(f"Output: {output_file}")
        
        # Getting the district layer and the feature for the selected district
        district_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
        
        # Finding the feature for the selected district
        district_feature = None
        for feature in district_layer.getFeatures():
            if feature["Name"] == district_name:
                district_feature = feature
                break
        # If no feature is found, raise an exception
        if district_feature is None:
            raise QgsProcessingException(
                f"District '{district_name}' not found."
            )
        # Extracting the parent district name, geometry, and area
        parent_name = district_feature["P_District"]
        geometry = district_feature.geometry()
        area_m2 = geometry.area()
        area_km2 = round(area_m2 / 1_000_000, 2)
         
         # Function to count points in a layer that fall within the district geometry
        def countpoints(layer_name, field_name):
            layer_list = QgsProject.instance().mapLayersByName(layer_name)
            if not layer_list:
                feedback.pushInfo(f"Layer '{layer_name}' not found, returning count = 0")
                return 0
            layer = layer_list[0]
            count = 0
            for point in layer.getFeatures():
                if geometry.contains(point.geometry()):
                    count += 1
            return count      # Count points in the specified layer that fall within the district geometry
        
        # Counting households, parcels, and theme-specific points
        households_count = countpoints("House_Numbers", "AnyField")
        parcels_count = countpoints("Muenster_Parcels", "AnyField")
        theme_layer_name = "Schools" if theme == "Schools" else "public_swimming_pools"
        theme_count_raw = countpoints(theme_layer_name, "Name")
        
        # Preparing the text for the theme count
        if theme_count_raw == 0:
            theme_count_text = f"No {theme.lower()} in this district"
        else:
            theme_count_text = f"{theme}: {theme_count_raw}"

        # Setting the map canvas to the district geometry and saving the map as an image
        iface.mapCanvas().setExtent(geometry.boundingBox())
        iface.mapCanvas().refresh()
        time.sleep(1)
        feedback.setProgress(50)
        # Save the map canvas as an image
        image_path = str(Path(tempfile.gettempdir()) / f"{district_name}.png")
        iface.mapCanvas().saveAsImage(image_path)
 
        # Creating the PDF report using ReportLab
        c = canvas.Canvas(output_file, pagesize=A4)
        width, height = A4
    
       # Setting the PDF title and adding district information
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 50, f"City District Profile: {district_name}")

        # Adding district information to the PDF
        c.setFont("Helvetica", 12)
        text = (
            f"Parent District: {parent_name}\n"
            f"District Name: {district_name}\n"
            f"Area: {area_km2} km²\n"
            f"Households: {households_count}\n"
            f"Parcels: {parcels_count}\n"
            f"{theme_count_text}"
        )
        
        # this adds the text to the PDF
        y = height - 100
        for line in text.split("\n"):
            c.drawString(100, y, line)
            y -= 20
        # Adding the map image to the PDF
        c.drawImage(image_path, 50, 200, width=500, preserveAspectRatio=True, mask="auto")

        # Adding a footer with the current date and time
        c.showPage()
        c.save()
        feedback.pushInfo("PDF report generated successfully.")

        return {"OUTPUT": output_file}

    # This function is used to create an instance of the algorithm
    def createInstance(self):
        return CreateCityDistictsProfile()
