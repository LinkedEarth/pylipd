
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.datatable import DataTable

class Model:
    """Auto-generated LinkedEarth class representing `Model`."""
    def __init__(self):
        """Initialize a new Model instance."""
        
        self.code: str = None
        self.distributionTables: list[DataTable] = []
        self.ensembleTables: list[DataTable] = []
        self.summaryTables: list[DataTable] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Model"
        self.id = self.ns + "/" + uniqid("Model.")

    @staticmethod
    def from_data(id, data) -> 'Model':
        """Instantiate `Model` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        Model
            The populated `Model` instance.
        """
        self = Model()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasCode":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.code = obj
        
            elif key == "hasDistributionTable":
                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.distributionTables.append(obj)
        
            elif key == "hasEnsembleTable":
                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.ensembleTables.append(obj)
        
            elif key == "hasSummaryTable":
                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.summaryTables.append(obj)
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

        if len(self.distributionTables):
            data[self.id]["hasDistributionTable"] = []
        for value_obj in self.distributionTables:
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
            data[self.id]["hasDistributionTable"].append(obj)

        if len(self.ensembleTables):
            data[self.id]["hasEnsembleTable"] = []
        for value_obj in self.ensembleTables:
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
            data[self.id]["hasEnsembleTable"].append(obj)

        if len(self.summaryTables):
            data[self.id]["hasSummaryTable"] = []
        for value_obj in self.summaryTables:
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
            data[self.id]["hasSummaryTable"].append(obj)

        if self.code:
            value_obj = self.code
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCode"] = [obj]
                
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

        if len(self.distributionTables):
            data["distributionTable"] = []
        for value_obj in self.distributionTables:
            obj = value_obj.to_json()
            data["distributionTable"].append(obj)

        if len(self.ensembleTables):
            data["ensembleTable"] = []
        for value_obj in self.ensembleTables:
            obj = value_obj.to_json()
            data["ensembleTable"].append(obj)

        if len(self.summaryTables):
            data["summaryTable"] = []
        for value_obj in self.summaryTables:
            obj = value_obj.to_json()
            data["summaryTable"].append(obj)

        if self.code:
            value_obj = self.code
            obj = value_obj
            data["method"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Model':
        """Instantiate `Model` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        Model
            The populated `Model` instance.
        """
        self = Model()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "distributionTable":
                for value in pvalue:
                    obj = DataTable.from_json(value)
                    self.distributionTables.append(obj)
            elif key == "ensembleTable":
                for value in pvalue:
                    obj = DataTable.from_json(value)
                    self.ensembleTables.append(obj)
            elif key == "method":
                    value = pvalue
                    obj = value
                    self.code = obj
            elif key == "summaryTable":
                for value in pvalue:
                    obj = DataTable.from_json(value)
                    self.summaryTables.append(obj)
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
        
    def getCode(self) -> str:
        """Get code.

        Returns
        -------
        str
            The current value of code.
        """
        return self.code

    def setCode(self, code:str):
        """Set code.

        Parameters
        ----------
        code : str
            The value to assign.
        """
        assert isinstance(code, str), f"Error: '{code}' is not of type str"
        self.code = code
    
    def getDistributionTables(self) -> list[DataTable]:
        """Get distributionTables list.

        Returns
        -------
        list[DataTable]
            A list of DataTable objects.
        """
        return self.distributionTables

    def setDistributionTables(self, distributionTables:list[DataTable]):
        """Set the distributionTables list.

        Parameters
        ----------
        distributionTables : list[DataTable]
            The list to assign.
        """
        assert isinstance(distributionTables, list), "Error: distributionTables is not a list"
        assert all(isinstance(x, DataTable) for x in distributionTables), f"Error: '{distributionTables}' is not of type DataTable"
        self.distributionTables = distributionTables

    def addDistributionTable(self, distributionTables:DataTable):
        """Add a value to the distributionTables list.

        Parameters
        ----------
        distributionTables : DataTable
            The value to append.
        """
        assert isinstance(distributionTables, DataTable), f"Error: '{distributionTables}' is not of type DataTable"
        self.distributionTables.append(distributionTables)
        
    def getEnsembleTables(self) -> list[DataTable]:
        """Get ensembleTables list.

        Returns
        -------
        list[DataTable]
            A list of DataTable objects.
        """
        return self.ensembleTables

    def setEnsembleTables(self, ensembleTables:list[DataTable]):
        """Set the ensembleTables list.

        Parameters
        ----------
        ensembleTables : list[DataTable]
            The list to assign.
        """
        assert isinstance(ensembleTables, list), "Error: ensembleTables is not a list"
        assert all(isinstance(x, DataTable) for x in ensembleTables), f"Error: '{ensembleTables}' is not of type DataTable"
        self.ensembleTables = ensembleTables

    def addEnsembleTable(self, ensembleTables:DataTable):
        """Add a value to the ensembleTables list.

        Parameters
        ----------
        ensembleTables : DataTable
            The value to append.
        """
        assert isinstance(ensembleTables, DataTable), f"Error: '{ensembleTables}' is not of type DataTable"
        self.ensembleTables.append(ensembleTables)
        
    def getSummaryTables(self) -> list[DataTable]:
        """Get summaryTables list.

        Returns
        -------
        list[DataTable]
            A list of DataTable objects.
        """
        return self.summaryTables

    def setSummaryTables(self, summaryTables:list[DataTable]):
        """Set the summaryTables list.

        Parameters
        ----------
        summaryTables : list[DataTable]
            The list to assign.
        """
        assert isinstance(summaryTables, list), "Error: summaryTables is not a list"
        assert all(isinstance(x, DataTable) for x in summaryTables), f"Error: '{summaryTables}' is not of type DataTable"
        self.summaryTables = summaryTables

    def addSummaryTable(self, summaryTables:DataTable):
        """Add a value to the summaryTables list.

        Parameters
        ----------
        summaryTables : DataTable
            The value to append.
        """
        assert isinstance(summaryTables, DataTable), f"Error: '{summaryTables}' is not of type DataTable"
        self.summaryTables.append(summaryTables)
        