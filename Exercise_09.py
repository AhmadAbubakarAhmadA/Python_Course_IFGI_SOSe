#importing necessary libraries
# this script is u
import arcpy
import os

# setting the workspace
arcpy.env.workspace = r'C:\Users\User\Desktop\PIQAA\exercise_arcpy_1.gdb'

# listing all feature classes of type 'Point'
point_fc_list = arcpy.ListFeatureClasses(feature_type='Point')
print("Point Feature Classes found:")
for fc in point_fc_list:
    print("??", fc)

# Defining the output feature class path
output_fc = os.path.join(arcpy.env.workspace, 'active_assets')

# if it exists, delete it
if arcpy.Exists(output_fc):
    arcpy.Delete_management(output_fc)
    print(f"Deleted existing feature class: {output_fc}")

# Creating a new point feature class with the same spatial reference 
# as the first point feature class in the list
description = arcpy.Describe(point_fc_list[0])
spatial_ref = description.spatialReference
arcpy.CreateFeatureclass_management(
    arcpy.env.workspace,
    'active_assets',
    'POINT',
    spatial_reference=spatial_ref
)

# Adding fields to the new feature class
arcpy.AddField_management(output_fc, 'name',   'TEXT')
arcpy.AddField_management(output_fc, 'type',   'TEXT')
arcpy.AddField_management(output_fc, 'status', 'TEXT')

# Inserting data into the new feature class
# Using an InsertCursor on output
fields_output = ['SHAPE@', 'name', 'type', 'status']
with arcpy.da.InsertCursor(output_fc, fields_output) as icur:
    
    # Iterating through each point feature class
    for fc in point_fc_list:
        print(f" scanning {fc} for active assets")

        # making sure the feature class has those fields
        fields_input = ['SHAPE@', 'type', 'status']
        with arcpy.da.SearchCursor(fc, fields_input) as scur:
            for shape, typ, status in scur:
                # only insert if status is 'active'
                if status and status.lower() == 'active':
                    print(f" inserting name={fc}, type={typ}, status={status}")
                    icur.insertRow((shape, fc, typ, status))

print("Done: active_assets created with only active records.")