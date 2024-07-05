
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid

class Calibration:

    def __init__(self):
        self.dOI: str = None
        self.datasetRange: str = None
        self.equation: str = None
        self.notes: str = None
        self.proxyDataset: str = None
        self.seasonality: str = None
        self.targetDataset: str = None
        self.uncertainty: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Calibration"
        self.id = self.ns + "/" + uniqid("Calibration.")

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
        
            elif key == "hasDOI":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.dOI = obj
        
            elif key == "hasDatasetRange":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.datasetRange = obj
        
            elif key == "hasEquation":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equation = obj
        
            elif key == "hasNotes":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasProxyDataset":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.proxyDataset = obj
        
            elif key == "hasTargetDataset":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.targetDataset = obj
        
            elif key == "hasUncertainty":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.uncertainty = obj
        
            elif key == "seasonality":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.seasonality = obj
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

        if self.dOI:
            value_obj = self.dOI
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDOI"] = [obj]
                

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDatasetRange"] = [obj]
                

        if self.equation:
            value_obj = self.equation
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasEquation"] = [obj]
                

        if self.notes:
            value_obj = self.notes
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"] = [obj]
                

        if self.proxyDataset:
            value_obj = self.proxyDataset
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasProxyDataset"] = [obj]
                

        if self.seasonality:
            value_obj = self.seasonality
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["seasonality"] = [obj]
                

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
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasUncertainty"] = [obj]
                
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

        if self.dOI:
            value_obj = self.dOI
            obj = value_obj
            data["doi"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["datasetRange"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["equationIntercept"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["equationR2"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["equationSlope"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["equationSlopeUncertainty"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["method"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["methodDetail"] = obj

        if self.equation:
            value_obj = self.equation
            obj = value_obj
            data["equation"] = obj

        if self.notes:
            value_obj = self.notes
            obj = value_obj
            data["notes"] = obj

        if self.proxyDataset:
            value_obj = self.proxyDataset
            obj = value_obj
            data["proxyDataset"] = obj

        if self.seasonality:
            value_obj = self.seasonality
            obj = value_obj
            data["hasSeasonality"] = obj

        if self.targetDataset:
            value_obj = self.targetDataset
            obj = value_obj
            data["targetDataset"] = obj

        if self.uncertainty:
            value_obj = self.uncertainty
            obj = value_obj
            data["uncertainty"] = obj

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
        
    def getDOI(self) -> str:
        return self.dOI

    def setDOI(self, dOI:str):
        self.dOI = dOI
    
    def getDatasetRange(self) -> str:
        return self.datasetRange

    def setDatasetRange(self, datasetRange:str):
        self.datasetRange = datasetRange
    
    def getEquation(self) -> str:
        return self.equation

    def setEquation(self, equation:str):
        self.equation = equation
    
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes
    
    def getProxyDataset(self) -> str:
        return self.proxyDataset

    def setProxyDataset(self, proxyDataset:str):
        self.proxyDataset = proxyDataset
    
    def getSeasonality(self) -> str:
        return self.seasonality

    def setSeasonality(self, seasonality:str):
        self.seasonality = seasonality
    
    def getTargetDataset(self) -> str:
        return self.targetDataset

    def setTargetDataset(self, targetDataset:str):
        self.targetDataset = targetDataset
    
    def getUncertainty(self) -> str:
        return self.uncertainty

    def setUncertainty(self, uncertainty:str):
        self.uncertainty = uncertainty
    