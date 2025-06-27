
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.change import Change

class ChangeLog:
    """Auto-generated LinkedEarth class representing `ChangeLog`."""
    def __init__(self):
        """Initialize a new ChangeLog instance."""
        
        self.changess: list[Change] = []
        self.curator: str = None
        self.lastVersion: str = None
        self.notes: str = None
        self.timestamp: str = None
        self.version: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#ChangeLog"
        self.id = self.ns + "/" + uniqid("ChangeLog.")

    @staticmethod
    def from_data(id, data) -> 'ChangeLog':
        """Instantiate `ChangeLog` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        ChangeLog
            The populated `ChangeLog` instance.
        """
        self = ChangeLog()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasChanges":
                for val in value:
                    if "@id" in val:
                        obj = Change.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.changess.append(obj)
        
            elif key == "hasCurator":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.curator = obj
        
            elif key == "hasLastVersion":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.lastVersion = obj
        
            elif key == "hasNotes":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasTimestamp":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.timestamp = obj
        
            elif key == "hasVersion":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.version = obj
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

        if len(self.changess):
            data[self.id]["hasChanges"] = []
        for value_obj in self.changess:
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
            data[self.id]["hasChanges"].append(obj)

        if self.curator:
            value_obj = self.curator
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCurator"] = [obj]
                

        if self.lastVersion:
            value_obj = self.lastVersion
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasLastVersion"] = [obj]
                

        if self.notes:
            value_obj = self.notes
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"] = [obj]
                

        if self.timestamp:
            value_obj = self.timestamp
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasTimestamp"] = [obj]
                

        if self.version:
            value_obj = self.version
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasVersion"] = [obj]
                
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

        if len(self.changess):
            data["changes"] = []
        for value_obj in self.changess:
            obj = value_obj.to_json()
            data["changes"].append(obj)

        if self.curator:
            value_obj = self.curator
            obj = value_obj
            data["curator"] = obj

        if self.lastVersion:
            value_obj = self.lastVersion
            obj = value_obj
            data["lastVersion"] = obj

        if self.notes:
            value_obj = self.notes
            obj = value_obj
            data["notes"] = obj

        if self.timestamp:
            value_obj = self.timestamp
            obj = value_obj
            data["timestamp"] = obj

        if self.version:
            value_obj = self.version
            obj = value_obj
            data["version"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'ChangeLog':
        """Instantiate `ChangeLog` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        ChangeLog
            The populated `ChangeLog` instance.
        """
        self = ChangeLog()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "changes":
                for value in pvalue:
                    obj = Change.from_json(value)
                    self.changess.append(obj)
            elif key == "curator":
                    value = pvalue
                    obj = value
                    self.curator = obj
            elif key == "lastVersion":
                    value = pvalue
                    obj = value
                    self.lastVersion = obj
            elif key == "notes":
                    value = pvalue
                    obj = value
                    self.notes = obj
            elif key == "timestamp":
                    value = pvalue
                    obj = value
                    self.timestamp = obj
            elif key == "version":
                    value = pvalue
                    obj = value
                    self.version = obj
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
        
    def getChangess(self) -> list[Change]:
        """Get changess list.

        Returns
        -------
        list[Change]
            A list of Change objects.
        """
        return self.changess

    def setChangess(self, changess:list[Change]):
        """Set the changess list.

        Parameters
        ----------
        changess : list[Change]
            The list to assign.
        """
        assert isinstance(changess, list), "Error: changess is not a list"
        assert all(isinstance(x, Change) for x in changess), f"Error: '{changess}' is not of type Change"
        self.changess = changess

    def addChanges(self, changess:Change):
        """Add a value to the changess list.

        Parameters
        ----------
        changess : Change
            The value to append.
        """
        assert isinstance(changess, Change), f"Error: '{changess}' is not of type Change"
        self.changess.append(changess)
        
    def getCurator(self) -> str:
        """Get curator.

        Returns
        -------
        str
            The current value of curator.
        """
        return self.curator

    def setCurator(self, curator:str):
        """Set curator.

        Parameters
        ----------
        curator : str
            The value to assign.
        """
        assert isinstance(curator, str), f"Error: '{curator}' is not of type str"
        self.curator = curator
    
    def getLastVersion(self) -> str:
        """Get lastVersion.

        Returns
        -------
        str
            The current value of lastVersion.
        """
        return self.lastVersion

    def setLastVersion(self, lastVersion:str):
        """Set lastVersion.

        Parameters
        ----------
        lastVersion : str
            The value to assign.
        """
        assert isinstance(lastVersion, str), f"Error: '{lastVersion}' is not of type str"
        self.lastVersion = lastVersion
    
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
    
    def getTimestamp(self) -> str:
        """Get timestamp.

        Returns
        -------
        str
            The current value of timestamp.
        """
        return self.timestamp

    def setTimestamp(self, timestamp:str):
        """Set timestamp.

        Parameters
        ----------
        timestamp : str
            The value to assign.
        """
        assert isinstance(timestamp, str), f"Error: '{timestamp}' is not of type str"
        self.timestamp = timestamp
    
    def getVersion(self) -> str:
        """Get version.

        Returns
        -------
        str
            The current value of version.
        """
        return self.version

    def setVersion(self, version:str):
        """Set version.

        Parameters
        ----------
        version : str
            The value to assign.
        """
        assert isinstance(version, str), f"Error: '{version}' is not of type str"
        self.version = version
    