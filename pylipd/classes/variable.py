
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.archivetype import ArchiveType
from pylipd.classes.paleovariable import PaleoVariable
from pylipd.classes.uncertainty import Uncertainty
from pylipd.classes.paleoproxy import PaleoProxy
from pylipd.classes.calibration import Calibration
from pylipd.classes.resolution import Resolution
from pylipd.classes.paleoproxygeneral import PaleoProxyGeneral
from pylipd.classes.compilation import Compilation
from pylipd.classes.paleounit import PaleoUnit
from pylipd.classes.interpretation import Interpretation

class Variable:

    def __init__(self):
        self.description: str = None
        self.instrument: None = None
        self.variableId: str = None
        self.name: str = None
        self.archiveType: ArchiveType = None
        self.missingValue: str = None
        self.foundInTable: None = None
        self.units: PaleoUnit = None
        self.proxyGeneral: PaleoProxyGeneral = None
        self.primary: bool = None
        self.partOfCompilation: Compilation = None
        self.physicalSample: None = None
        self.uncertainty: Uncertainty = None
        self.resolution: Resolution = None
        self.compilationNest: str = None
        self.standardVariable: PaleoVariable = None
        self.type: str = None
        self.meanValue: float = None
        self.notes: str = None
        self.composite: bool = None
        self.medianValue: float = None
        self.minValue: float = None
        self.calibratedVias: list[Calibration] = []
        self.foundInDataset: None = None
        self.values: list = None
        self.interpretations: list[Interpretation] = []
        self.proxy: PaleoProxy = None
        self.maxValue: float = None
        self.columnNumber: int = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Variable':
        self = Variable()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasUnits":

                for val in value:
                    obj = PaleoUnit.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.units = obj
        
            elif key == "hasMaxValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.maxValue = obj
        
            elif key == "isPrimary":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.primary = obj
        
            elif key == "hasUncertainty":

                for val in value:
                    if "@id" in val:
                        obj = Uncertainty.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.uncertainty = obj
        
            elif key == "hasProxy":

                for val in value:
                    obj = PaleoProxy.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.proxy = obj
        
            elif key == "hasColumnNumber":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.columnNumber = obj
        
            elif key == "hasDescription":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.description = obj
        
            elif key == "hasProxyGeneral":

                for val in value:
                    obj = PaleoProxyGeneral.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.proxyGeneral = obj
        
            elif key == "hasInstrument":

                for val in value:
                    obj = val["@id"]                        
                    self.instrument = obj
        
            elif key == "hasStandardVariable":

                for val in value:
                    obj = PaleoVariable.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.standardVariable = obj
        
            elif key == "hasVariableId":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableId = obj
        
            elif key == "hasMedianValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.medianValue = obj
        
            elif key == "isComposite":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.composite = obj
        
            elif key == "hasMeanValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.meanValue = obj
        
            elif key == "hasName":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "hasResolution":

                for val in value:
                    if "@id" in val:
                        obj = Resolution.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.resolution = obj
        
            elif key == "hasCompilationNest":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.compilationNest = obj
        
            elif key == "partOfCompilation":

                for val in value:
                    if "@id" in val:
                        obj = Compilation.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.partOfCompilation = obj
        
            elif key == "hasArchiveType":

                for val in value:
                    obj = ArchiveType.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.archiveType = obj
        
            elif key == "hasNotes":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasMinValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.minValue = obj
        
            elif key == "hasInterpretation":

                for val in value:
                    if "@id" in val:
                        obj = Interpretation.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.interpretations.append(obj)
        
            elif key == "foundInTable":

                for val in value:
                    obj = val["@id"]                        
                    self.foundInTable = obj
        
            elif key == "physicalSample":

                for val in value:
                    obj = val["@id"]                        
                    self.physicalSample = obj
        
            elif key == "hasValues":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.values = obj
        
            elif key == "hasMissingValue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.missingValue = obj
        
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
        
            elif key == "hasType":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.type = obj
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
        
    def getUnits(self) -> PaleoUnit:
        return self.units

    def setUnits(self, units:PaleoUnit):
        self.units = units

    def getMissingValue(self) -> str:
        return self.missingValue

    def setMissingValue(self, missingValue:str):
        self.missingValue = missingValue

    def getValues(self) -> list:
        return self.values

    def setValues(self, values:list):
        self.values = values

    def getMaxValue(self) -> float:
        return self.maxValue

    def setMaxValue(self, maxValue:float):
        self.maxValue = maxValue

    def getArchiveType(self) -> ArchiveType:
        return self.archiveType

    def setArchiveType(self, archiveType:ArchiveType):
        self.archiveType = archiveType

    def getPhysicalSample(self) -> None:
        return self.physicalSample

    def setPhysicalSample(self, physicalSample:None):
        self.physicalSample = physicalSample

    def getResolution(self) -> Resolution:
        return self.resolution

    def setResolution(self, resolution:Resolution):
        self.resolution = resolution

    def getStandardVariable(self) -> PaleoVariable:
        return self.standardVariable

    def setStandardVariable(self, standardVariable:PaleoVariable):
        self.standardVariable = standardVariable

    def getCalibratedVias(self) -> list[Calibration]:
        return self.calibratedVias

    def setCalibratedVias(self, calibratedVias:list[Calibration]):
        self.calibratedVias = calibratedVias

    def addCalibratedVia(self, calibratedVia:Calibration):
        self.calibratedVias.append(calibratedVia)
        
    def getMeanValue(self) -> float:
        return self.meanValue

    def setMeanValue(self, meanValue:float):
        self.meanValue = meanValue

    def isPrimary(self) -> bool:
        return self.primary

    def setPrimary(self, primary:bool):
        self.primary = primary

    def getProxyGeneral(self) -> PaleoProxyGeneral:
        return self.proxyGeneral

    def setProxyGeneral(self, proxyGeneral:PaleoProxyGeneral):
        self.proxyGeneral = proxyGeneral

    def isComposite(self) -> bool:
        return self.composite

    def setComposite(self, composite:bool):
        self.composite = composite

    def getDescription(self) -> str:
        return self.description

    def setDescription(self, description:str):
        self.description = description

    def getPartOfCompilation(self) -> Compilation:
        return self.partOfCompilation

    def setPartOfCompilation(self, partOfCompilation:Compilation):
        self.partOfCompilation = partOfCompilation

    def getVariableId(self) -> str:
        return self.variableId

    def setVariableId(self, variableId:str):
        self.variableId = variableId

    def getCompilationNest(self) -> str:
        return self.compilationNest

    def setCompilationNest(self, compilationNest:str):
        self.compilationNest = compilationNest

    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        self.name = name

    def getMinValue(self) -> float:
        return self.minValue

    def setMinValue(self, minValue:float):
        self.minValue = minValue

    def getUncertainty(self) -> Uncertainty:
        return self.uncertainty

    def setUncertainty(self, uncertainty:Uncertainty):
        self.uncertainty = uncertainty

    def getFoundInDataset(self) -> None:
        return self.foundInDataset

    def setFoundInDataset(self, foundInDataset:None):
        self.foundInDataset = foundInDataset

    def getInterpretations(self) -> list[Interpretation]:
        return self.interpretations

    def setInterpretations(self, interpretations:list[Interpretation]):
        self.interpretations = interpretations

    def addInterpretation(self, interpretation:Interpretation):
        self.interpretations.append(interpretation)
        
    def getColumnNumber(self) -> int:
        return self.columnNumber

    def setColumnNumber(self, columnNumber:int):
        self.columnNumber = columnNumber

    def getType(self) -> str:
        return self.type

    def setType(self, type:str):
        self.type = type

    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes

    def getFoundInTable(self) -> None:
        return self.foundInTable

    def setFoundInTable(self, foundInTable:None):
        self.foundInTable = foundInTable

    def getProxy(self) -> PaleoProxy:
        return self.proxy

    def setProxy(self, proxy:PaleoProxy):
        self.proxy = proxy

    def getInstrument(self) -> None:
        return self.instrument

    def setInstrument(self, instrument:None):
        self.instrument = instrument

    def getMedianValue(self) -> float:
        return self.medianValue

    def setMedianValue(self, medianValue:float):
        self.medianValue = medianValue
