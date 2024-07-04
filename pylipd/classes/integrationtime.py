
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.independentvariable import IndependentVariable
from pylipd.classes.paleounit import PaleoUnit

class IntegrationTime:

    def __init__(self):
        self.relevantQuote: str = None
        self.units: PaleoUnit = None
        self.independentVariables: list[IndependentVariable] = []
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'IntegrationTime':
        self = IntegrationTime()
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
        
            elif key == "hasUnits":

                for val in value:
                    obj = PaleoUnit.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.units = obj
        
            elif key == "relevantQuote":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.relevantQuote = obj
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
        
    def getRelevantQuote(self) -> str:
        return self.relevantQuote

    def setRelevantQuote(self, relevantQuote:str):
        self.relevantQuote = relevantQuote

    def getUnits(self) -> PaleoUnit:
        return self.units

    def setUnits(self, units:PaleoUnit):
        self.units = units

    def getIndependentVariables(self) -> list[IndependentVariable]:
        return self.independentVariables

    def setIndependentVariables(self, independentVariables:list[IndependentVariable]):
        self.independentVariables = independentVariables

    def addIndependentVariable(self, independentVariable:IndependentVariable):
        self.independentVariables.append(independentVariable)
        