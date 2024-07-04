
##############################
# Auto-generated. Do not Edit
##############################

import re

class IndependentVariable:

    def __init__(self):
        self.rank: str = None
        self.relevantQuote: str = None
        self.interpretationDirection: str = None
        self.equation: str = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'IndependentVariable':
        self = IndependentVariable()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "equation":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equation = obj
        
            elif key == "interpretationDirection":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.interpretationDirection = obj
        
            elif key == "hasRank":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.rank = obj
        
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
        
    def getInterpretationDirection(self) -> str:
        return self.interpretationDirection

    def setInterpretationDirection(self, interpretationDirection:str):
        self.interpretationDirection = interpretationDirection

    def getRelevantQuote(self) -> str:
        return self.relevantQuote

    def setRelevantQuote(self, relevantQuote:str):
        self.relevantQuote = relevantQuote

    def getEquation(self) -> str:
        return self.equation

    def setEquation(self, equation:str):
        self.equation = equation

    def getRank(self) -> str:
        return self.rank

    def setRank(self, rank:str):
        self.rank = rank
