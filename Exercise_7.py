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
import tempfile
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

    def displayName(self):
        return QCoreApplication.translate(
            "CreateCityDistrictsProfile",
            "Create City Districts Profile"
        )

    def group(self):
        return QCoreApplication.translate(
            "CreateCityDistrictsProfile",
            "Districts Analysis"
        )

    def groupId(self):
        return "districts_analysis"

    def shortHelpString(self):
        return QCoreApplication.translate(
            "CreateCityDistrictsProfile",
            "This algorithm generates a PDF summarizing objects and a map for the selected city district."
        )

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

    def processAlgorithm(self, parameters, context, feedback):
        district_index = self.parameterAsEnum(parameters, "DISTRICT", context)
        district_list = getDistrictNames()
        district_name = district_list[district_index]

        theme_index = self.parameterAsEnum(parameters, "THEME", context)
        themes = ["Schools", "Pools"]
        theme = themes[theme_index]

        output_file = self.parameterAsFileOutput(parameters, "OUTPUT", context)

        feedback.pushInfo(f"District: {district_name}")
        feedback.pushInfo(f"Theme: {theme}")
        feedback.pushInfo(f"Output: {output_file}")

        district_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

        district_feature = None
        for feature in district_layer.getFeatures():
            if feature["Name"] == district_name:
                district_feature = feature
                break

        if district_feature is None:
            raise QgsProcessingException(
                f"District '{district_name}' not found."
            )

        geometry = district_feature.geometry()
        area_m2 = geometry.area()
        area_km2 = round(area_m2 / 1_000_000, 2)

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
            return count


        households_count = countpoints("Households", "AnyField")
        parcels_count = countpoints("Parcels", "AnyField")
        theme_layer_name = "Schools" if theme == "Schools" else "public_swimming_pools"
        theme_count = countpoints(theme_layer_name, "Name")

        iface.mapCanvas().setExtent(geometry.boundingBox())
        iface.mapCanvas().refresh()
        feedback.setProgress(50)
        image_path = str(Path(tempfile.gettempdir()) / f"{district_name}.png")
        iface.mapCanvas().saveAsImage(image_path,)

        c = canvas.Canvas(output_file, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica", 16)
        c.drawString(100, height - 50, f"City District Profile: {district_name}")

        c.setFont("Helvetica", 12)
        text = (
            f"District Name: {district_name}\n"
            f"Area: {area_km2} km²\n"
            f"Households: {households_count}\n"
            f"Parcels: {parcels_count}\n"
            f"{theme}: {theme_count}"
        )

        y = height - 100
        for line in text.split("\n"):
            c.drawString(100, y, line)
            y -= 20

        c.drawImage(image_path, 50, 200, width=500, preserveAspectRatio=True, mask="auto")

        c.showPage()
        c.save()
        feedback.pushInfo("PDF report generated successfully.")

        return {"OUTPUT": output_file}

    def createInstance(self):
        return CreateCityDistictsProfile()
