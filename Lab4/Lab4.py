
# create a gdb and garage feature
import arcpy

arcpy.env.workspace = r'C:\Users\sbing\TAMU\GEOG676\bingham-online-GEOG676-spring2026\Lab4'
folder_path = r'C:\Users\sbing\TAMU\GEOG676\bingham-online-GEOG676-spring2026\Lab4'
gdb_name = 'Lab04.gdb'
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r'C:\Users\sbing\TAMU\GEOG676\TAMU-MGSc-Online-GEOG676-GIS-PROGRAMMING\data\homework\04\\garages.csv'
garage_layer_name = 'Garage_Points'
garage = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garage
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

# open campus gdb, copy building feature to our gdb
campus = r'C:\Users\sbing\TAMU\GEOG676\TAMU-MGSc-Online-GEOG676-GIS-PROGRAMMING\data\homework\04\Campus.gdb'
buildings_campus = campus + r"\Structures"
buildings = gdb_path + r"\\" + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)

# Re-Projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + r"\Garage_Points_reprojected", spatial_ref)

# buffer the garages
buffer_distance = "150 Meters"
garageBuffered = arcpy.Buffer_analysis(
gdb_path + r"\Garage_Points_reprojected",
gdb_path + r"\Garage_Points_buffered",
buffer_distance
)

# Intersect our buffer with the buildings
arcpy.Intersect_analysis(
    [garageBuffered, buildings],
    gdb_path + r"\Garage_Building_Intersect",
    "ALL"
)

arcpy.TableToTable_conversion(
    gdb_path + r"\Garage_Building_Intersect",
    r"C:\Users\sbing\TAMU\GEOG676\TAMU-MGSc-Online-GEOG676-GIS-PROGRAMMING\data\homework\04\Campus.gdb",
    "nearbyBuildings"
)