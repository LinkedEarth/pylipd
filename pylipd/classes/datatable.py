
##############################
# Auto-generated. Do not Edit
##############################

import re
import pandas as pd
import json
from pylipd.classes.variable import Variable
from pylipd.utils import uniqid
from pylipd.classes.variable import Variable

class DataTable:
    """Auto-generated LinkedEarth class representing `DataTable`."""
    def __init__(self):
        """Initialize a new DataTable instance."""
        
        self.fileName: str = None
        self.missingValue: str = None
        self.variables: list[Variable] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#DataTable"
        self.id = self.ns + "/" + uniqid("DataTable.")

    @staticmethod
    def from_data(id, data) -> 'DataTable':
        """Instantiate `DataTable` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        DataTable
            The populated `DataTable` instance.
        """
        self = DataTable()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasFileName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.fileName = obj
        
            elif key == "hasMissingValue":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.missingValue = obj
        
            elif key == "hasVariable":
                for val in value:
                    if "@id" in val:
                        obj = Variable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.variables.append(obj)
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

        if len(self.variables):
            data[self.id]["hasVariable"] = []
        for value_obj in self.variables:
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
            data[self.id]["hasVariable"].append(obj)

        if self.fileName:
            value_obj = self.fileName
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasFileName"] = [obj]
                

        if self.missingValue:
            value_obj = self.missingValue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasMissingValue"] = [obj]
                
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

        if len(self.variables):
            data["columns"] = []
        for value_obj in self.variables:
            obj = value_obj.to_json()
            data["columns"].append(obj)

        if self.fileName:
            value_obj = self.fileName
            obj = value_obj
            data["filename"] = obj

        if self.missingValue:
            value_obj = self.missingValue
            obj = value_obj
            data["missingValue"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'DataTable':
        """Instantiate `DataTable` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        DataTable
            The populated `DataTable` instance.
        """
        self = DataTable()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "columns":
                for value in pvalue:
                    obj = Variable.from_json(value)
                    self.variables.append(obj)
            elif key == "filename":
                    value = pvalue
                    obj = value
                    self.fileName = obj
            elif key == "missingValue":
                    value = pvalue
                    obj = value
                    self.missingValue = obj
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
        
    def getFileName(self) -> str:
        """Get fileName.

        Returns
        -------
        str
            The current value of fileName.
        """
        return self.fileName

    def setFileName(self, fileName:str):
        """Set fileName.

        Parameters
        ----------
        fileName : str
            The value to assign.
        """
        assert isinstance(fileName, str), f"Error: '{fileName}' is not of type str"
        self.fileName = fileName
    
    def getMissingValue(self) -> str:
        """Get missingValue.

        Returns
        -------
        str
            The current value of missingValue.
        """
        return self.missingValue

    def setMissingValue(self, missingValue:str):
        """Set missingValue.

        Parameters
        ----------
        missingValue : str
            The value to assign.
        """
        assert isinstance(missingValue, str), f"Error: '{missingValue}' is not of type str"
        self.missingValue = missingValue
    
    def getVariables(self) -> list[Variable]:
        """Get variables list.

        Returns
        -------
        list[Variable]
            A list of Variable objects.
        """
        return self.variables

    def setVariables(self, variables:list[Variable]):
        """Set the variables list.

        Parameters
        ----------
        variables : list[Variable]
            The list to assign.
        """
        assert isinstance(variables, list), "Error: variables is not a list"
        assert all(isinstance(x, Variable) for x in variables), f"Error: '{variables}' is not of type Variable"
        self.variables = variables

    def addVariable(self, variables:Variable):
        """Add a value to the variables list.

        Parameters
        ----------
        variables : Variable
            The value to append.
        """
        assert isinstance(variables, Variable), f"Error: '{variables}' is not of type Variable"
        self.variables.append(variables)
        
    # Special Functions manually added for DataTable class
    def getDataFrame(self, use_standard_names=False) -> pd.DataFrame:
        cols = []
        for v in self.variables:
            colname = v.getName()
            if use_standard_names and v.getStandardVariable() is not None:
                colname = v.getStandardVariable().getLabel()
            cols.append(colname)
        
        df = pd.DataFrame(columns=cols)
        for v in self.variables:
            colname = v.getName()
            if use_standard_names and v.getStandardVariable() is not None:
                colname = v.getStandardVariable().getLabel()
            df[colname] = json.loads(v.getValues())
        
        # Create metadata as a dictionary and add to dataframe attr
        df.attrs = {}
        for v in self.variables:
            colname = v.getName()
            if use_standard_names and v.getStandardVariable() is not None:
                colname = v.getStandardVariable().getLabel()
            df.attrs[colname] = v.to_json()
            del df.attrs[colname]["hasValues"]
    
        return df

    def setDataFrame(self, df: pd.DataFrame):
        # Create new set of variable objects using the metadata
        self.variables = []
        for colname in df.attrs:
            v = Variable.from_json(df.attrs[colname])
            v.setValues(json.dumps(df[colname].to_list()))
            self.addVariable(v)
