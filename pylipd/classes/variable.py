
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.archivetype import ArchiveType
from pylipd.classes.calibration import Calibration
from pylipd.classes.compilation import Compilation
from pylipd.classes.interpretation import Interpretation
from pylipd.classes.paleoproxy import PaleoProxy
from pylipd.classes.paleoproxygeneral import PaleoProxyGeneral
from pylipd.classes.paleounit import PaleoUnit
from pylipd.classes.paleovariable import PaleoVariable
from pylipd.classes.resolution import Resolution
from pylipd.classes.uncertainty import Uncertainty

class Variable:

    def __init__(self):
        self.archiveType: ArchiveType = None
        self.calibratedVias: list[Calibration] = []
        self.columnNumber: int = None
        self.compilationNest: str = None
        self.composite: bool = None
        self.description: str = None
        self.foundInDataset: None = None
        self.foundInTable: None = None
        self.instrument: None = None
        self.interpretations: list[Interpretation] = []
        self.maxValue: float = None
        self.meanValue: float = None
        self.medianValue: float = None
        self.minValue: float = None
        self.missingValue: str = None
        self.name: str = None
        self.notes: str = None
        self.partOfCompilation: Compilation = None
        self.physicalSample: None = None
        self.primary: bool = None
        self.proxy: PaleoProxy = None
        self.proxyGeneral: PaleoProxyGeneral = None
        self.resolution: Resolution = None
        self.standardVariable: PaleoVariable = None
        self.uncertainty: Uncertainty = None
        self.units: PaleoUnit = None
        self.values: str = None
        self.variableId: str = None
        self.variableType: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Variable"
        self.id = self.ns + "/" + uniqid("Variable.")

    @staticmethod
    def from_data(id, data) -> 'Variable':
        self = Variable()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "calibratedVia":
                for val in value:
                    if "@id" in val:
                        obj = Calibration.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.calibratedVias.append(obj)
        
            elif key == "foundInDataset":
                for val in value:
                    obj = val["@id"]                        
                    self.foundInDataset = obj
        
            elif key == "foundInTable":
                for val in value:
                    obj = val["@id"]                        
                    self.foundInTable = obj
        
            elif key == "hasArchiveType":
                for val in value:
                    obj = ArchiveType.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.archiveType = obj
        
            elif key == "hasColumnNumber":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.columnNumber = obj
        
            elif key == "hasCompilationNest":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.compilationNest = obj
        
            elif key == "hasDescription":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.description = obj
        
            elif key == "hasInstrument":
                for val in value:
                    obj = val["@id"]                        
                    self.instrument = obj
        
            elif key == "hasInterpretation":
                for val in value:
                    if "@id" in val:
                        obj = Interpretation.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.interpretations.append(obj)
        
            elif key == "hasMaxValue":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.maxValue = obj
        
            elif key == "hasMeanValue":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.meanValue = obj
        
            elif key == "hasMedianValue":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.medianValue = obj
        
            elif key == "hasMinValue":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.minValue = obj
        
            elif key == "hasMissingValue":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.missingValue = obj
        
            elif key == "hasName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "hasNotes":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasProxy":
                for val in value:
                    obj = PaleoProxy.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.proxy = obj
        
            elif key == "hasProxyGeneral":
                for val in value:
                    obj = PaleoProxyGeneral.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.proxyGeneral = obj
        
            elif key == "hasResolution":
                for val in value:
                    if "@id" in val:
                        obj = Resolution.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.resolution = obj
        
            elif key == "hasStandardVariable":
                for val in value:
                    obj = PaleoVariable.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.standardVariable = obj
        
            elif key == "hasType":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableType = obj
        
            elif key == "hasUncertainty":
                for val in value:
                    if "@id" in val:
                        obj = Uncertainty.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.uncertainty = obj
        
            elif key == "hasUnits":
                for val in value:
                    obj = PaleoUnit.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.units = obj
        
            elif key == "hasValues":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.values = obj
        
            elif key == "hasVariableId":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableId = obj
        
            elif key == "isComposite":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.composite = obj
        
            elif key == "isPrimary":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.primary = obj
        
            elif key == "partOfCompilation":
                for val in value:
                    if "@id" in val:
                        obj = Compilation.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.partOfCompilation = obj
        
            elif key == "physicalSample":
                for val in value:
                    obj = val["@id"]                        
                    self.physicalSample = obj
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

        if len(self.calibratedVias):
            data[self.id]["calibratedVia"] = []
        for value_obj in self.calibratedVias: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["calibratedVia"].append(obj)

        if len(self.interpretations):
            data[self.id]["hasInterpretation"] = []
        for value_obj in self.interpretations: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasInterpretation"].append(obj)

        if self.archiveType:
            value_obj = self.archiveType 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasArchiveType"] = [obj]
                

        if self.columnNumber:
            value_obj = self.columnNumber
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#integer"
            }
            data[self.id]["hasColumnNumber"] = [obj]
                

        if self.compilationNest:
            value_obj = self.compilationNest
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCompilationNest"] = [obj]
                

        if self.composite:
            value_obj = self.composite
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#boolean"
            }
            data[self.id]["isComposite"] = [obj]
                

        if self.description:
            value_obj = self.description
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDescription"] = [obj]
                

        if self.foundInDataset:
            value_obj = self.foundInDataset
            obj = {
                "@id": value_obj,
                "@type": "uri"
            }
            data[self.id]["foundInDataset"] = [obj]
                

        if self.foundInTable:
            value_obj = self.foundInTable
            obj = {
                "@id": value_obj,
                "@type": "uri"
            }
            data[self.id]["foundInTable"] = [obj]
                

        if self.instrument:
            value_obj = self.instrument
            obj = {
                "@id": value_obj,
                "@type": "uri"
            }
            data[self.id]["hasInstrument"] = [obj]
                

        if self.maxValue:
            value_obj = self.maxValue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#float"
            }
            data[self.id]["hasMaxValue"] = [obj]
                

        if self.meanValue:
            value_obj = self.meanValue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#float"
            }
            data[self.id]["hasMeanValue"] = [obj]
                

        if self.medianValue:
            value_obj = self.medianValue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#float"
            }
            data[self.id]["hasMedianValue"] = [obj]
                

        if self.minValue:
            value_obj = self.minValue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#float"
            }
            data[self.id]["hasMinValue"] = [obj]
                

        if self.missingValue:
            value_obj = self.missingValue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasMissingValue"] = [obj]
                

        if self.name:
            value_obj = self.name
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasName"] = [obj]
                

        if self.notes:
            value_obj = self.notes
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"] = [obj]
                

        if self.partOfCompilation:
            value_obj = self.partOfCompilation 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["partOfCompilation"] = [obj]
                

        if self.physicalSample:
            value_obj = self.physicalSample
            obj = {
                "@id": value_obj,
                "@type": "uri"
            }
            data[self.id]["physicalSample"] = [obj]
                

        if self.primary:
            value_obj = self.primary
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#boolean"
            }
            data[self.id]["isPrimary"] = [obj]
                

        if self.proxy:
            value_obj = self.proxy 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasProxy"] = [obj]
                

        if self.proxyGeneral:
            value_obj = self.proxyGeneral 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasProxyGeneral"] = [obj]
                

        if self.resolution:
            value_obj = self.resolution 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasResolution"] = [obj]
                

        if self.standardVariable:
            value_obj = self.standardVariable 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasStandardVariable"] = [obj]
                

        if self.uncertainty:
            value_obj = self.uncertainty 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasUncertainty"] = [obj]
                

        if self.units:
            value_obj = self.units 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasUnits"] = [obj]
                

        if self.values:
            value_obj = self.values
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasValues"] = [obj]
                

        if self.variableId:
            value_obj = self.variableId
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasVariableId"] = [obj]
                

        if self.variableType:
            value_obj = self.variableType
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasType"] = [obj]
                
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
        
    def getArchiveType(self) -> ArchiveType:
        return self.archiveType

    def setArchiveType(self, archiveType:ArchiveType):
        self.archiveType = archiveType
    
    def getCalibratedVias(self) -> list[Calibration]:
        return self.calibratedVias

    def setCalibratedVias(self, calibratedVias:list[Calibration]):
        self.calibratedVias = calibratedVias

    def addCalibratedVia(self, calibratedVias:Calibration):
        self.calibratedVias.append(calibratedVias)
        
    def getColumnNumber(self) -> int:
        return self.columnNumber

    def setColumnNumber(self, columnNumber:int):
        self.columnNumber = columnNumber
    
    def getCompilationNest(self) -> str:
        return self.compilationNest

    def setCompilationNest(self, compilationNest:str):
        self.compilationNest = compilationNest
    
    def getDescription(self) -> str:
        return self.description

    def setDescription(self, description:str):
        self.description = description
    
    def getFoundInDataset(self) -> None:
        return self.foundInDataset

    def setFoundInDataset(self, foundInDataset:None):
        self.foundInDataset = foundInDataset
    
    def getFoundInTable(self) -> None:
        return self.foundInTable

    def setFoundInTable(self, foundInTable:None):
        self.foundInTable = foundInTable
    
    def getInstrument(self) -> None:
        return self.instrument

    def setInstrument(self, instrument:None):
        self.instrument = instrument
    
    def getInterpretations(self) -> list[Interpretation]:
        return self.interpretations

    def setInterpretations(self, interpretations:list[Interpretation]):
        self.interpretations = interpretations

    def addInterpretation(self, interpretations:Interpretation):
        self.interpretations.append(interpretations)
        
    def getMaxValue(self) -> float:
        return self.maxValue

    def setMaxValue(self, maxValue:float):
        self.maxValue = maxValue
    
    def getMeanValue(self) -> float:
        return self.meanValue

    def setMeanValue(self, meanValue:float):
        self.meanValue = meanValue
    
    def getMedianValue(self) -> float:
        return self.medianValue

    def setMedianValue(self, medianValue:float):
        self.medianValue = medianValue
    
    def getMinValue(self) -> float:
        return self.minValue

    def setMinValue(self, minValue:float):
        self.minValue = minValue
    
    def getMissingValue(self) -> str:
        return self.missingValue

    def setMissingValue(self, missingValue:str):
        self.missingValue = missingValue
    
    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        self.name = name
    
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes
    
    def getPartOfCompilation(self) -> Compilation:
        return self.partOfCompilation

    def setPartOfCompilation(self, partOfCompilation:Compilation):
        self.partOfCompilation = partOfCompilation
    
    def getPhysicalSample(self) -> None:
        return self.physicalSample

    def setPhysicalSample(self, physicalSample:None):
        self.physicalSample = physicalSample
    
    def getProxy(self) -> PaleoProxy:
        return self.proxy

    def setProxy(self, proxy:PaleoProxy):
        self.proxy = proxy
    
    def getProxyGeneral(self) -> PaleoProxyGeneral:
        return self.proxyGeneral

    def setProxyGeneral(self, proxyGeneral:PaleoProxyGeneral):
        self.proxyGeneral = proxyGeneral
    
    def getResolution(self) -> Resolution:
        return self.resolution

    def setResolution(self, resolution:Resolution):
        self.resolution = resolution
    
    def getStandardVariable(self) -> PaleoVariable:
        return self.standardVariable

    def setStandardVariable(self, standardVariable:PaleoVariable):
        self.standardVariable = standardVariable
    
    def getUncertainty(self) -> Uncertainty:
        return self.uncertainty

    def setUncertainty(self, uncertainty:Uncertainty):
        self.uncertainty = uncertainty
    
    def getUnits(self) -> PaleoUnit:
        return self.units

    def setUnits(self, units:PaleoUnit):
        self.units = units
    
    def getValues(self) -> str:
        return self.values

    def setValues(self, values:str):
        self.values = values
    
    def getVariableId(self) -> str:
        return self.variableId

    def setVariableId(self, variableId:str):
        self.variableId = variableId
    
    def getVariableType(self) -> str:
        return self.variableType

    def setVariableType(self, variableType:str):
        self.variableType = variableType
    
    def isComposite(self) -> bool:
        return self.composite

    def setComposite(self, composite:bool):
        self.composite = composite
    
    def isPrimary(self) -> bool:
        return self.primary

    def setPrimary(self, primary:bool):
        self.primary = primary
    