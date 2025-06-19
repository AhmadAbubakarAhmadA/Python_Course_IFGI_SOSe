#importing necessary libraries
# this script is used to create a feature class of active assets from point feature classes
import arcpy
import os

# setting the workspace
arcpy.env.workspace = r'C:\Users\User\Desktop\PIQAA\exercise_arcpy_1.gdb'
arcpy.env.overwriteOutput = True

# listing all feature classes of type 'Point'
point_fc_list = arcpy.ListFeatureClasses(feature_type='Point')
print("Point Feature Classes found:")
for fc in point_fc_list:
    print(" •", fc)

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
arcpy.AddField_management(output_fc, 'name',      'TEXT')
arcpy.AddField_management(output_fc, 'type',      'TEXT')
arcpy.AddField_management(output_fc, 'status',    'TEXT')

# Inserting data into the new feature class
# Using an InsertCursor on output
fields_output = ['SHAPE@', 'name', 'type', 'status']
with arcpy.da.InsertCursor(output_fc, fields_output) as icur:
    
    # Iterating through each point feature class
    for fc in point_fc_list:
        print(f"Scanning {fc} for active assets")

        # making sure the feature class has those fields
        fields_input = ['SHAPE@', 'type', 'status']
        with arcpy.da.SearchCursor(fc, fields_input) as scur:
            for shape, typ, status in scur:
                # only insert if status is 'active'
                if status and status.lower() == 'active':
                    name_val = fc
                    type_val = typ.strip().lower()
                    print(f" Inserting name={name_val}, type={type_val}, status={status}")
                    icur.insertRow((shape, name_val, type_val, status))

print("Done: active_assets created with only active records.")


# Building buffer around each active asset according to their type
# Adding a helper field 'buffer_distance'
arcpy.AddField_management(output_fc, 'bufDist', 'DOUBLE')

# calculate buffer distances based on type
type_to_dist = {
    'mast':             300,
    'mobile_antenna':    50,
    'building_antenna': 100
}

# Using an UpdateCursor to set buffer distances
with arcpy.da.UpdateCursor(output_fc, ['type', 'bufDist']) as ucur:
    for typ, _ in ucur:
        key = typ.strip().lower()
        dist = type_to_dist.get(key, 0)
        ucur.updateRow((typ, dist))

# Running the buffer tools
# merge all buffers into a single feature class called coverage
coverage_fc = os.path.join(arcpy.env.workspace, 'coverage')
if arcpy.Exists(coverage_fc):
    arcpy.Delete_management(coverage_fc)
    print(f"Deleted existing coverage feature class: {coverage_fc}")

arcpy.Buffer_analysis(
    in_features=output_fc,
    out_feature_class=coverage_fc,
    buffer_distance_or_field='bufDist',
    line_side='FULL',
    line_end_type='ROUND',
    dissolve_option='ALL'
)

print("Done: Buffers created and merged into coverage feature class.")