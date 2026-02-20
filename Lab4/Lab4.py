
# create a gdb and garage feature
import os
import arcpy

arcpy.env.overwriteOutput = True

# -------------------------------
# INPUT DATA (from cloned repo)
# -------------------------------
repo_dir = r"C:\Users\sbing\TAMU\GEOG676\TAMU-MGSc-Online-GEOG676-GIS-PROGRAMMING\data\homework\04"

csv_path = os.path.join(repo_dir, "garages.csv")
campus_gdb = os.path.join(repo_dir, "Campus.gdb")
structures_fc = os.path.join(campus_gdb, "Structures")

# -------------------------------
# OUTPUT LOCATION (your Lab4 folder)
# -------------------------------
lab4_dir = r"C:\Users\sbing\TAMU\GEOG676\bingham-online-GEOG676-spring2026\Lab4"
arcpy.env.workspace = lab4_dir

gdb_name = "Lab04.gdb"
out_gdb = os.path.join(lab4_dir, gdb_name)

# Create GDB if it doesn't exist
if not arcpy.Exists(out_gdb):
    arcpy.management.CreateFileGDB(lab4_dir, gdb_name)

# -------------------------------
# 1) Create garage points from CSV
# -------------------------------
garage_layer = "Garage_Points_Lyr"
arcpy.management.MakeXYEventLayer(csv_path, "X", "Y", garage_layer)

garage_points = os.path.join(out_gdb, "Garage_Points")
arcpy.management.CopyFeatures(garage_layer, garage_points)

# -------------------------------
# 2) Copy buildings into our GDB
# -------------------------------
buildings = os.path.join(out_gdb, "Buildings")
arcpy.management.CopyFeatures(structures_fc, buildings)

# -------------------------------
# 3) Reproject garages to match buildings
# -------------------------------
spatial_ref = arcpy.Describe(buildings).spatialReference

garage_points_reproj = os.path.join(out_gdb, "Garage_Points_reprojected")
arcpy.management.Project(garage_points, garage_points_reproj, spatial_ref)

# -------------------------------
# 4) Buffer the garages
# -------------------------------
garage_buffer = os.path.join(out_gdb, "Garage_Points_buffered")
arcpy.analysis.Buffer(garage_points_reproj, garage_buffer, "150")

# -------------------------------
# 5) Intersect buffer with buildings
# -------------------------------
intersection_fc = os.path.join(out_gdb, "Garage_Building_Intersection")
arcpy.analysis.Intersect([garage_buffer, buildings], intersection_fc, "ALL")

# -------------------------------
# 6) Export to CSV in Lab4 folder
# -------------------------------
arcpy.conversion.TableToTable(
    intersection_fc,
    lab4_dir,
    "nearbyBuildings.csv"
)
