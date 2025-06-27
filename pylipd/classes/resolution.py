
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.paleounit import PaleoUnit

class Resolution:
    """Auto-generated LinkedEarth class representing `Resolution`."""
    def __init__(self):
        """Initialize a new Resolution instance."""
        
        self.maxValue: float = None
        self.meanValue: float = None
        self.medianValue: float = None
        self.minValue: float = None
        self.units: PaleoUnit = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Resolution"
        self.id = self.ns + "/" + uniqid("Resolution.")

    @staticmethod
    def from_data(id, data) -> 'Resolution':
        """Instantiate `Resolution` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        Resolution
            The populated `Resolution` instance.
        """
        self = Resolution()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
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
        
            elif key == "hasUnits":
                for val in value:
                    obj = PaleoUnit.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.units = obj
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

        if self.units:
            value_obj = self.units
            obj = value_obj.to_json()
            data["units"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Resolution':
        """Instantiate `Resolution` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        Resolution
            The populated `Resolution` instance.
        """
        self = Resolution()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
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
            elif key == "units":
                    value = pvalue
                    obj = PaleoUnit.from_synonym(re.sub("^.*?#", "", value))
                    self.units = obj
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
        
    def getMaxValue(self) -> float:
        """Get maxValue.

        Returns
        -------
        float
            The current value of maxValue.
        """
        return self.maxValue

    def setMaxValue(self, maxValue:float):
        """Set maxValue.

        Parameters
        ----------
        maxValue : float
            The value to assign.
        """
        assert isinstance(maxValue, float), f"Error: '{maxValue}' is not of type float"
        self.maxValue = maxValue
    
    def getMeanValue(self) -> float:
        """Get meanValue.

        Returns
        -------
        float
            The current value of meanValue.
        """
        return self.meanValue

    def setMeanValue(self, meanValue:float):
        """Set meanValue.

        Parameters
        ----------
        meanValue : float
            The value to assign.
        """
        assert isinstance(meanValue, float), f"Error: '{meanValue}' is not of type float"
        self.meanValue = meanValue
    
    def getMedianValue(self) -> float:
        """Get medianValue.

        Returns
        -------
        float
            The current value of medianValue.
        """
        return self.medianValue

    def setMedianValue(self, medianValue:float):
        """Set medianValue.

        Parameters
        ----------
        medianValue : float
            The value to assign.
        """
        assert isinstance(medianValue, float), f"Error: '{medianValue}' is not of type float"
        self.medianValue = medianValue
    
    def getMinValue(self) -> float:
        """Get minValue.

        Returns
        -------
        float
            The current value of minValue.
        """
        return self.minValue

    def setMinValue(self, minValue:float):
        """Set minValue.

        Parameters
        ----------
        minValue : float
            The value to assign.
        """
        assert isinstance(minValue, float), f"Error: '{minValue}' is not of type float"
        self.minValue = minValue
    
    def getUnits(self) -> PaleoUnit:
        """Get units.

        Returns
        -------
        PaleoUnit
            The current value of units.
        """
        return self.units

    def setUnits(self, units:PaleoUnit):
        """Set units.

        Parameters
        ----------
        units : PaleoUnit
            The value to assign.
        """
        assert isinstance(units, PaleoUnit), f"Error: '{units}' is not of type PaleoUnit\nYou can create a new PaleoUnit object from a string using the following syntax:\n- Fetch existing PaleoUnit by synonym: PaleoUnit.from_synonym(\"{units}\")\n- Create a new custom PaleoUnit: PaleoUnit(\"{units}\")"
        self.units = units
    