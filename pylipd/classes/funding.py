
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.person import Person

class Funding:
    """Auto-generated LinkedEarth class representing `Funding`."""
    def __init__(self):
        """Initialize a new Funding instance."""
        
        self.fundingAgency: str = None
        self.fundingCountry: str = None
        self.grants: list[str] = []
        self.investigators: list[Person] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Funding"
        self.id = self.ns + "/" + uniqid("Funding.")

    @staticmethod
    def from_data(id, data) -> 'Funding':
        """Instantiate `Funding` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        Funding
            The populated `Funding` instance.
        """
        self = Funding()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasFundingAgency":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.fundingAgency = obj
        
            elif key == "hasFundingCountry":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.fundingCountry = obj
        
            elif key == "hasGrant":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.grants.append(obj)
        
            elif key == "hasInvestigator":
                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.investigators.append(obj)
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

        if len(self.grants):
            data[self.id]["hasGrant"] = []
        for value_obj in self.grants:
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasGrant"].append(obj)

        if len(self.investigators):
            data[self.id]["hasInvestigator"] = []
        for value_obj in self.investigators:
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
            data[self.id]["hasInvestigator"].append(obj)

        if self.fundingAgency:
            value_obj = self.fundingAgency
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasFundingAgency"] = [obj]
                

        if self.fundingCountry:
            value_obj = self.fundingCountry
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasFundingCountry"] = [obj]
                
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

        if len(self.grants):
            data["grant"] = []
        for value_obj in self.grants:
            obj = value_obj
            data["grant"].append(obj)

        if len(self.investigators):
            data["investigator"] = []
        for value_obj in self.investigators:
            obj = value_obj.to_json()
            data["investigator"].append(obj)

        if self.fundingAgency:
            value_obj = self.fundingAgency
            obj = value_obj
            data["agency"] = obj

        if self.fundingCountry:
            value_obj = self.fundingCountry
            obj = value_obj
            data["country"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Funding':
        """Instantiate `Funding` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        Funding
            The populated `Funding` instance.
        """
        self = Funding()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "agency":
                    value = pvalue
                    obj = value
                    self.fundingAgency = obj
            elif key == "country":
                    value = pvalue
                    obj = value
                    self.fundingCountry = obj
            elif key == "grant":
                for value in pvalue:
                    obj = value
                    self.grants.append(obj)
            elif key == "investigator":
                for value in pvalue:
                    obj = Person.from_json(value)
                    self.investigators.append(obj)
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
        
    def getFundingAgency(self) -> str:
        """Get fundingAgency.

        Returns
        -------
        str
            The current value of fundingAgency.
        """
        return self.fundingAgency

    def setFundingAgency(self, fundingAgency:str):
        """Set fundingAgency.

        Parameters
        ----------
        fundingAgency : str
            The value to assign.
        """
        assert isinstance(fundingAgency, str), f"Error: '{fundingAgency}' is not of type str"
        self.fundingAgency = fundingAgency
    
    def getFundingCountry(self) -> str:
        """Get fundingCountry.

        Returns
        -------
        str
            The current value of fundingCountry.
        """
        return self.fundingCountry

    def setFundingCountry(self, fundingCountry:str):
        """Set fundingCountry.

        Parameters
        ----------
        fundingCountry : str
            The value to assign.
        """
        assert isinstance(fundingCountry, str), f"Error: '{fundingCountry}' is not of type str"
        self.fundingCountry = fundingCountry
    
    def getGrants(self) -> list[str]:
        """Get grants list.

        Returns
        -------
        list[str]
            A list of str objects.
        """
        return self.grants

    def setGrants(self, grants:list[str]):
        """Set the grants list.

        Parameters
        ----------
        grants : list[str]
            The list to assign.
        """
        assert isinstance(grants, list), "Error: grants is not a list"
        assert all(isinstance(x, str) for x in grants), f"Error: '{grants}' is not of type str"
        self.grants = grants

    def addGrant(self, grants:str):
        """Add a value to the grants list.

        Parameters
        ----------
        grants : str
            The value to append.
        """
        assert isinstance(grants, str), f"Error: '{grants}' is not of type str"
        self.grants.append(grants)
        
    def getInvestigators(self) -> list[Person]:
        """Get investigators list.

        Returns
        -------
        list[Person]
            A list of Person objects.
        """
        return self.investigators

    def setInvestigators(self, investigators:list[Person]):
        """Set the investigators list.

        Parameters
        ----------
        investigators : list[Person]
            The list to assign.
        """
        assert isinstance(investigators, list), "Error: investigators is not a list"
        assert all(isinstance(x, Person) for x in investigators), f"Error: '{investigators}' is not of type Person"
        self.investigators = investigators

    def addInvestigator(self, investigators:Person):
        """Add a value to the investigators list.

        Parameters
        ----------
        investigators : Person
            The value to append.
        """
        assert isinstance(investigators, Person), f"Error: '{investigators}' is not of type Person"
        self.investigators.append(investigators)
        