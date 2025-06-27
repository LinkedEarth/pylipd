
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.interpretationseasonality import InterpretationSeasonality
from pylipd.classes.interpretationvariable import InterpretationVariable

class Interpretation:
    """Auto-generated LinkedEarth class representing `Interpretation`."""
    def __init__(self):
        """Initialize a new Interpretation instance."""
        
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
        """Instantiate `Interpretation` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        Interpretation
            The populated `Interpretation` instance.
        """
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
        """Serialize the object into a JSON-LD compatible dictionary.

        Parameters
        ----------
        data : dict, optional
            Existing data dictionary to extend.

        Returns
        -------
        dict
            The updated data dictionary.
        """
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
        """Return a lightweight JSON representation (used by LiPD).

        Returns
        -------
        dict
            A dictionary representation of this object.
        """
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
        """Instantiate `Interpretation` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        Interpretation
            The populated `Interpretation` instance.
        """
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
        """Store a predicate that is not defined in the ontology schema.

        This is useful for forward-compatibility with new properties that are
        not yet part of the official schema.

        Parameters
        ----------
        key : str
            The property name.
        value : any
            The property value.
        """
        if key not in self.misc:
            self.misc[key] = value
    
    def get_non_standard_property(self, key):
        """Return a single non-standard property by key.

        Parameters
        ----------
        key : str
            The property name.

        Returns
        -------
        any
            The property value.
        """
        return self.misc[key]
                
    def get_all_non_standard_properties(self):
        """Return the dictionary of all non-standard properties.

        Returns
        -------
        dict
            Dictionary of all non-standard properties.
        """
        return self.misc

    def add_non_standard_property(self, key, value):
        """Append a value to a list-valued non-standard property.

        Parameters
        ----------
        key : str
            The property name.
        value : any
            The value to append.
        """
        if key not in self.misc:
            self.misc[key] = []
        self.misc[key].append(value)
        
    def getBasis(self) -> str:
        """Get basis.

        Returns
        -------
        str
            The current value of basis.
        """
        return self.basis

    def setBasis(self, basis:str):
        """Set basis.

        Parameters
        ----------
        basis : str
            The value to assign.
        """
        assert isinstance(basis, str), f"Error: '{basis}' is not of type str"
        self.basis = basis
    
    def getDirection(self) -> str:
        """Get direction.

        Returns
        -------
        str
            The current value of direction.
        """
        return self.direction

    def setDirection(self, direction:str):
        """Set direction.

        Parameters
        ----------
        direction : str
            The value to assign.
        """
        assert isinstance(direction, str), f"Error: '{direction}' is not of type str"
        self.direction = direction
    
    def getMathematicalRelation(self) -> str:
        """Get mathematicalRelation.

        Returns
        -------
        str
            The current value of mathematicalRelation.
        """
        return self.mathematicalRelation

    def setMathematicalRelation(self, mathematicalRelation:str):
        """Set mathematicalRelation.

        Parameters
        ----------
        mathematicalRelation : str
            The value to assign.
        """
        assert isinstance(mathematicalRelation, str), f"Error: '{mathematicalRelation}' is not of type str"
        self.mathematicalRelation = mathematicalRelation
    
    def getNotes(self) -> str:
        """Get notes.

        Returns
        -------
        str
            The current value of notes.
        """
        return self.notes

    def setNotes(self, notes:str):
        """Set notes.

        Parameters
        ----------
        notes : str
            The value to assign.
        """
        assert isinstance(notes, str), f"Error: '{notes}' is not of type str"
        self.notes = notes
    
    def getRank(self) -> str:
        """Get rank.

        Returns
        -------
        str
            The current value of rank.
        """
        return self.rank

    def setRank(self, rank:str):
        """Set rank.

        Parameters
        ----------
        rank : str
            The value to assign.
        """
        assert isinstance(rank, str), f"Error: '{rank}' is not of type str"
        self.rank = rank
    
    def getScope(self) -> str:
        """Get scope.

        Returns
        -------
        str
            The current value of scope.
        """
        return self.scope

    def setScope(self, scope:str):
        """Set scope.

        Parameters
        ----------
        scope : str
            The value to assign.
        """
        assert isinstance(scope, str), f"Error: '{scope}' is not of type str"
        self.scope = scope
    
    def getSeasonality(self) -> InterpretationSeasonality:
        """Get seasonality.

        Returns
        -------
        InterpretationSeasonality
            The current value of seasonality.
        """
        return self.seasonality

    def setSeasonality(self, seasonality:InterpretationSeasonality):
        """Set seasonality.

        Parameters
        ----------
        seasonality : InterpretationSeasonality
            The value to assign.
        """
        assert isinstance(seasonality, InterpretationSeasonality), f"Error: '{seasonality}' is not of type InterpretationSeasonality\nYou can create a new InterpretationSeasonality object from a string using the following syntax:\n- Fetch existing InterpretationSeasonality by synonym: InterpretationSeasonality.from_synonym(\"{seasonality}\")\n- Create a new custom InterpretationSeasonality: InterpretationSeasonality(\"{seasonality}\")"
        self.seasonality = seasonality
    
    def getSeasonalityGeneral(self) -> InterpretationSeasonality:
        """Get seasonalityGeneral.

        Returns
        -------
        InterpretationSeasonality
            The current value of seasonalityGeneral.
        """
        return self.seasonalityGeneral

    def setSeasonalityGeneral(self, seasonalityGeneral:InterpretationSeasonality):
        """Set seasonalityGeneral.

        Parameters
        ----------
        seasonalityGeneral : InterpretationSeasonality
            The value to assign.
        """
        assert isinstance(seasonalityGeneral, InterpretationSeasonality), f"Error: '{seasonalityGeneral}' is not of type InterpretationSeasonality\nYou can create a new InterpretationSeasonality object from a string using the following syntax:\n- Fetch existing InterpretationSeasonality by synonym: InterpretationSeasonality.from_synonym(\"{seasonalityGeneral}\")\n- Create a new custom InterpretationSeasonality: InterpretationSeasonality(\"{seasonalityGeneral}\")"
        self.seasonalityGeneral = seasonalityGeneral
    
    def getSeasonalityOriginal(self) -> InterpretationSeasonality:
        """Get seasonalityOriginal.

        Returns
        -------
        InterpretationSeasonality
            The current value of seasonalityOriginal.
        """
        return self.seasonalityOriginal

    def setSeasonalityOriginal(self, seasonalityOriginal:InterpretationSeasonality):
        """Set seasonalityOriginal.

        Parameters
        ----------
        seasonalityOriginal : InterpretationSeasonality
            The value to assign.
        """
        assert isinstance(seasonalityOriginal, InterpretationSeasonality), f"Error: '{seasonalityOriginal}' is not of type InterpretationSeasonality\nYou can create a new InterpretationSeasonality object from a string using the following syntax:\n- Fetch existing InterpretationSeasonality by synonym: InterpretationSeasonality.from_synonym(\"{seasonalityOriginal}\")\n- Create a new custom InterpretationSeasonality: InterpretationSeasonality(\"{seasonalityOriginal}\")"
        self.seasonalityOriginal = seasonalityOriginal
    
    def getVariable(self) -> InterpretationVariable:
        """Get variable.

        Returns
        -------
        InterpretationVariable
            The current value of variable.
        """
        return self.variable

    def setVariable(self, variable:InterpretationVariable):
        """Set variable.

        Parameters
        ----------
        variable : InterpretationVariable
            The value to assign.
        """
        assert isinstance(variable, InterpretationVariable), f"Error: '{variable}' is not of type InterpretationVariable\nYou can create a new InterpretationVariable object from a string using the following syntax:\n- Fetch existing InterpretationVariable by synonym: InterpretationVariable.from_synonym(\"{variable}\")\n- Create a new custom InterpretationVariable: InterpretationVariable(\"{variable}\")"
        self.variable = variable
    
    def getVariableDetail(self) -> str:
        """Get variableDetail.

        Returns
        -------
        str
            The current value of variableDetail.
        """
        return self.variableDetail

    def setVariableDetail(self, variableDetail:str):
        """Set variableDetail.

        Parameters
        ----------
        variableDetail : str
            The value to assign.
        """
        assert isinstance(variableDetail, str), f"Error: '{variableDetail}' is not of type str"
        self.variableDetail = variableDetail
    
    def getVariableGeneral(self) -> str:
        """Get variableGeneral.

        Returns
        -------
        str
            The current value of variableGeneral.
        """
        return self.variableGeneral

    def setVariableGeneral(self, variableGeneral:str):
        """Set variableGeneral.

        Parameters
        ----------
        variableGeneral : str
            The value to assign.
        """
        assert isinstance(variableGeneral, str), f"Error: '{variableGeneral}' is not of type str"
        self.variableGeneral = variableGeneral
    
    def getVariableGeneralDirection(self) -> str:
        """Get variableGeneralDirection.

        Returns
        -------
        str
            The current value of variableGeneralDirection.
        """
        return self.variableGeneralDirection

    def setVariableGeneralDirection(self, variableGeneralDirection:str):
        """Set variableGeneralDirection.

        Parameters
        ----------
        variableGeneralDirection : str
            The value to assign.
        """
        assert isinstance(variableGeneralDirection, str), f"Error: '{variableGeneralDirection}' is not of type str"
        self.variableGeneralDirection = variableGeneralDirection
    
    def isLocal(self) -> str:
        """Get local.

        Returns
        -------
        str
            The current value of local.
        """
        return self.local

    def setLocal(self, local:str):
        """Set local.

        Parameters
        ----------
        local : str
            The value to assign.
        """
        assert isinstance(local, str), f"Error: '{local}' is not of type str"
        self.local = local
    