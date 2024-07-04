
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.integrationtime import IntegrationTime
from pylipd.classes.interpretationvariable import InterpretationVariable
from pylipd.classes.interpretationseasonality import InterpretationSeasonality

class Interpretation:

    def __init__(self):
        self.local: str = None
        self.variable: InterpretationVariable = None
        self.variableGeneral: str = None
        self.seasonalityGeneral: InterpretationSeasonality = None
        self.interpretationDirection: str = None
        self.variableGeneralDirection: str = None
        self.rank: str = None
        self.integrationTime: IntegrationTime = None
        self.notes: str = None
        self.seasonality: InterpretationSeasonality = None
        self.variableDetail: str = None
        self.scope: str = None
        self.seasonalityOriginal: InterpretationSeasonality = None
        self.basis: str = None
        self.mathematicalRelation: str = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Interpretation':
        self = Interpretation()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasScope":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.scope = obj
        
            elif key == "hasIntegrationTime":

                for val in value:
                    if "@id" in val:
                        obj = IntegrationTime.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.integrationTime = obj
        
            elif key == "hasMathematicalRelation":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.mathematicalRelation = obj
        
            elif key == "hasBasis":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.basis = obj
        
            elif key == "hasVariableDetail":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableDetail = obj
        
            elif key == "hasSeasonality":

                for val in value:
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.seasonality = obj
        
            elif key == "hasNotes":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasVariableGeneral":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableGeneral = obj
        
            elif key == "hasVariable":

                for val in value:
                    obj = InterpretationVariable.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.variable = obj
        
            elif key == "hasRank":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.rank = obj
        
            elif key == "isLocal":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.local = obj
        
            elif key == "hasVariableGeneralDirection":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.variableGeneralDirection = obj
        
            elif key == "hasSeasonalityGeneral":

                for val in value:
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.seasonalityGeneral = obj
        
            elif key == "hasSeasonalityOriginal":

                for val in value:
                    obj = InterpretationSeasonality.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.seasonalityOriginal = obj
        
            elif key == "hasInterpretationDirection":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.interpretationDirection = obj
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
        
    def getSeasonality(self) -> InterpretationSeasonality:
        return self.seasonality

    def setSeasonality(self, seasonality:InterpretationSeasonality):
        self.seasonality = seasonality

    def getBasis(self) -> str:
        return self.basis

    def setBasis(self, basis:str):
        self.basis = basis

    def getVariableGeneralDirection(self) -> str:
        return self.variableGeneralDirection

    def setVariableGeneralDirection(self, variableGeneralDirection:str):
        self.variableGeneralDirection = variableGeneralDirection

    def getRank(self) -> str:
        return self.rank

    def setRank(self, rank:str):
        self.rank = rank

    def getVariable(self) -> InterpretationVariable:
        return self.variable

    def setVariable(self, variable:InterpretationVariable):
        self.variable = variable

    def getInterpretationDirection(self) -> str:
        return self.interpretationDirection

    def setInterpretationDirection(self, interpretationDirection:str):
        self.interpretationDirection = interpretationDirection

    def getSeasonalityGeneral(self) -> InterpretationSeasonality:
        return self.seasonalityGeneral

    def setSeasonalityGeneral(self, seasonalityGeneral:InterpretationSeasonality):
        self.seasonalityGeneral = seasonalityGeneral

    def getIntegrationTime(self) -> IntegrationTime:
        return self.integrationTime

    def setIntegrationTime(self, integrationTime:IntegrationTime):
        self.integrationTime = integrationTime

    def getVariableGeneral(self) -> str:
        return self.variableGeneral

    def setVariableGeneral(self, variableGeneral:str):
        self.variableGeneral = variableGeneral

    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes

    def getMathematicalRelation(self) -> str:
        return self.mathematicalRelation

    def setMathematicalRelation(self, mathematicalRelation:str):
        self.mathematicalRelation = mathematicalRelation

    def getVariableDetail(self) -> str:
        return self.variableDetail

    def setVariableDetail(self, variableDetail:str):
        self.variableDetail = variableDetail

    def isLocal(self) -> str:
        return self.local

    def setLocal(self, local:str):
        self.local = local

    def getScope(self) -> str:
        return self.scope

    def setScope(self, scope:str):
        self.scope = scope

    def getSeasonalityOriginal(self) -> InterpretationSeasonality:
        return self.seasonalityOriginal

    def setSeasonalityOriginal(self, seasonalityOriginal:InterpretationSeasonality):
        self.seasonalityOriginal = seasonalityOriginal
