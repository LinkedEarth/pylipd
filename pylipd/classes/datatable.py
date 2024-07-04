
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.variable import Variable

class DataTable:

    def __init__(self):
        self.missingValue: str = None
        self.fileName: str = None
        self.variables: list[Variable] = []
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'DataTable':
        self = DataTable()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasFileName":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.fileName = obj
        
            elif key == "hasMissingValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.missingValue = obj
        
            elif key == "hasVariable":

                for val in value:
                    if "@id" in val:
                        obj = Variable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.variables.append(obj)
            else:
                for val in value:
                    obj = None
                    if "@id" in val:
                        obj = mydata[val["@id"]]
                    elif "@value" in val:
                        obj = val["@value"]
                    self.set_non_standard_property(key, obj)
        
        return self

    def set_non_standard_property(self, key, value):
        if key not in self.misc:
            self.misc[key] = value
    
    def get_non_standard_property(self, key):
        return self.misc[key]
                   
    def get_all_non_standard_properties(self):
        return self.misc

    def add_non_standard_property(self, key, value):
        if key not in self.misc:
            self.misc[key] = []
        self.misc[key].append(value)
        
    def getFileName(self) -> str:
        return self.fileName

    def setFileName(self, fileName:str):
        self.fileName = fileName

    def getMissingValue(self) -> str:
        return self.missingValue

    def setMissingValue(self, missingValue:str):
        self.missingValue = missingValue

    def getVariables(self) -> list[Variable]:
        return self.variables

    def setVariables(self, variables:list[Variable]):
        self.variables = variables

    def addVariable(self, variable:Variable):
        self.variables.append(variable)
        