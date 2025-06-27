
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid

class Change:
    """Auto-generated LinkedEarth class representing `Change`."""
    def __init__(self):
        """Initialize a new Change instance."""
        
        self.name: str = None
        self.notess: list[str] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Change"
        self.id = self.ns + "/" + uniqid("Change.")

    @staticmethod
    def from_data(id, data) -> 'Change':
        """Instantiate `Change` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        Change
            The populated `Change` instance.
        """
        self = Change()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "hasNotes":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.notess.append(obj)
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

        if len(self.notess):
            data[self.id]["hasNotes"] = []
        for value_obj in self.notess:
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"].append(obj)

        if self.name:
            value_obj = self.name
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasName"] = [obj]
                
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

        if len(self.notess):
            data["notes"] = []
        for value_obj in self.notess:
            obj = value_obj
            data["notes"].append(obj)

        if self.name:
            value_obj = self.name
            obj = value_obj
            data["name"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Change':
        """Instantiate `Change` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        Change
            The populated `Change` instance.
        """
        self = Change()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "name":
                    value = pvalue
                    obj = value
                    self.name = obj
            elif key == "notes":
                for value in pvalue:
                    obj = value
                    self.notess.append(obj)
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
        
    def getName(self) -> str:
        """Get name.

        Returns
        -------
        str
            The current value of name.
        """
        return self.name

    def setName(self, name:str):
        """Set name.

        Parameters
        ----------
        name : str
            The value to assign.
        """
        assert isinstance(name, str), f"Error: '{name}' is not of type str"
        self.name = name
    
    def getNotess(self) -> list[str]:
        """Get notess list.

        Returns
        -------
        list[str]
            A list of str objects.
        """
        return self.notess

    def setNotess(self, notess:list[str]):
        """Set the notess list.

        Parameters
        ----------
        notess : list[str]
            The list to assign.
        """
        assert isinstance(notess, list), "Error: notess is not a list"
        assert all(isinstance(x, str) for x in notess), f"Error: '{notess}' is not of type str"
        self.notess = notess

    def addNotes(self, notess:str):
        """Add a value to the notess list.

        Parameters
        ----------
        notess : str
            The value to append.
        """
        assert isinstance(notess, str), f"Error: '{notess}' is not of type str"
        self.notess.append(notess)
        