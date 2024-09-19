import os
import yaml


class SetVariables:
    """
    A class to set variables from various sources.

    This class is designed to set variables based on an array of variable names.
    The variables can be set from environment variables, a shell script file,
    or a YAML file if they exist.

    Attributes:
        varNamesArray (list): An array of variable names to be set.
        shFileName (str, optional): The name of the shell script file. Defaults to None.
        yamlFileName (str, optional): The name of the YAML file. Defaults to None.
    """

    def __init__(self, varNamesArray, shFileName=None, yamlFileName=None) -> None:
        """
        Initializes the SetVariables class with variable names, shell script file name, and YAML file name.

        Args:
            varNamesArray (list): An array of variable names to be set.
            shFileName (str, optional): The name of the shell script file. Defaults to None.
            yamlFileName (str, optional): The name of the YAML file. Defaults to None.
        """
        self.varNamesArray = varNamesArray
        self.shFileName    = shFileName
        self.yamlFileName  = yamlFileName
        self.variableValues = {}
        for variableName in self.varNamesArray:
            variableValue = self.setFromEnvironment(variableName)
            if (variableValue == "" ):
                variableValue = self.setFromShellFile(shFileName, variableName)
                if ( variableValue == ""):
                    variableValue = self.setFromYamlFile(yamlFileName, variableName)
            self.variableValues[variableName] = variableValue
        pass

    def getVariables(self):
        return self.variableValues

    def setFromYamlFile(self, yamlFileName, variableName):
        retVal = ""
        if ( yamlFileName != None ):
            with open(yamlFileName,'r') as yamlFile:
                data = yaml.safe_load(yamlFile)
                #print(f'DEBUG: yaml file contents \n{json.dumps(data, indent=3)}')
                retVal = data[variableName]
        return retVal

    def setFromShellFile(self, shFileName, variableName):
        retVal = ""
        if ( shFileName != None ):
            with open(shFileName, 'r') as file:
                for line in file:
                    line = line.split('#')[0].rstrip().strip()    # get rid of the comments
                    line = line.replace("export", "", 1).strip()  # get rid of the export command
                    if( variableName.upper() == line.split('=')[0].rstrip().strip() ):
                        variableValue = line.split("=")[1].rstrip().strip()
                        if ( variableValue[0] == '\'' ) or ( variableValue[0] == '"' ):
                            variableValue = variableValue[1:]
                        if ( variableValue[-1] == '\'' ) or ( variableValue[1] == '"' ):
                            variableValue = variableValue[:-1]
                        retVal = variableValue
                        #print(f'DEBUG found variable {variableName} with value {variableValue}')
        return retVal

    def setFromEnvironment(self, variableName):
        retVal = ""
        ev = os.getenv(variableName.upper())
        if ( ev != None ):
            retVal = ev
        return retVal
