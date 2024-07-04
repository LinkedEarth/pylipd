
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.uncertainty import Uncertainty

class Calibration:

    def __init__(self):
        self.proxyDataset: str = None
        self.datasetRange: str = None
        self.dOI: str = None
        self.targetDataset: str = None
        self.uncertainty: Uncertainty = None
        self.notes: str = None
        self.uncertainty: str = None
        self.equation: str = None
        self.seasonality: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Calibration"
        self.id = self.ns + "/" + uniqid("Calibration")

    @staticmethod
    def from_data(id, data) -> 'Calibration':
        self = Calibration()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasTargetDataset":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.targetDataset = obj
        
            elif key == "hasProxyDataset":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.proxyDataset = obj
        
            elif key == "hasDatasetRange":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.datasetRange = obj
        
            elif key == "hasNotes":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasUncertainty":

                for val in value:
                    if "@id" in val:
                        obj = Uncertainty.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.uncertainty = obj
        
            elif key == "seasonality":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.seasonality = obj
        
            elif key == "hasEquation":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equation = obj
        
            elif key == "hasUncertainty":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.uncertainty = obj
        
            elif key == "hasDOI":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.dOI = obj
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

        
        if self.notes:
            value_obj = self.notes
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"] = [obj]
            
        
        if self.seasonality:
            value_obj = self.seasonality
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["seasonality"] = [obj]
            
        
        if self.datasetRange:
            value_obj = self.datasetRange
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDatasetRange"] = [obj]
            
        
        if self.proxyDataset:
            value_obj = self.proxyDataset
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasProxyDataset"] = [obj]
            
        
        if self.targetDataset:
            value_obj = self.targetDataset
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasTargetDataset"] = [obj]
            
        
        if self.uncertainty:
            value_obj = self.uncertainty 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            
            data[self.id]["hasUncertainty"] = [obj]
            
        
        if self.equation:
            value_obj = self.equation
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasEquation"] = [obj]
            
        
        if self.uncertainty:
            value_obj = self.uncertainty
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasUncertainty"] = [obj]
            
        
        if self.dOI:
            value_obj = self.dOI
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDOI"] = [obj]
            

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
        
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes

    def getTargetDataset(self) -> str:
        return self.targetDataset

    def setTargetDataset(self, targetDataset:str):
        self.targetDataset = targetDataset

    def getEquation(self) -> str:
        return self.equation

    def setEquation(self, equation:str):
        self.equation = equation

    def getUncertainty(self) -> str:
        return self.uncertainty

    def setUncertainty(self, uncertainty:str):
        self.uncertainty = uncertainty

    def getSeasonality(self) -> str:
        return self.seasonality

    def setSeasonality(self, seasonality:str):
        self.seasonality = seasonality

    def getProxyDataset(self) -> str:
        return self.proxyDataset

    def setProxyDataset(self, proxyDataset:str):
        self.proxyDataset = proxyDataset

    def getUncertainty(self) -> Uncertainty:
        return self.uncertainty

    def setUncertainty(self, uncertainty:Uncertainty):
        self.uncertainty = uncertainty

    def getDOI(self) -> str:
        return self.dOI

    def setDOI(self, dOI:str):
        self.dOI = dOI

    def getDatasetRange(self) -> str:
        return self.datasetRange

    def setDatasetRange(self, datasetRange:str):
        self.datasetRange = datasetRange
