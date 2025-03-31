
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
from pylipd.classes.physicalsample import PhysicalSample
from pylipd.classes.resolution import Resolution

class Variable:

    def __init__(self):
        self.archiveType: ArchiveType = None
        self.calibratedVias: list[Calibration] = []
        self.columnNumber: int = None
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
        self.physicalSamples: list[PhysicalSample] = []
        self.primary: bool = None
        self.proxy: PaleoProxy = None
        self.proxyGeneral: PaleoProxyGeneral = None
        self.resolution: Resolution = None
        self.standardVariable: PaleoVariable = None
        self.uncertainty: str = None
        self.uncertaintyAnalytical: str = None
        self.uncertaintyReproducibility: str = None
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
        
            elif key == "hasPhysicalSample":
                for val in value:
                    if "@id" in val:
                        obj = PhysicalSample.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.physicalSamples.append(obj)
        
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
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.uncertainty = obj
        
            elif key == "hasUncertaintyAnalytical":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.uncertaintyAnalytical = obj
        
            elif key == "hasUncertaintyReproducibility":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.uncertaintyReproducibility = obj
        
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
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["calibratedVia"].append(obj)

        if len(self.interpretations):
            data[self.id]["hasInterpretation"] = []
        for value_obj in self.interpretations:
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["hasInterpretation"].append(obj)

        if len(self.physicalSamples):
            data[self.id]["hasPhysicalSample"] = []
        for value_obj in self.physicalSamples:
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["hasPhysicalSample"].append(obj)

        if self.archiveType:
            value_obj = self.archiveType
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
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
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["partOfCompilation"] = [obj]
                

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
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["hasProxy"] = [obj]
                

        if self.proxyGeneral:
            value_obj = self.proxyGeneral
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["hasProxyGeneral"] = [obj]
                

        if self.resolution:
            value_obj = self.resolution
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["hasResolution"] = [obj]
                

        if self.standardVariable:
            value_obj = self.standardVariable
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
                obj = {
                    "@id": value_obj.id,
                    "@type": "uri"
                }
                data = value_obj.to_data(data)
            data[self.id]["hasStandardVariable"] = [obj]
                

        if self.uncertainty:
            value_obj = self.uncertainty
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasUncertainty"] = [obj]
                

        if self.uncertaintyAnalytical:
            value_obj = self.uncertaintyAnalytical
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasUncertaintyAnalytical"] = [obj]
                

        if self.uncertaintyReproducibility:
            value_obj = self.uncertaintyReproducibility
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasUncertaintyReproducibility"] = [obj]
                

        if self.units:
            value_obj = self.units
            if type(value_obj) is str:
                obj = {
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }
            else:
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

        if len(self.calibratedVias):
            data["calibration"] = []
        for value_obj in self.calibratedVias:
            obj = value_obj.to_json()
            data["calibration"].append(obj)

        if len(self.interpretations):
            data["interpretation"] = []
        for value_obj in self.interpretations:
            obj = value_obj.to_json()
            data["interpretation"].append(obj)

        if len(self.physicalSamples):
            data["physicalSample"] = []
        for value_obj in self.physicalSamples:
            obj = value_obj.to_json()
            data["physicalSample"].append(obj)

        if self.archiveType:
            value_obj = self.archiveType
            obj = value_obj.to_json()
            data["archiveType"] = obj

        if self.columnNumber:
            value_obj = self.columnNumber
            obj = value_obj
            data["number"] = obj

        if self.composite:
            value_obj = self.composite
            obj = value_obj
            data["isComposite"] = obj

        if self.description:
            value_obj = self.description
            obj = value_obj
            data["description"] = obj

        if self.instrument:
            value_obj = self.instrument
            obj = value_obj
            data["measurementInstrument"] = obj

        if self.maxValue:
            value_obj = self.maxValue
            obj = value_obj
            data["hasMaxValue"] = obj

        if self.meanValue:
            value_obj = self.meanValue
            obj = value_obj
            data["hasMeanValue"] = obj

        if self.medianValue:
            value_obj = self.medianValue
            obj = value_obj
            data["hasMedianValue"] = obj

        if self.minValue:
            value_obj = self.minValue
            obj = value_obj
            data["hasMinValue"] = obj

        if self.missingValue:
            value_obj = self.missingValue
            obj = value_obj
            data["missingValue"] = obj

        if self.name:
            value_obj = self.name
            obj = value_obj
            data["variableName"] = obj

        if self.notes:
            value_obj = self.notes
            obj = value_obj
            data["notes"] = obj

        if self.partOfCompilation:
            value_obj = self.partOfCompilation
            obj = value_obj.to_json()
            data["inCompilationBeta"] = obj

        if self.primary:
            value_obj = self.primary
            obj = value_obj
            data["isPrimary"] = obj

        if self.proxy:
            value_obj = self.proxy
            obj = value_obj.to_json()
            data["proxy"] = obj

        if self.proxyGeneral:
            value_obj = self.proxyGeneral
            obj = value_obj.to_json()
            data["proxyGeneral"] = obj

        if self.resolution:
            value_obj = self.resolution
            obj = value_obj.to_json()
            data["resolution"] = obj

        if self.standardVariable:
            value_obj = self.standardVariable
            obj = value_obj.to_json()
            data["hasStandardVariable"] = obj

        if self.uncertainty:
            value_obj = self.uncertainty
            obj = value_obj
            data["uncertainty"] = obj

        if self.uncertaintyAnalytical:
            value_obj = self.uncertaintyAnalytical
            obj = value_obj
            data["uncertaintyAnalytical"] = obj

        if self.uncertaintyReproducibility:
            value_obj = self.uncertaintyReproducibility
            obj = value_obj
            data["uncertaintyReproducibility"] = obj

        if self.units:
            value_obj = self.units
            obj = value_obj.to_json()
            data["units"] = obj

        if self.values:
            value_obj = self.values
            obj = value_obj
            data["hasValues"] = obj

        if self.variableId:
            value_obj = self.variableId
            obj = value_obj
            data["TSid"] = obj

        if self.variableType:
            value_obj = self.variableType
            obj = value_obj
            data["variableType"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Variable':
        self = Variable()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "TSid":
                    value = pvalue
                    obj = value
                    self.variableId = obj
            elif key == "archiveType":
                    value = pvalue
                    obj = ArchiveType.from_synonym(re.sub("^.*?#", "", value))
                    self.archiveType = obj
            elif key == "calibration":
                for value in pvalue:
                    obj = Calibration.from_json(value)
                    self.calibratedVias.append(obj)
            elif key == "description":
                    value = pvalue
                    obj = value
                    self.description = obj
            elif key == "foundInDataset":
                    value = pvalue
                    obj = value
                    self.foundInDataset = obj
            elif key == "foundInTable":
                    value = pvalue
                    obj = value
                    self.foundInTable = obj
            elif key == "hasMaxValue":
                    value = pvalue
                    obj = value
                    self.maxValue = obj
            elif key == "hasMeanValue":
                    value = pvalue
                    obj = value
                    self.meanValue = obj
            elif key == "hasMedianValue":
                    value = pvalue
                    obj = value
                    self.medianValue = obj
            elif key == "hasMinValue":
                    value = pvalue
                    obj = value
                    self.minValue = obj
            elif key == "hasStandardVariable":
                    value = pvalue
                    obj = PaleoVariable.from_synonym(re.sub("^.*?#", "", value))
                    self.standardVariable = obj
            elif key == "hasValues":
                    value = pvalue
                    obj = value
                    self.values = obj
            elif key == "inCompilationBeta":
                    value = pvalue
                    obj = Compilation.from_json(value)
                    self.partOfCompilation = obj
            elif key == "interpretation":
                for value in pvalue:
                    obj = Interpretation.from_json(value)
                    self.interpretations.append(obj)
            elif key == "isComposite":
                    value = pvalue
                    obj = value
                    self.composite = obj
            elif key == "isPrimary":
                    value = pvalue
                    obj = value
                    self.primary = obj
            elif key == "measurementInstrument":
                    value = pvalue
                    obj = value
                    self.instrument = obj
            elif key == "missingValue":
                    value = pvalue
                    obj = value
                    self.missingValue = obj
            elif key == "notes":
                    value = pvalue
                    obj = value
                    self.notes = obj
            elif key == "number":
                    value = pvalue
                    obj = value
                    self.columnNumber = obj
            elif key == "physicalSample":
                for value in pvalue:
                    obj = PhysicalSample.from_json(value)
                    self.physicalSamples.append(obj)
            elif key == "proxy":
                    value = pvalue
                    obj = PaleoProxy.from_synonym(re.sub("^.*?#", "", value))
                    self.proxy = obj
            elif key == "proxyGeneral":
                    value = pvalue
                    obj = PaleoProxyGeneral.from_synonym(re.sub("^.*?#", "", value))
                    self.proxyGeneral = obj
            elif key == "resolution":
                    value = pvalue
                    obj = Resolution.from_json(value)
                    self.resolution = obj
            elif key == "uncertainty":
                    value = pvalue
                    obj = value
                    self.uncertainty = obj
            elif key == "uncertaintyAnalytical":
                    value = pvalue
                    obj = value
                    self.uncertaintyAnalytical = obj
            elif key == "uncertaintyReproducibility":
                    value = pvalue
                    obj = value
                    self.uncertaintyReproducibility = obj
            elif key == "units":
                    value = pvalue
                    obj = PaleoUnit.from_synonym(re.sub("^.*?#", "", value))
                    self.units = obj
            elif key == "variableName":
                    value = pvalue
                    obj = value
                    self.name = obj
            elif key == "variableType":
                    value = pvalue
                    obj = value
                    self.variableType = obj
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
        
    def getArchiveType(self) -> ArchiveType:
        return self.archiveType

    def setArchiveType(self, archiveType:ArchiveType):
        assert isinstance(archiveType, ArchiveType), f"Error: '{archiveType}' is not of type ArchiveType\nYou can create a new ArchiveType object from a string using the following syntax:\n- Fetch existing ArchiveType by synonym: ArchiveType.from_synonym(\"{archiveType}\")\n- Create a new custom ArchiveType: ArchiveType(\"{archiveType}\")"
        self.archiveType = archiveType
    
    def getCalibratedVias(self) -> list[Calibration]:
        return self.calibratedVias

    def setCalibratedVias(self, calibratedVias:list[Calibration]):
        assert isinstance(calibratedVias, list), "Error: calibratedVias is not a list"
        assert all(isinstance(x, Calibration) for x in calibratedVias), f"Error: '{calibratedVias}' is not of type Calibration"
        self.calibratedVias = calibratedVias

    def addCalibratedVia(self, calibratedVias:Calibration):
        assert isinstance(calibratedVias, Calibration), f"Error: '{calibratedVias}' is not of type Calibration"
        self.calibratedVias.append(calibratedVias)
        
    def getColumnNumber(self) -> int:
        return self.columnNumber

    def setColumnNumber(self, columnNumber:int):
        assert isinstance(columnNumber, int), f"Error: '{columnNumber}' is not of type int"
        self.columnNumber = columnNumber
    
    def getDescription(self) -> str:
        return self.description

    def setDescription(self, description:str):
        assert isinstance(description, str), f"Error: '{description}' is not of type str"
        self.description = description
    
    def getFoundInDataset(self) -> object:
        return self.foundInDataset

    def setFoundInDataset(self, foundInDataset:object):
        assert isinstance(foundInDataset, object), f"Error: '{foundInDataset}' is not of type object"
        self.foundInDataset = foundInDataset
    
    def getFoundInTable(self) -> object:
        return self.foundInTable

    def setFoundInTable(self, foundInTable:object):
        assert isinstance(foundInTable, object), f"Error: '{foundInTable}' is not of type object"
        self.foundInTable = foundInTable
    
    def getInstrument(self) -> object:
        return self.instrument

    def setInstrument(self, instrument:object):
        assert isinstance(instrument, object), f"Error: '{instrument}' is not of type object"
        self.instrument = instrument
    
    def getInterpretations(self) -> list[Interpretation]:
        return self.interpretations

    def setInterpretations(self, interpretations:list[Interpretation]):
        assert isinstance(interpretations, list), "Error: interpretations is not a list"
        assert all(isinstance(x, Interpretation) for x in interpretations), f"Error: '{interpretations}' is not of type Interpretation"
        self.interpretations = interpretations

    def addInterpretation(self, interpretations:Interpretation):
        assert isinstance(interpretations, Interpretation), f"Error: '{interpretations}' is not of type Interpretation"
        self.interpretations.append(interpretations)
        
    def getMaxValue(self) -> float:
        return self.maxValue

    def setMaxValue(self, maxValue:float):
        assert isinstance(maxValue, float), f"Error: '{maxValue}' is not of type float"
        self.maxValue = maxValue
    
    def getMeanValue(self) -> float:
        return self.meanValue

    def setMeanValue(self, meanValue:float):
        assert isinstance(meanValue, float), f"Error: '{meanValue}' is not of type float"
        self.meanValue = meanValue
    
    def getMedianValue(self) -> float:
        return self.medianValue

    def setMedianValue(self, medianValue:float):
        assert isinstance(medianValue, float), f"Error: '{medianValue}' is not of type float"
        self.medianValue = medianValue
    
    def getMinValue(self) -> float:
        return self.minValue

    def setMinValue(self, minValue:float):
        assert isinstance(minValue, float), f"Error: '{minValue}' is not of type float"
        self.minValue = minValue
    
    def getMissingValue(self) -> str:
        return self.missingValue

    def setMissingValue(self, missingValue:str):
        assert isinstance(missingValue, str), f"Error: '{missingValue}' is not of type str"
        self.missingValue = missingValue
    
    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        assert isinstance(name, str), f"Error: '{name}' is not of type str"
        self.name = name
    
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        assert isinstance(notes, str), f"Error: '{notes}' is not of type str"
        self.notes = notes
    
    def getPartOfCompilation(self) -> Compilation:
        return self.partOfCompilation

    def setPartOfCompilation(self, partOfCompilation:Compilation):
        assert isinstance(partOfCompilation, Compilation), f"Error: '{partOfCompilation}' is not of type Compilation"
        self.partOfCompilation = partOfCompilation
    
    def getPhysicalSamples(self) -> list[PhysicalSample]:
        return self.physicalSamples

    def setPhysicalSamples(self, physicalSamples:list[PhysicalSample]):
        assert isinstance(physicalSamples, list), "Error: physicalSamples is not a list"
        assert all(isinstance(x, PhysicalSample) for x in physicalSamples), f"Error: '{physicalSamples}' is not of type PhysicalSample"
        self.physicalSamples = physicalSamples

    def addPhysicalSample(self, physicalSamples:PhysicalSample):
        assert isinstance(physicalSamples, PhysicalSample), f"Error: '{physicalSamples}' is not of type PhysicalSample"
        self.physicalSamples.append(physicalSamples)
        
    def getProxy(self) -> PaleoProxy:
        return self.proxy

    def setProxy(self, proxy:PaleoProxy):
        assert isinstance(proxy, PaleoProxy), f"Error: '{proxy}' is not of type PaleoProxy\nYou can create a new PaleoProxy object from a string using the following syntax:\n- Fetch existing PaleoProxy by synonym: PaleoProxy.from_synonym(\"{proxy}\")\n- Create a new custom PaleoProxy: PaleoProxy(\"{proxy}\")"
        self.proxy = proxy
    
    def getProxyGeneral(self) -> PaleoProxyGeneral:
        return self.proxyGeneral

    def setProxyGeneral(self, proxyGeneral:PaleoProxyGeneral):
        assert isinstance(proxyGeneral, PaleoProxyGeneral), f"Error: '{proxyGeneral}' is not of type PaleoProxyGeneral\nYou can create a new PaleoProxyGeneral object from a string using the following syntax:\n- Fetch existing PaleoProxyGeneral by synonym: PaleoProxyGeneral.from_synonym(\"{proxyGeneral}\")\n- Create a new custom PaleoProxyGeneral: PaleoProxyGeneral(\"{proxyGeneral}\")"
        self.proxyGeneral = proxyGeneral
    
    def getResolution(self) -> Resolution:
        return self.resolution

    def setResolution(self, resolution:Resolution):
        assert isinstance(resolution, Resolution), f"Error: '{resolution}' is not of type Resolution"
        self.resolution = resolution
    
    def getStandardVariable(self) -> PaleoVariable:
        return self.standardVariable

    def setStandardVariable(self, standardVariable:PaleoVariable):
        assert isinstance(standardVariable, PaleoVariable), f"Error: '{standardVariable}' is not of type PaleoVariable\nYou can create a new PaleoVariable object from a string using the following syntax:\n- Fetch existing PaleoVariable by synonym: PaleoVariable.from_synonym(\"{standardVariable}\")\n- Create a new custom PaleoVariable: PaleoVariable(\"{standardVariable}\")"
        self.standardVariable = standardVariable
    
    def getUncertainty(self) -> str:
        return self.uncertainty

    def setUncertainty(self, uncertainty:str):
        assert isinstance(uncertainty, str), f"Error: '{uncertainty}' is not of type str"
        self.uncertainty = uncertainty
    
    def getUncertaintyAnalytical(self) -> str:
        return self.uncertaintyAnalytical

    def setUncertaintyAnalytical(self, uncertaintyAnalytical:str):
        assert isinstance(uncertaintyAnalytical, str), f"Error: '{uncertaintyAnalytical}' is not of type str"
        self.uncertaintyAnalytical = uncertaintyAnalytical
    
    def getUncertaintyReproducibility(self) -> str:
        return self.uncertaintyReproducibility

    def setUncertaintyReproducibility(self, uncertaintyReproducibility:str):
        assert isinstance(uncertaintyReproducibility, str), f"Error: '{uncertaintyReproducibility}' is not of type str"
        self.uncertaintyReproducibility = uncertaintyReproducibility
    
    def getUnits(self) -> PaleoUnit:
        return self.units

    def setUnits(self, units:PaleoUnit):
        assert isinstance(units, PaleoUnit), f"Error: '{units}' is not of type PaleoUnit\nYou can create a new PaleoUnit object from a string using the following syntax:\n- Fetch existing PaleoUnit by synonym: PaleoUnit.from_synonym(\"{units}\")\n- Create a new custom PaleoUnit: PaleoUnit(\"{units}\")"
        self.units = units
    
    def getValues(self) -> str:
        return self.values

    def setValues(self, values:str):
        assert isinstance(values, str), f"Error: '{values}' is not of type str"
        self.values = values
    
    def getVariableId(self) -> str:
        return self.variableId

    def setVariableId(self, variableId:str):
        assert isinstance(variableId, str), f"Error: '{variableId}' is not of type str"
        self.variableId = variableId
    
    def getVariableType(self) -> str:
        return self.variableType

    def setVariableType(self, variableType:str):
        assert isinstance(variableType, str), f"Error: '{variableType}' is not of type str"
        self.variableType = variableType
    
    def isComposite(self) -> bool:
        return self.composite

    def setComposite(self, composite:bool):
        assert isinstance(composite, bool), f"Error: '{composite}' is not of type bool"
        self.composite = composite
    
    def isPrimary(self) -> bool:
        return self.primary

    def setPrimary(self, primary:bool):
        assert isinstance(primary, bool), f"Error: '{primary}' is not of type bool"
        self.primary = primary
    