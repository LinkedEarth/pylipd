
##############################
# Auto-generated. Do not Edit
##############################

import re

class Uncertainty:

    def __init__(self):
        self.uncertaintyType: str = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Uncertainty':
        self = Uncertainty()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasUncertaintyType":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.uncertaintyType = obj
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
        
    def getUncertaintyType(self) -> str:
        return self.uncertaintyType

    def setUncertaintyType(self, uncertaintyType:str):
        self.uncertaintyType = uncertaintyType
