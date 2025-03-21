
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
        self.equationIntercept: str = None
        self.equationR2: str = None
        self.equationSlope: str = None
        self.equationSlopeUncertainty: str = None
        self.method: str = None
        self.methodDetail: str = None
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
        
            elif key == "hasEquationIntercept":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equationIntercept = obj
        
            elif key == "hasEquationR2":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equationR2 = obj
        
            elif key == "hasEquationSlope":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equationSlope = obj
        
            elif key == "hasEquationSlopeUncertainty":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.equationSlopeUncertainty = obj
        
            elif key == "hasMethod":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.method = obj
        
            elif key == "hasMethodDetail":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.methodDetail = obj
        
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
                

        if self.equationIntercept:
            value_obj = self.equationIntercept
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasEquationIntercept"] = [obj]
                

        if self.equationR2:
            value_obj = self.equationR2
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasEquationR2"] = [obj]
                

        if self.equationSlope:
            value_obj = self.equationSlope
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasEquationSlope"] = [obj]
                

        if self.equationSlopeUncertainty:
            value_obj = self.equationSlopeUncertainty
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasEquationSlopeUncertainty"] = [obj]
                

        if self.method:
            value_obj = self.method
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasMethod"] = [obj]
                

        if self.methodDetail:
            value_obj = self.methodDetail
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasMethodDetail"] = [obj]
                

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

        if self.dOI:
            value_obj = self.dOI
            obj = value_obj
            data["doi"] = obj

        if self.datasetRange:
            value_obj = self.datasetRange
            obj = value_obj
            data["datasetRange"] = obj

        if self.equation:
            value_obj = self.equation
            obj = value_obj
            data["equation"] = obj

        if self.equationIntercept:
            value_obj = self.equationIntercept
            obj = value_obj
            data["equationIntercept"] = obj

        if self.equationR2:
            value_obj = self.equationR2
            obj = value_obj
            data["equationR2"] = obj

        if self.equationSlope:
            value_obj = self.equationSlope
            obj = value_obj
            data["equationSlope"] = obj

        if self.equationSlopeUncertainty:
            value_obj = self.equationSlopeUncertainty
            obj = value_obj
            data["equationSlopeUncertainty"] = obj

        if self.method:
            value_obj = self.method
            obj = value_obj
            data["method"] = obj

        if self.methodDetail:
            value_obj = self.methodDetail
            obj = value_obj
            data["methodDetail"] = obj

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

    @staticmethod
    def from_json(data) -> 'Calibration':
        self = Calibration()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "datasetRange":
                    value = pvalue
                    obj = value
                    self.datasetRange = obj
            elif key == "doi":
                    value = pvalue
                    obj = value
                    self.dOI = obj
            elif key == "equation":
                    value = pvalue
                    obj = value
                    self.equation = obj
            elif key == "equationIntercept":
                    value = pvalue
                    obj = value
                    self.equationIntercept = obj
            elif key == "equationR2":
                    value = pvalue
                    obj = value
                    self.equationR2 = obj
            elif key == "equationSlope":
                    value = pvalue
                    obj = value
                    self.equationSlope = obj
            elif key == "equationSlopeUncertainty":
                    value = pvalue
                    obj = value
                    self.equationSlopeUncertainty = obj
            elif key == "hasSeasonality":
                    value = pvalue
                    obj = value
                    self.seasonality = obj
            elif key == "method":
                    value = pvalue
                    obj = value
                    self.method = obj
            elif key == "methodDetail":
                    value = pvalue
                    obj = value
                    self.methodDetail = obj
            elif key == "notes":
                    value = pvalue
                    obj = value
                    self.notes = obj
            elif key == "proxyDataset":
                    value = pvalue
                    obj = value
                    self.proxyDataset = obj
            elif key == "targetDataset":
                    value = pvalue
                    obj = value
                    self.targetDataset = obj
            elif key == "uncertainty":
                    value = pvalue
                    obj = value
                    self.uncertainty = obj
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
        
    def getDOI(self) -> str:
        return self.dOI

    def setDOI(self, dOI:str):
        assert isinstance(dOI, str), "Property dOI is not of type str"
        self.dOI = dOI
    
    def getDatasetRange(self) -> str:
        return self.datasetRange

    def setDatasetRange(self, datasetRange:str):
        assert isinstance(datasetRange, str), "Property datasetRange is not of type str"
        self.datasetRange = datasetRange
    
    def getEquation(self) -> str:
        return self.equation

    def setEquation(self, equation:str):
        assert isinstance(equation, str), "Property equation is not of type str"
        self.equation = equation
    
    def getEquationIntercept(self) -> str:
        return self.equationIntercept

    def setEquationIntercept(self, equationIntercept:str):
        assert isinstance(equationIntercept, str), "Property equationIntercept is not of type str"
        self.equationIntercept = equationIntercept
    
    def getEquationR2(self) -> str:
        return self.equationR2

    def setEquationR2(self, equationR2:str):
        assert isinstance(equationR2, str), "Property equationR2 is not of type str"
        self.equationR2 = equationR2
    
    def getEquationSlope(self) -> str:
        return self.equationSlope

    def setEquationSlope(self, equationSlope:str):
        assert isinstance(equationSlope, str), "Property equationSlope is not of type str"
        self.equationSlope = equationSlope
    
    def getEquationSlopeUncertainty(self) -> str:
        return self.equationSlopeUncertainty

    def setEquationSlopeUncertainty(self, equationSlopeUncertainty:str):
        assert isinstance(equationSlopeUncertainty, str), "Property equationSlopeUncertainty is not of type str"
        self.equationSlopeUncertainty = equationSlopeUncertainty
    
    def getMethod(self) -> str:
        return self.method

    def setMethod(self, method:str):
        assert isinstance(method, str), "Property method is not of type str"
        self.method = method
    
    def getMethodDetail(self) -> str:
        return self.methodDetail

    def setMethodDetail(self, methodDetail:str):
        assert isinstance(methodDetail, str), "Property methodDetail is not of type str"
        self.methodDetail = methodDetail
    
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        assert isinstance(notes, str), "Property notes is not of type str"
        self.notes = notes
    
    def getProxyDataset(self) -> str:
        return self.proxyDataset

    def setProxyDataset(self, proxyDataset:str):
        assert isinstance(proxyDataset, str), "Property proxyDataset is not of type str"
        self.proxyDataset = proxyDataset
    
    def getSeasonality(self) -> str:
        return self.seasonality

    def setSeasonality(self, seasonality:str):
        assert isinstance(seasonality, str), "Property seasonality is not of type str"
        self.seasonality = seasonality
    
    def getTargetDataset(self) -> str:
        return self.targetDataset

    def setTargetDataset(self, targetDataset:str):
        assert isinstance(targetDataset, str), "Property targetDataset is not of type str"
        self.targetDataset = targetDataset
    
    def getUncertainty(self) -> str:
        return self.uncertainty

    def setUncertainty(self, uncertainty:str):
        assert isinstance(uncertainty, str), "Property uncertainty is not of type str"
        self.uncertainty = uncertainty
    