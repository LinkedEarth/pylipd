
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.person import Person

class Funding:

    def __init__(self):
        self.fundingCountry: str = None
        self.fundingAgency: str = None
        self.investigators: list[Person] = []
        self.grants: list[str] = []
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Funding':
        self = Funding()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasGrant":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.grants.append(obj)
        
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
        
    def getInvestigators(self) -> list[Person]:
        return self.investigators

    def setInvestigators(self, investigators:list[Person]):
        self.investigators = investigators

    def addInvestigator(self, investigator:Person):
        self.investigators.append(investigator)
        
    def getFundingAgency(self) -> str:
        return self.fundingAgency

    def setFundingAgency(self, fundingAgency:str):
        self.fundingAgency = fundingAgency

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
