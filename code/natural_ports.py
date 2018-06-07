# Takes 33.9 seconds to run this script

print "Setting the working directory"
import os
work_dir = os.path.dirname(os.path.realpath(__file__)) # This method returns the directry path of this script.
os.chdir(work_dir)

print "Launching ArcGIS"
import arcpy

print "Enabling the Spatial Analyst extension"
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

print "Setting the environment"
arcpy.env.overwriteOutput = True # Allow the overwriting of the output files
arcpy.env.workspace = "../b_temp/b_temp.gdb" # Set the working directory. Some geoprocessing tools (e.g. Extract By Mask) cannot save the output unless the workspace is a geodatabase.

if not os.path.isdir("../data/"): # Create the output directory if it doesn't exist
    os.makedirs("../data/")

### Define the main function ###
def main():
  try:
    # Input
    ports_shp = "../orig/WPI.shp"
    # Output
    output_shp = "../data/natural_ports.shp"
    # Process
    select_natural_ports(ports_shp, output_shp)

    print "All done."

  # Return geoprocessing specific errors
  except arcpy.ExecuteError:
    print arcpy.GetMessages()
  # Return any other type of error
  except:
    print "There is non-geoprocessing error."
  # Check in extensions
  finally:
    arcpy.CheckInExtension("spatial")

# subfunctions
def select_natural_ports(ports_shp, natural_harbors_shp):
  print "...deleting the output if it exists"
  delete_if_exists(natural_harbors_shp)
  print "...selecting natural harbors"
  selection_criteria = '"HARBORTYPE" = \'CN\' OR "HARBORTYPE" = \'RN\''
  arcpy.Select_analysis(in_features = ports_shp, out_feature_class = natural_harbors_shp, where_clause = selection_criteria) # http://desktop.arcgis.com/en/arcmap/10.3/tools/analysis-toolbox/select.htm

def delete_if_exists(file):
  if arcpy.Exists(file):
    arcpy.Delete_management(file)


### Execute the main function ###
if __name__ == "__main__":
    main()
