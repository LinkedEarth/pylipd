
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.integrationtime import IntegrationTime
from pylipd.classes.independentvariable import IndependentVariable

class IsotopeInterpretation:

    def __init__(self):
        self.independentVariables: list[IndependentVariable] = []
        self.integrationTime: IntegrationTime = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'IsotopeInterpretation':
        self = IsotopeInterpretation()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasIndependentVariable":

                for val in value:
                    if "@id" in val:
                        obj = IndependentVariable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.independentVariables.append(obj)
        
            elif key == "hasIntegrationTime":

                for val in value:
                    if "@id" in val:
                        obj = IntegrationTime.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.integrationTime = obj
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
        
    def getIntegrationTime(self) -> IntegrationTime:
        return self.integrationTime

    def setIntegrationTime(self, integrationTime:IntegrationTime):
        self.integrationTime = integrationTime

    def getIndependentVariables(self) -> list[IndependentVariable]:
        return self.independentVariables

    def setIndependentVariables(self, independentVariables:list[IndependentVariable]):
        self.independentVariables = independentVariables

    def addIndependentVariable(self, independentVariable:IndependentVariable):
        self.independentVariables.append(independentVariable)
        