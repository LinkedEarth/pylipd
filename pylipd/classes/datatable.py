
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.variable import Variable

class DataTable:

    def __init__(self):
        self.fileName: str = None
        self.missingValue: str = None
        self.variables: list[Variable] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#DataTable"
        self.id = self.ns + "/" + uniqid("DataTable.")

    @staticmethod
    def from_data(id, data) -> 'DataTable':
        self = DataTable()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
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

        if len(self.variables):
            data[self.id]["hasVariable"] = []
        for value_obj in self.variables: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasVariable"].append(obj)

        if self.fileName:
            value_obj = self.fileName
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasFileName"] = [obj]
                

        if self.missingValue:
            value_obj = self.missingValue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasMissingValue"] = [obj]
                
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

    def addVariable(self, variables:Variable):
        self.variables.append(variables)
        