
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.paleounit import PaleoUnit

class Resolution:

    def __init__(self):
        self.units: PaleoUnit = None
        self.minValue: float = None
        self.meanValue: float = None
        self.maxValue: float = None
        self.medianValue: float = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Resolution':
        self = Resolution()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasMedianValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.medianValue = obj
        
            elif key == "hasUnits":

                for val in value:
                    obj = PaleoUnit.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.units = obj
        
            elif key == "hasMaxValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.maxValue = obj
        
            elif key == "hasMeanValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.meanValue = obj
        
            elif key == "hasMinValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.minValue = obj
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
        
    def getUnits(self) -> PaleoUnit:
        return self.units

    def setUnits(self, units:PaleoUnit):
        self.units = units

    def getMinValue(self) -> float:
        return self.minValue

    def setMinValue(self, minValue:float):
        self.minValue = minValue

    def getMeanValue(self) -> float:
        return self.meanValue

    def setMeanValue(self, meanValue:float):
        self.meanValue = meanValue

    def getMaxValue(self) -> float:
        return self.maxValue

    def setMaxValue(self, maxValue:float):
        self.maxValue = maxValue

    def getMedianValue(self) -> float:
        return self.medianValue

    def setMedianValue(self, medianValue:float):
        self.medianValue = medianValue
