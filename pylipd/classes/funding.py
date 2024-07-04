
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.person import Person

class Funding:

    def __init__(self):
        self.fundingCountry: str = None
        self.grants: list[str] = []
        self.investigators: list[Person] = []
        self.fundingAgency: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Funding"
        self.id = self.ns + "/" + uniqid("Funding")

    @staticmethod
    def from_data(id, data) -> 'Funding':
        self = Funding()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasFundingAgency":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.fundingAgency = obj
        
            elif key == "hasFundingCountry":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.fundingCountry = obj
        
            elif key == "hasInvestigator":

                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.investigators.append(obj)
        
            elif key == "hasGrant":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.grants.append(obj)
            else:
                for val in value:
                    obj = None
                    if "@id" in val:
                        obj = mydata[val["@id"]]
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

        
        if len(self.investigators):
            data[self.id]["hasInvestigator"] = []
        for value_obj in self.investigators: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            
            data[self.id]["hasInvestigator"].append(obj)
        
        if self.fundingCountry:
            value_obj = self.fundingCountry
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasFundingCountry"] = [obj]
            
        
        if len(self.grants):
            data[self.id]["hasGrant"] = []
        for value_obj in self.grants:
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasGrant"].append(obj)
        
        if self.fundingAgency:
            value_obj = self.fundingAgency
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasFundingAgency"] = [obj]
            

        for key in self.misc:
            value = self.misc[key]
            data[self.id][key] = []
            ptype = None
            tp = type(value).__name__
            if tp == "int":
                ptype = "http://www.w3.org/2001/XMLSchema#integer"
            elif tp == "float":
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
        
    def getGrants(self) -> list[str]:
        return self.grants

    def setGrants(self, grants:list[str]):
        self.grants = grants

    def addGrant(self, grant:str):
        self.grants.append(grant)
        
    def getFundingCountry(self) -> str:
        return self.fundingCountry

    def setFundingCountry(self, fundingCountry:str):
        self.fundingCountry = fundingCountry

    def getFundingAgency(self) -> str:
        return self.fundingAgency

    def setFundingAgency(self, fundingAgency:str):
        self.fundingAgency = fundingAgency

    def getInvestigators(self) -> list[Person]:
        return self.investigators

    def setInvestigators(self, investigators:list[Person]):
        self.investigators = investigators

    def addInvestigator(self, investigator:Person):
        self.investigators.append(investigator)
        