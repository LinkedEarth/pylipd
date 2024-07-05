
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid

class IndependentVariable:

    def __init__(self):
        self.equation: str = None
        self.interpretationDirection: str = None
        self.rank: str = None
        self.relevantQuote: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#IndependentVariable"
        self.id = self.ns + "/" + uniqid("IndependentVariable.")

    @staticmethod
    def from_data(id, data) -> 'IndependentVariable':
        self = IndependentVariable()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "equation":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equation = obj
        
            elif key == "hasRank":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.rank = obj
        
            elif key == "interpretationDirection":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.interpretationDirection = obj
        
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

        if self.equation:
            value_obj = self.equation
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["equation"] = [obj]
                

        if self.interpretationDirection:
            value_obj = self.interpretationDirection
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["interpretationDirection"] = [obj]
                

        if self.rank:
            value_obj = self.rank
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasRank"] = [obj]
                

        if self.relevantQuote:
            value_obj = self.relevantQuote
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["relevantQuote"] = [obj]
                
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

        if self.equation:
            value_obj = self.equation
            obj = value_obj
            data["mathematicalRelation"] = obj

        if self.interpretationDirection:
            value_obj = self.interpretationDirection
            obj = value_obj
            data["direction"] = obj

        if self.rank:
            value_obj = self.rank
            obj = value_obj
            data["rank"] = obj

        if self.relevantQuote:
            value_obj = self.relevantQuote
            obj = value_obj
            data["basis"] = obj

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
        
    def getEquation(self) -> str:
        return self.equation

    def setEquation(self, equation:str):
        self.equation = equation
    
    def getInterpretationDirection(self) -> str:
        return self.interpretationDirection

    def setInterpretationDirection(self, interpretationDirection:str):
        self.interpretationDirection = interpretationDirection
    
    def getRank(self) -> str:
        return self.rank

    def setRank(self, rank:str):
        self.rank = rank
    
    def getRelevantQuote(self) -> str:
        return self.relevantQuote

    def setRelevantQuote(self, relevantQuote:str):
        self.relevantQuote = relevantQuote
    