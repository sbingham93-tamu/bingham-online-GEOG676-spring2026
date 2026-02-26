import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the toolbox is the name of the .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""
        # List of tool closest classified with this toolbox
        self.tools = [GraduatedColorsRenderer]

class GraduatedColorsRenderer(object):
    def __init__(self):
        """Tool definition"""
        self.label = "GraduatedColors"
        self.description = "Create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        ***Define parameter definitions***
        #original project name
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputeName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

      # which layer you want to clarify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="layerToClassify",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        #output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="outputLocation",
            datatype="DEFolder",
            direction="Input"
        )
        #output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="outputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        ***Set whether tool is liscensed to execute.***
        return True

    def updateParameters(self, parameters):
        ***Modify the values and properties of parameters before internal
        validation is perrformed. This method is called whenever a parameter
        has been chargeed.***
        return

    def updateMessages(self, parameters):
        ***Modify the messages created by internal vaalicaiton for each tool
        parameter. This method is called after internal validation.***
        return

def execute(self, parameters, messages):
    ***The source code of the tool.***
    # Define Progressor Varibles
    readline - 3 #the etime for users to read thte progress
    start = 0      #beginning position of the progressor
    max = 100      # end position
    step = 33      # the progress interval to move the progressor along

    #Setup Progressor
    arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
    time.sleep(readTime) #pause the execution for 2.5 seconds

    #Add message to the Results Pane
    arcpy.AddMessage("Validating Project File...")

    # Project file
    project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

    # Grabs the first Instance of a Map from the .aprx
    campus = project.listMaps("Map")[0]

    # Increment Progressor
    arcpy.SetProgressorPosition(start + step)
    arcpy.SetProgressorLabel("Finding your map layer...")
    time.sleep(readTime)
    arcpy.AddMessage("Finding your map layer...")

        for layer in campus.listLayers():

            if layer.isFeatureLayer:

                symbology = layer.symbology

                if hasattr(symbology, "renderer"):

                    if layer.name == parameters[1].valueAsText:

                        arcpy.SetProgressorPosition(start + step * 2)
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        # Update renderer
                        symbology.updateRenderer("GraduatedColorsRenderer")

                        # Classification field
                        symbology.renderer.classificationField = "Shape_Area"

                        arcpy.SetProgressorPosition(start + step * 2)
                        arcpy.SetProgressorLabel("Cleaning up...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Cleaning up...")

                        # Number of classes
                        symbology.renderer.breakCount = 5

                        # Color ramp
                        symbology.renderer.colorRamp = project.listColorRamps("Oranges (5 Classes)")[0]

                        # Apply symbology
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")

        else:
            print("No feature layers found")

        # Saving project
        arcpy.SetProgressorPosition(start + step * 3)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        output_path = os.path.join(
            parameters[2].valueAsText,
            parameters[3].valueAsText + ".aprx"
        )

        project.saveACopy(output_path)
