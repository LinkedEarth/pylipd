
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.independentvariable import IndependentVariable
from pylipd.classes.paleounit import PaleoUnit

class IntegrationTime:

    def __init__(self):
        self.independentVariables: list[IndependentVariable] = []
        self.relevantQuote: str = None
        self.units: PaleoUnit = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#IntegrationTime"
        self.id = self.ns + "/" + uniqid("IntegrationTime.")

    @staticmethod
    def from_data(id, data) -> 'IntegrationTime':
        self = IntegrationTime()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
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

        if len(self.independentVariables):
            data[self.id]["hasIndependentVariable"] = []
        for value_obj in self.independentVariables: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasIndependentVariable"].append(obj)

        if self.relevantQuote:
            value_obj = self.relevantQuote
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["relevantQuote"] = [obj]
                

        if self.units:
            value_obj = self.units 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasUnits"] = [obj]
                
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

        if len(self.independentVariables):
            data["independentVariable"] = []
        for value_obj in self.independentVariables:
            if hasattr(value_obj, "to_json"):
                obj = value_obj.to_json()
            else:
                obj = value_obj
            data["independentVariable"].append(obj)

        if self.relevantQuote:
            value_obj = self.relevantQuote
            obj = value_obj
            data["basis"] = obj

        if self.units:
            value_obj = self.units
            if hasattr(value_obj, "to_json"):
                obj = value_obj.to_json()
            else:
                obj = value_obj
            data["units"] = obj

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
        
    def getIndependentVariables(self) -> list[IndependentVariable]:
        return self.independentVariables

    def setIndependentVariables(self, independentVariables:list[IndependentVariable]):
        self.independentVariables = independentVariables

    def addIndependentVariable(self, independentVariables:IndependentVariable):
        self.independentVariables.append(independentVariables)
        
    def getRelevantQuote(self) -> str:
        return self.relevantQuote

    def setRelevantQuote(self, relevantQuote:str):
        self.relevantQuote = relevantQuote
    
    def getUnits(self) -> PaleoUnit:
        return self.units

    def setUnits(self, units:PaleoUnit):
        self.units = units
    