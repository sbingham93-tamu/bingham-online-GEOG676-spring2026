
# create a gdb and garage feature
import os
from tkinter import ALL
import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"C:\Users\sbing\TAMU\GEOG676\bingham-online-GEOG676-spring2026\Lab4"
folder_path = arcpy.env.workspace

gdb_name = "garages.gdb"
gdb_path = os.path.join(folder_path, gdb_name)

if not arcpy.Exists(gdb_path):
    arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_file = os.path.join(folder_path, "garages.csv")

garages_layer_name = "Garage_Points"
garages_points = os.path.join(gdb_path, garages_layer_name)

if arcpy.Exists(garages_points):
    arcpy.Delete_management(garages_points)

arcpy.management.XYTableToPoint(csv_file, garages_points, "X", "Y")

print("Garage points created:", garages_points)

# open campus gdb, copy building feature to our gdb
campus = r'C:\Users\sbing\TAMU\GEOG676\bingham-online-GEOG676-spring2026\Lab4\campus.gdb'

import os
import arcpy

arcpy.env.overwriteOutput = True
# --- paths ---
buildings = os.path.join(gdb_path, "Buildings")   # <-- MUST be above the Exists() line

# delete if it already exists
if arcpy.Exists(buildings):
    arcpy.management.Delete(buildings)

# copy buildings into your gdb
import os
import arcpy

arcpy.env.overwriteOutput = True

campus_gdb = r"C:\Users\sbing\TAMU\GEOG676\bingham-online-GEOG676-spring2026\Lab4\campus.gdb"

# input from campus.gdb (adjust name if needed)
buildings_campus = os.path.join(campus_gdb, "Structures")

# output into your garages.gdb
buildings = os.path.join(gdb_path, "Buildings")

# optional delete (if overwriteOutput ever doesn’t behave)
if arcpy.Exists(buildings):
    arcpy.management.Delete(buildings)

arcpy.Copy_management(buildings_campus, buildings)
if arcpy.Exists(buildings):
    arcpy.management.Delete(buildings)

buildings_campus = os.path.join(campus, "Structures")
buildings = os.path.join(gdb_path, "Buildings")

if arcpy.Exists(buildings):
    arcpy.management.Delete(buildings)

arcpy.Copy_management(buildings_campus, buildings)

garage_reproj = os.path.join(gdb_path, "Garage_Points_reprojected")

spatial_ref = arcpy.Describe(buildings_campus).spatialReference

arcpy.Project_management(garages_points, garage_reproj, spatial_ref)

# Re-Projection
spatial_ref = arcpy.Describe(buildings_campus).spatialReference
arcpy.Project_management(garages_points, garage_reproj, spatial_ref)

# buffer the garages
garageBuffered = arcpy.Buffer_analysis(garage_reproj, os.path.join(gdb_path, "Garage_Buffer"), "100 Feet")

# Intersect out buffer with the buildings
arcpy.Intersect_analysis([garageBuffered, buildings], os.path.join(gdb_path, "Garage_Building_Intersect"))

intersect_table = os.path.join(gdb_path, "Garage_Building_Intersect")
out_name = "Garage_Building_Table"

arcpy.conversion.TableToTable(intersect_table, gdb_path, out_name)
