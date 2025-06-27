
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.datatable import DataTable
from pylipd.classes.model import Model

class PaleoData:
    """Auto-generated LinkedEarth class representing `PaleoData`."""
    def __init__(self):
        """Initialize a new PaleoData instance."""
        
        self.measurementTables: list[DataTable] = []
        self.modeledBy: list[Model] = []
        self.name: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#PaleoData"
        self.id = self.ns + "/" + uniqid("PaleoData.")

    @staticmethod
    def from_data(id, data) -> 'PaleoData':
        """Instantiate `PaleoData` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        PaleoData
            The populated `PaleoData` instance.
        """
        self = PaleoData()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasMeasurementTable":
                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.measurementTables.append(obj)
        
            elif key == "hasName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "modeledBy":
                for val in value:
                    if "@id" in val:
                        obj = Model.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.modeledBy.append(obj)
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

        if len(self.measurementTables):
            data[self.id]["hasMeasurementTable"] = []
        for value_obj in self.measurementTables:
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
            data[self.id]["hasMeasurementTable"].append(obj)

        if len(self.modeledBy):
            data[self.id]["modeledBy"] = []
        for value_obj in self.modeledBy:
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
            data[self.id]["modeledBy"].append(obj)

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

        if len(self.measurementTables):
            data["measurementTable"] = []
        for value_obj in self.measurementTables:
            obj = value_obj.to_json()
            data["measurementTable"].append(obj)

        if len(self.modeledBy):
            data["model"] = []
        for value_obj in self.modeledBy:
            obj = value_obj.to_json()
            data["model"].append(obj)

        if self.name:
            value_obj = self.name
            obj = value_obj
            data["paleoDataName"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'PaleoData':
        """Instantiate `PaleoData` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        PaleoData
            The populated `PaleoData` instance.
        """
        self = PaleoData()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "measurementTable":
                for value in pvalue:
                    obj = DataTable.from_json(value)
                    self.measurementTables.append(obj)
            elif key == "model":
                for value in pvalue:
                    obj = Model.from_json(value)
                    self.modeledBy.append(obj)
            elif key == "paleoDataName":
                    value = pvalue
                    obj = value
                    self.name = obj
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
        
    def getMeasurementTables(self) -> list[DataTable]:
        """Get measurementTables list.

        Returns
        -------
        list[DataTable]
            A list of DataTable objects.
        """
        return self.measurementTables

    def setMeasurementTables(self, measurementTables:list[DataTable]):
        """Set the measurementTables list.

        Parameters
        ----------
        measurementTables : list[DataTable]
            The list to assign.
        """
        assert isinstance(measurementTables, list), "Error: measurementTables is not a list"
        assert all(isinstance(x, DataTable) for x in measurementTables), f"Error: '{measurementTables}' is not of type DataTable"
        self.measurementTables = measurementTables

    def addMeasurementTable(self, measurementTables:DataTable):
        """Add a value to the measurementTables list.

        Parameters
        ----------
        measurementTables : DataTable
            The value to append.
        """
        assert isinstance(measurementTables, DataTable), f"Error: '{measurementTables}' is not of type DataTable"
        self.measurementTables.append(measurementTables)
        
    def getModeledBy(self) -> list[Model]:
        """Get modeledBy list.

        Returns
        -------
        list[Model]
            A list of Model objects.
        """
        return self.modeledBy

    def setModeledBy(self, modeledBy:list[Model]):
        """Set the modeledBy list.

        Parameters
        ----------
        modeledBy : list[Model]
            The list to assign.
        """
        assert isinstance(modeledBy, list), "Error: modeledBy is not a list"
        assert all(isinstance(x, Model) for x in modeledBy), f"Error: '{modeledBy}' is not of type Model"
        self.modeledBy = modeledBy

    def addModeledBy(self, modeledBy:Model):
        """Add a value to the modeledBy list.

        Parameters
        ----------
        modeledBy : Model
            The value to append.
        """
        assert isinstance(modeledBy, Model), f"Error: '{modeledBy}' is not of type Model"
        self.modeledBy.append(modeledBy)
        
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
    