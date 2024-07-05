
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid

class PhysicalSample:

    def __init__(self):
        self.housedAt: str = None
        self.iGSN: str = None
        self.name: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#PhysicalSample"
        self.id = self.ns + "/" + uniqid("PhysicalSample.")

    @staticmethod
    def from_data(id, data) -> 'PhysicalSample':
        self = PhysicalSample()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasIGSN":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.iGSN = obj
        
            elif key == "housedAt":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.housedAt = obj
        
            elif key == "name":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
            else:
                for val in value:
                    obj = None
                    if "@id" in val:
                        obj = data[val["@id"]]
                    elif "@value" in val:
                        obj = val["@value"]
                    self.set_non_standard_property(key, obj)
            
        return self

    def to_data(self, data={}):
        data[self.id] = {}
        data[self.id]["type"] = [
            {
                "@id": self.type,
                "@type": "uri"
            }
        ]

        if self.housedAt:
            value_obj = self.housedAt
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["housedAt"] = [obj]
                

        if self.iGSN:
            value_obj = self.iGSN
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasIGSN"] = [obj]
                

        if self.name:
            value_obj = self.name
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["name"] = [obj]
                
        for key in self.misc:
            value = self.misc[key]
            data[self.id][key] = []
            ptype = None
            tp = type(value).__name__
            if tp == "int":
                ptype = "http://www.w3.org/2001/XMLSchema#integer"
            elif tp == "float" or tp == "double":
                ptype = "http://www.w3.org/2001/XMLSchema#float"
            elif tp == "str":
                if re.match("\d{4}-\d{2}-\d{2}", value):
                    ptype = "http://www.w3.org/2001/XMLSchema#date"
                else:
                    ptype = "http://www.w3.org/2001/XMLSchema#string"
            elif tp == "bool":
                ptype = "http://www.w3.org/2001/XMLSchema#boolean"

            data[self.id][key].append({
                "@value": value,
                "@type": "literal",
                "@datatype": ptype
            })
        
        return data

    def to_json(self):
        data = {
            "@id": self.id
        }

        if self.housedAt:
            value_obj = self.housedAt
            obj = value_obj
            data["housedat"] = obj

        if self.iGSN:
            value_obj = self.iGSN
            obj = value_obj
            data["hasidentifier"] = obj

        if self.name:
            value_obj = self.name
            obj = value_obj
            data["hasname"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

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
        
    def getHousedAt(self) -> str:
        return self.housedAt

    def setHousedAt(self, housedAt:str):
        self.housedAt = housedAt
    
    def getIGSN(self) -> str:
        return self.iGSN

    def setIGSN(self, iGSN:str):
        self.iGSN = iGSN
    
    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        self.name = name
    