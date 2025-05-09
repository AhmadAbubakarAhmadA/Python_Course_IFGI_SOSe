# exercise_4_2.py
# Task here is to extract Name and X,Y of selected school features into a CSV.

from qgis.core import QgsProject

# find the Schools layer by name
layer_list = QgsProject.instance().mapLayersByName('Schools')
if not layer_list:
    raise Exception("Layer not found. Please check the layer name.")
layer = layer_list[0]
# Fetch only the selected features
selected_feats = layer.selectedFeatures()
if not selected_feats:
    raise Exception("No features selected. Please select at least one school first.")

# Writing the CSV file
output_path = r'C:\Users\User\Desktop\PIQAA\SchoolReport.csv'  
with open(output_path, 'w', encoding='utf-8') as f:
    # Write the header
    f.write('Name;X;Y\n')
    
    # Loop through each selected feature
    for feat in selected_feats:
        name = feat['Name']  # attribute field
        geom = feat.geometry()
        # If the layer is point-based, asPoint() gives you a QgsPointXY
        pt = geom.asPoint()
        x = pt.x()
        y = pt.y()
        # Write a semicolon-delimited line
        f.write(f"{name};{x};{y}\n")

#  Inform user about the output
print(f"SchoolReport.csv written with {len(selected_feats)} records to:\n{output_path}")

