
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.interpretationseasonality import InterpretationSeasonality
from pylipd.classes.interpretationvariable import InterpretationVariable

class Interpretation:

    def __init__(self):
        self.basis: str = None
        self.direction: str = None
        self.local: str = None
        self.mathematicalRelation: str = None
        self.notes: str = None
        self.rank: str = None
        self.scope: str = None
        self.seasonality: InterpretationSeasonality = None
        self.seasonalityGeneral: InterpretationSeasonality = None
        self.seasonalityOriginal: InterpretationSeasonality = None
        self.variable: InterpretationVariable = None
        self.variableDetail: str = None
        self.variableGeneral: str = None
        self.variableGeneralDirection: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Interpretation"
        self.id = self.ns + "/" + uniqid("Interpretation.")

    @staticmethod
    def from_data(id, data) -> 'Interpretation':
        self = Interpretation()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasBasis":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.basis = obj
        
            elif key == "hasDirection":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.direction = obj
        
            elif key == "hasMathematicalRelation":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.mathematicalRelation = obj
        
            elif key == "hasNotes":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasRank":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.rank = obj
        
            elif key == "hasScope":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.scope = obj
        
            elif key == "hasSeasonality":
                for val in value:
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.seasonality = obj
        
            elif key == "hasSeasonalityGeneral":
                for val in value:
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.seasonalityGeneral = obj
        
            elif key == "hasSeasonalityOriginal":
                for val in value:
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.seasonalityOriginal = obj
        
            elif key == "hasVariable":
                for val in value:
                    obj = InterpretationVariable.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.variable = obj
        
            elif key == "hasVariableDetail":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableDetail = obj
        
            elif key == "hasVariableGeneral":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableGeneral = obj
        
            elif key == "hasVariableGeneralDirection":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableGeneralDirection = obj
        
            elif key == "isLocal":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.local = obj
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

        if self.basis:
            value_obj = self.basis
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasBasis"] = [obj]
                

        if self.direction:
            value_obj = self.direction
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDirection"] = [obj]
                

        if self.local:
            value_obj = self.local
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["isLocal"] = [obj]
                

        if self.mathematicalRelation:
            value_obj = self.mathematicalRelation
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasMathematicalRelation"] = [obj]
                

        if self.notes:
            value_obj = self.notes
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"] = [obj]
                

        if self.rank:
            value_obj = self.rank
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasRank"] = [obj]
                

        if self.scope:
            value_obj = self.scope
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasScope"] = [obj]
                

        if self.seasonality:
            value_obj = self.seasonality
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
            data[self.id]["hasSeasonality"] = [obj]
                

        if self.seasonalityGeneral:
            value_obj = self.seasonalityGeneral
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
            data[self.id]["hasSeasonalityGeneral"] = [obj]
                

        if self.seasonalityOriginal:
            value_obj = self.seasonalityOriginal
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
            data[self.id]["hasSeasonalityOriginal"] = [obj]
                

        if self.variable:
            value_obj = self.variable
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
            data[self.id]["hasVariable"] = [obj]
                

        if self.variableDetail:
            value_obj = self.variableDetail
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasVariableDetail"] = [obj]
                

        if self.variableGeneral:
            value_obj = self.variableGeneral
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasVariableGeneral"] = [obj]
                

        if self.variableGeneralDirection:
            value_obj = self.variableGeneralDirection
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasVariableGeneralDirection"] = [obj]
                
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

        if self.basis:
            value_obj = self.basis
            obj = value_obj
            data["basis"] = obj

        if self.direction:
            value_obj = self.direction
            obj = value_obj
            data["direction"] = obj

        if self.local:
            value_obj = self.local
            obj = value_obj
            data["isLocal"] = obj

        if self.mathematicalRelation:
            value_obj = self.mathematicalRelation
            obj = value_obj
            data["mathematicalRelation"] = obj

        if self.notes:
            value_obj = self.notes
            obj = value_obj
            data["notes"] = obj

        if self.rank:
            value_obj = self.rank
            obj = value_obj
            data["rank"] = obj

        if self.scope:
            value_obj = self.scope
            obj = value_obj
            data["scope"] = obj

        if self.seasonality:
            value_obj = self.seasonality
            obj = value_obj.to_json()
            data["seasonality"] = obj

        if self.seasonalityGeneral:
            value_obj = self.seasonalityGeneral
            obj = value_obj.to_json()
            data["seasonalityGeneral"] = obj

        if self.seasonalityOriginal:
            value_obj = self.seasonalityOriginal
            obj = value_obj.to_json()
            data["seasonalityOriginal"] = obj

        if self.variable:
            value_obj = self.variable
            obj = value_obj.to_json()
            data["variable"] = obj

        if self.variableDetail:
            value_obj = self.variableDetail
            obj = value_obj
            data["variableDetail"] = obj

        if self.variableGeneral:
            value_obj = self.variableGeneral
            obj = value_obj
            data["variableGeneral"] = obj

        if self.variableGeneralDirection:
            value_obj = self.variableGeneralDirection
            obj = value_obj
            data["variableGeneralDirection"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Interpretation':
        self = Interpretation()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "basis":
                    value = pvalue
                    obj = value
                    self.basis = obj
            elif key == "direction":
                    value = pvalue
                    obj = value
                    self.direction = obj
            elif key == "isLocal":
                    value = pvalue
                    obj = value
                    self.local = obj
            elif key == "mathematicalRelation":
                    value = pvalue
                    obj = value
                    self.mathematicalRelation = obj
            elif key == "notes":
                    value = pvalue
                    obj = value
                    self.notes = obj
            elif key == "rank":
                    value = pvalue
                    obj = value
                    self.rank = obj
            elif key == "scope":
                    value = pvalue
                    obj = value
                    self.scope = obj
            elif key == "seasonality":
                    value = pvalue
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", value))
                    self.seasonality = obj
            elif key == "seasonalityGeneral":
                    value = pvalue
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", value))
                    self.seasonalityGeneral = obj
            elif key == "seasonalityOriginal":
                    value = pvalue
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", value))
                    self.seasonalityOriginal = obj
            elif key == "variable":
                    value = pvalue
                    obj = InterpretationVariable.from_synonym(re.sub("^.*?#", "", value))
                    self.variable = obj
            elif key == "variableDetail":
                    value = pvalue
                    obj = value
                    self.variableDetail = obj
            elif key == "variableGeneral":
                    value = pvalue
                    obj = value
                    self.variableGeneral = obj
            elif key == "variableGeneralDirection":
                    value = pvalue
                    obj = value
                    self.variableGeneralDirection = obj
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
        
    def getBasis(self) -> str:
        return self.basis

    def setBasis(self, basis:str):
        self.basis = basis
    
    def getDirection(self) -> str:
        return self.direction

    def setDirection(self, direction:str):
        self.direction = direction
    
    def getMathematicalRelation(self) -> str:
        return self.mathematicalRelation

    def setMathematicalRelation(self, mathematicalRelation:str):
        self.mathematicalRelation = mathematicalRelation
    
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes
    
    def getRank(self) -> str:
        return self.rank

    def setRank(self, rank:str):
        self.rank = rank
    
    def getScope(self) -> str:
        return self.scope

    def setScope(self, scope:str):
        self.scope = scope
    
    def getSeasonality(self) -> InterpretationSeasonality:
        return self.seasonality

    def setSeasonality(self, seasonality:InterpretationSeasonality):
        self.seasonality = seasonality
    
    def getSeasonalityGeneral(self) -> InterpretationSeasonality:
        return self.seasonalityGeneral

    def setSeasonalityGeneral(self, seasonalityGeneral:InterpretationSeasonality):
        self.seasonalityGeneral = seasonalityGeneral
    
    def getSeasonalityOriginal(self) -> InterpretationSeasonality:
        return self.seasonalityOriginal

    def setSeasonalityOriginal(self, seasonalityOriginal:InterpretationSeasonality):
        self.seasonalityOriginal = seasonalityOriginal
    
    def getVariable(self) -> InterpretationVariable:
        return self.variable

    def setVariable(self, variable:InterpretationVariable):
        self.variable = variable
    
    def getVariableDetail(self) -> str:
        return self.variableDetail

    def setVariableDetail(self, variableDetail:str):
        self.variableDetail = variableDetail
    
    def getVariableGeneral(self) -> str:
        return self.variableGeneral

    def setVariableGeneral(self, variableGeneral:str):
        self.variableGeneral = variableGeneral
    
    def getVariableGeneralDirection(self) -> str:
        return self.variableGeneralDirection

    def setVariableGeneralDirection(self, variableGeneralDirection:str):
        self.variableGeneralDirection = variableGeneralDirection
    
    def isLocal(self) -> str:
        return self.local

    def setLocal(self, local:str):
        self.local = local
    