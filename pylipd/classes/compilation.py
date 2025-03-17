
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid

class Compilation:

    def __init__(self):
        self.name: str = None
        self.version: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Compilation"
        self.id = self.ns + "/" + uniqid("Compilation.")

    @staticmethod
    def from_data(id, data) -> 'Compilation':
        self = Compilation()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "hasVersion":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.version = obj
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

        if self.name:
            value_obj = self.name
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasName"] = [obj]
                

        if self.version:
            value_obj = self.version
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasVersion"] = [obj]
                
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
                if re.match(r"\d{4}-\d{2}-\d{2}( |T)\d{2}:\d{2}:\d{2}", value):
                    ptype = "http://www.w3.org/2001/XMLSchema#datetime"   
                elif re.match(r"\d{4}-\d{2}-\d{2}", value):
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

        if self.name:
            value_obj = self.name
            obj = value_obj
            data["compilationName"] = obj

        if self.version:
            value_obj = self.version
            obj = value_obj
            data["compilationVersion"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Compilation':
        self = Compilation()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "compilationName":
                    value = pvalue
                    obj = value
                    self.name = obj
            elif key == "compilationVersion":
                    value = pvalue
                    obj = value
                    self.version = obj
            else:
                self.set_non_standard_property(key, pvalue)
                   
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
        
    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        self.name = name
    
    def getVersion(self) -> str:
        return self.version

    def setVersion(self, version:str):
        self.version = version
    