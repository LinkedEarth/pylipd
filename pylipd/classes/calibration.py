
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.uncertainty import Uncertainty

class Calibration:

    def __init__(self):
        self.uncertainty: str = None
        self.uncertainty: Uncertainty = None
        self.notes: str = None
        self.seasonality: str = None
        self.targetDataset: str = None
        self.dOI: str = None
        self.proxyDataset: str = None
        self.equation: str = None
        self.datasetRange: str = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Calibration':
        self = Calibration()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasUncertainty":

                for val in value:
                    if "@id" in val:
                        obj = Uncertainty.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.uncertainty = obj
        
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
        
            elif key == "seasonality":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.seasonality = obj
        
            elif key == "hasNotes":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasDOI":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.dOI = obj
        
            elif key == "hasTargetDataset":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.targetDataset = obj
        
            elif key == "hasDatasetRange":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.datasetRange = obj
        
            elif key == "hasProxyDataset":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.proxyDataset = obj
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
        
    def getUncertainty(self) -> Uncertainty:
        return self.uncertainty

    def setUncertainty(self, uncertainty:Uncertainty):
        self.uncertainty = uncertainty

    def getTargetDataset(self) -> str:
        return self.targetDataset

    def setTargetDataset(self, targetDataset:str):
        self.targetDataset = targetDataset

    def getDatasetRange(self) -> str:
        return self.datasetRange

    def setDatasetRange(self, datasetRange:str):
        self.datasetRange = datasetRange

    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes

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

    def getDOI(self) -> str:
        return self.dOI

    def setDOI(self, dOI:str):
        self.dOI = dOI
