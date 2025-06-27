
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.archivetype import ArchiveType
from pylipd.classes.changelog import ChangeLog
from pylipd.classes.chrondata import ChronData
from pylipd.classes.funding import Funding
from pylipd.classes.location import Location
from pylipd.classes.paleodata import PaleoData
from pylipd.classes.person import Person
from pylipd.classes.publication import Publication

class Dataset:
    """Auto-generated LinkedEarth class representing `Dataset`."""
    def __init__(self):
        """Initialize a new Dataset instance."""
        
        self.archiveType: ArchiveType = None
        self.changeLogs: list[ChangeLog] = []
        self.chronData: list[ChronData] = []
        self.collectionName: str = None
        self.collectionYear: str = None
        self.compilationNest: str = None
        self.contributor: Person = None
        self.creators: list[Person] = []
        self.dataSource: str = None
        self.datasetId: str = None
        self.fundings: list[Funding] = []
        self.investigators: list[Person] = []
        self.location: Location = None
        self.name: str = None
        self.notes: str = None
        self.originalDataUrl: str = None
        self.paleoData: list[PaleoData] = []
        self.publications: list[Publication] = []
        self.spreadsheetLink: str = None
        self.version: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Dataset"
        self.id = self.ns + "/" + uniqid("Dataset.")

    @staticmethod
    def from_data(id, data) -> 'Dataset':
        """Instantiate `Dataset` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        Dataset
            The populated `Dataset` instance.
        """
        self = Dataset()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasArchiveType":
                for val in value:
                    obj = ArchiveType.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.archiveType = obj
        
            elif key == "hasChangeLog":
                for val in value:
                    if "@id" in val:
                        obj = ChangeLog.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.changeLogs.append(obj)
        
            elif key == "hasChronData":
                for val in value:
                    if "@id" in val:
                        obj = ChronData.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.chronData.append(obj)
        
            elif key == "hasCollectionName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.collectionName = obj
        
            elif key == "hasCollectionYear":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.collectionYear = obj
        
            elif key == "hasCompilationNest":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.compilationNest = obj
        
            elif key == "hasContributor":
                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.contributor = obj
        
            elif key == "hasCreator":
                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.creators.append(obj)
        
            elif key == "hasDataSource":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.dataSource = obj
        
            elif key == "hasDatasetId":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.datasetId = obj
        
            elif key == "hasFunding":
                for val in value:
                    if "@id" in val:
                        obj = Funding.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.fundings.append(obj)
        
            elif key == "hasInvestigator":
                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.investigators.append(obj)
        
            elif key == "hasLocation":
                for val in value:
                    if "@id" in val:
                        obj = Location.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.location = obj
        
            elif key == "hasName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "hasNotes":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasOriginalDataUrl":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.originalDataUrl = obj
        
            elif key == "hasPaleoData":
                for val in value:
                    if "@id" in val:
                        obj = PaleoData.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.paleoData.append(obj)
        
            elif key == "hasPublication":
                for val in value:
                    if "@id" in val:
                        obj = Publication.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.publications.append(obj)
        
            elif key == "hasSpreadsheetLink":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.spreadsheetLink = obj
        
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

        if len(self.changeLogs):
            data[self.id]["hasChangeLog"] = []
        for value_obj in self.changeLogs:
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
            data[self.id]["hasChangeLog"].append(obj)

        if len(self.chronData):
            data[self.id]["hasChronData"] = []
        for value_obj in self.chronData:
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
            data[self.id]["hasChronData"].append(obj)

        if len(self.creators):
            data[self.id]["hasCreator"] = []
        for value_obj in self.creators:
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
            data[self.id]["hasCreator"].append(obj)

        if len(self.fundings):
            data[self.id]["hasFunding"] = []
        for value_obj in self.fundings:
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
            data[self.id]["hasFunding"].append(obj)

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

        if len(self.paleoData):
            data[self.id]["hasPaleoData"] = []
        for value_obj in self.paleoData:
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
            data[self.id]["hasPaleoData"].append(obj)

        if len(self.publications):
            data[self.id]["hasPublication"] = []
        for value_obj in self.publications:
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
            data[self.id]["hasPublication"].append(obj)

        if self.archiveType:
            value_obj = self.archiveType
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
            data[self.id]["hasArchiveType"] = [obj]
                

        if self.collectionName:
            value_obj = self.collectionName
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCollectionName"] = [obj]
                

        if self.collectionYear:
            value_obj = self.collectionYear
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCollectionYear"] = [obj]
                

        if self.compilationNest:
            value_obj = self.compilationNest
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCompilationNest"] = [obj]
                

        if self.contributor:
            value_obj = self.contributor
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
            data[self.id]["hasContributor"] = [obj]
                

        if self.dataSource:
            value_obj = self.dataSource
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDataSource"] = [obj]
                

        if self.datasetId:
            value_obj = self.datasetId
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDatasetId"] = [obj]
                

        if self.location:
            value_obj = self.location
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
            data[self.id]["hasLocation"] = [obj]
                

        if self.name:
            value_obj = self.name
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasName"] = [obj]
                

        if self.notes:
            value_obj = self.notes
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"] = [obj]
                

        if self.originalDataUrl:
            value_obj = self.originalDataUrl
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasOriginalDataUrl"] = [obj]
                

        if self.spreadsheetLink:
            value_obj = self.spreadsheetLink
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasSpreadsheetLink"] = [obj]
                

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

        if len(self.changeLogs):
            data["changelog"] = []
        for value_obj in self.changeLogs:
            obj = value_obj.to_json()
            data["changelog"].append(obj)

        if len(self.chronData):
            data["chronData"] = []
        for value_obj in self.chronData:
            obj = value_obj.to_json()
            data["chronData"].append(obj)

        if len(self.creators):
            data["creator"] = []
        for value_obj in self.creators:
            obj = value_obj.to_json()
            data["creator"].append(obj)

        if len(self.fundings):
            data["funding"] = []
        for value_obj in self.fundings:
            obj = value_obj.to_json()
            data["funding"].append(obj)

        if len(self.investigators):
            data["investigator"] = []
        for value_obj in self.investigators:
            obj = value_obj.to_json()
            data["investigator"].append(obj)

        if len(self.paleoData):
            data["paleoData"] = []
        for value_obj in self.paleoData:
            obj = value_obj.to_json()
            data["paleoData"].append(obj)

        if len(self.publications):
            data["pub"] = []
        for value_obj in self.publications:
            obj = value_obj.to_json()
            data["pub"].append(obj)

        if self.archiveType:
            value_obj = self.archiveType
            obj = value_obj.to_json()
            data["archiveType"] = obj

        if self.collectionName:
            value_obj = self.collectionName
            obj = value_obj
            data["collectionName"] = obj

        if self.collectionYear:
            value_obj = self.collectionYear
            obj = value_obj
            data["collectionYear"] = obj

        if self.compilationNest:
            value_obj = self.compilationNest
            obj = value_obj
            data["compilation_nest"] = obj

        if self.contributor:
            value_obj = self.contributor
            obj = value_obj.to_json()
            data["dataContributor"] = obj

        if self.dataSource:
            value_obj = self.dataSource
            obj = value_obj
            data["dataSource"] = obj

        if self.datasetId:
            value_obj = self.datasetId
            obj = value_obj
            data["datasetId"] = obj

        if self.location:
            value_obj = self.location
            obj = value_obj.to_json()
            data["geo"] = obj

        if self.name:
            value_obj = self.name
            obj = value_obj
            data["dataSetName"] = obj

        if self.notes:
            value_obj = self.notes
            obj = value_obj
            data["notes"] = obj

        if self.originalDataUrl:
            value_obj = self.originalDataUrl
            obj = value_obj
            data["originalDataURL"] = obj

        if self.spreadsheetLink:
            value_obj = self.spreadsheetLink
            obj = value_obj
            data["googleSpreadSheetKey"] = obj

        if self.version:
            value_obj = self.version
            obj = value_obj
            data["dataSetVersion"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Dataset':
        """Instantiate `Dataset` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        Dataset
            The populated `Dataset` instance.
        """
        self = Dataset()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "archiveType":
                    value = pvalue
                    obj = ArchiveType.from_synonym(re.sub("^.*?#", "", value))
                    self.archiveType = obj
            elif key == "changelog":
                for value in pvalue:
                    obj = ChangeLog.from_json(value)
                    self.changeLogs.append(obj)
            elif key == "chronData":
                for value in pvalue:
                    obj = ChronData.from_json(value)
                    self.chronData.append(obj)
            elif key == "collectionName":
                    value = pvalue
                    obj = value
                    self.collectionName = obj
            elif key == "collectionYear":
                    value = pvalue
                    obj = value
                    self.collectionYear = obj
            elif key == "compilation_nest":
                    value = pvalue
                    obj = value
                    self.compilationNest = obj
            elif key == "creator":
                for value in pvalue:
                    obj = Person.from_json(value)
                    self.creators.append(obj)
            elif key == "dataContributor":
                    value = pvalue
                    obj = Person.from_json(value)
                    self.contributor = obj
            elif key == "dataSetName":
                    value = pvalue
                    obj = value
                    self.name = obj
            elif key == "dataSetVersion":
                    value = pvalue
                    obj = value
                    self.version = obj
            elif key == "dataSource":
                    value = pvalue
                    obj = value
                    self.dataSource = obj
            elif key == "datasetId":
                    value = pvalue
                    obj = value
                    self.datasetId = obj
            elif key == "funding":
                for value in pvalue:
                    obj = Funding.from_json(value)
                    self.fundings.append(obj)
            elif key == "geo":
                    value = pvalue
                    obj = Location.from_json(value)
                    self.location = obj
            elif key == "googleSpreadSheetKey":
                    value = pvalue
                    obj = value
                    self.spreadsheetLink = obj
            elif key == "investigator":
                for value in pvalue:
                    obj = Person.from_json(value)
                    self.investigators.append(obj)
            elif key == "notes":
                    value = pvalue
                    obj = value
                    self.notes = obj
            elif key == "originalDataURL":
                    value = pvalue
                    obj = value
                    self.originalDataUrl = obj
            elif key == "paleoData":
                for value in pvalue:
                    obj = PaleoData.from_json(value)
                    self.paleoData.append(obj)
            elif key == "pub":
                for value in pvalue:
                    obj = Publication.from_json(value)
                    self.publications.append(obj)
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
        
    def getArchiveType(self) -> ArchiveType:
        """Get archiveType.

        Returns
        -------
        ArchiveType
            The current value of archiveType.
        """
        return self.archiveType

    def setArchiveType(self, archiveType:ArchiveType):
        """Set archiveType.

        Parameters
        ----------
        archiveType : ArchiveType
            The value to assign.
        """
        assert isinstance(archiveType, ArchiveType), f"Error: '{archiveType}' is not of type ArchiveType\nYou can create a new ArchiveType object from a string using the following syntax:\n- Fetch existing ArchiveType by synonym: ArchiveType.from_synonym(\"{archiveType}\")\n- Create a new custom ArchiveType: ArchiveType(\"{archiveType}\")"
        self.archiveType = archiveType
    
    def getChangeLogs(self) -> list[ChangeLog]:
        """Get changeLogs list.

        Returns
        -------
        list[ChangeLog]
            A list of ChangeLog objects.
        """
        return self.changeLogs

    def setChangeLogs(self, changeLogs:list[ChangeLog]):
        """Set the changeLogs list.

        Parameters
        ----------
        changeLogs : list[ChangeLog]
            The list to assign.
        """
        assert isinstance(changeLogs, list), "Error: changeLogs is not a list"
        assert all(isinstance(x, ChangeLog) for x in changeLogs), f"Error: '{changeLogs}' is not of type ChangeLog"
        self.changeLogs = changeLogs

    def addChangeLog(self, changeLogs:ChangeLog):
        """Add a value to the changeLogs list.

        Parameters
        ----------
        changeLogs : ChangeLog
            The value to append.
        """
        assert isinstance(changeLogs, ChangeLog), f"Error: '{changeLogs}' is not of type ChangeLog"
        self.changeLogs.append(changeLogs)
        
    def getChronData(self) -> list[ChronData]:
        """Get chronData list.

        Returns
        -------
        list[ChronData]
            A list of ChronData objects.
        """
        return self.chronData

    def setChronData(self, chronData:list[ChronData]):
        """Set the chronData list.

        Parameters
        ----------
        chronData : list[ChronData]
            The list to assign.
        """
        assert isinstance(chronData, list), "Error: chronData is not a list"
        assert all(isinstance(x, ChronData) for x in chronData), f"Error: '{chronData}' is not of type ChronData"
        self.chronData = chronData

    def addChronData(self, chronData:ChronData):
        """Add a value to the chronData list.

        Parameters
        ----------
        chronData : ChronData
            The value to append.
        """
        assert isinstance(chronData, ChronData), f"Error: '{chronData}' is not of type ChronData"
        self.chronData.append(chronData)
        
    def getCollectionName(self) -> str:
        """Get collectionName.

        Returns
        -------
        str
            The current value of collectionName.
        """
        return self.collectionName

    def setCollectionName(self, collectionName:str):
        """Set collectionName.

        Parameters
        ----------
        collectionName : str
            The value to assign.
        """
        assert isinstance(collectionName, str), f"Error: '{collectionName}' is not of type str"
        self.collectionName = collectionName
    
    def getCollectionYear(self) -> str:
        """Get collectionYear.

        Returns
        -------
        str
            The current value of collectionYear.
        """
        return self.collectionYear

    def setCollectionYear(self, collectionYear:str):
        """Set collectionYear.

        Parameters
        ----------
        collectionYear : str
            The value to assign.
        """
        assert isinstance(collectionYear, str), f"Error: '{collectionYear}' is not of type str"
        self.collectionYear = collectionYear
    
    def getCompilationNest(self) -> str:
        """Get compilationNest.

        Returns
        -------
        str
            The current value of compilationNest.
        """
        return self.compilationNest

    def setCompilationNest(self, compilationNest:str):
        """Set compilationNest.

        Parameters
        ----------
        compilationNest : str
            The value to assign.
        """
        assert isinstance(compilationNest, str), f"Error: '{compilationNest}' is not of type str"
        self.compilationNest = compilationNest
    
    def getContributor(self) -> Person:
        """Get contributor.

        Returns
        -------
        Person
            The current value of contributor.
        """
        return self.contributor

    def setContributor(self, contributor:Person):
        """Set contributor.

        Parameters
        ----------
        contributor : Person
            The value to assign.
        """
        assert isinstance(contributor, Person), f"Error: '{contributor}' is not of type Person"
        self.contributor = contributor
    
    def getCreators(self) -> list[Person]:
        """Get creators list.

        Returns
        -------
        list[Person]
            A list of Person objects.
        """
        return self.creators

    def setCreators(self, creators:list[Person]):
        """Set the creators list.

        Parameters
        ----------
        creators : list[Person]
            The list to assign.
        """
        assert isinstance(creators, list), "Error: creators is not a list"
        assert all(isinstance(x, Person) for x in creators), f"Error: '{creators}' is not of type Person"
        self.creators = creators

    def addCreator(self, creators:Person):
        """Add a value to the creators list.

        Parameters
        ----------
        creators : Person
            The value to append.
        """
        assert isinstance(creators, Person), f"Error: '{creators}' is not of type Person"
        self.creators.append(creators)
        
    def getDataSource(self) -> str:
        """Get dataSource.

        Returns
        -------
        str
            The current value of dataSource.
        """
        return self.dataSource

    def setDataSource(self, dataSource:str):
        """Set dataSource.

        Parameters
        ----------
        dataSource : str
            The value to assign.
        """
        assert isinstance(dataSource, str), f"Error: '{dataSource}' is not of type str"
        self.dataSource = dataSource
    
    def getDatasetId(self) -> str:
        """Get datasetId.

        Returns
        -------
        str
            The current value of datasetId.
        """
        return self.datasetId

    def setDatasetId(self, datasetId:str):
        """Set datasetId.

        Parameters
        ----------
        datasetId : str
            The value to assign.
        """
        assert isinstance(datasetId, str), f"Error: '{datasetId}' is not of type str"
        self.datasetId = datasetId
    
    def getFundings(self) -> list[Funding]:
        """Get fundings list.

        Returns
        -------
        list[Funding]
            A list of Funding objects.
        """
        return self.fundings

    def setFundings(self, fundings:list[Funding]):
        """Set the fundings list.

        Parameters
        ----------
        fundings : list[Funding]
            The list to assign.
        """
        assert isinstance(fundings, list), "Error: fundings is not a list"
        assert all(isinstance(x, Funding) for x in fundings), f"Error: '{fundings}' is not of type Funding"
        self.fundings = fundings

    def addFunding(self, fundings:Funding):
        """Add a value to the fundings list.

        Parameters
        ----------
        fundings : Funding
            The value to append.
        """
        assert isinstance(fundings, Funding), f"Error: '{fundings}' is not of type Funding"
        self.fundings.append(fundings)
        
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
        
    def getLocation(self) -> Location:
        """Get location.

        Returns
        -------
        Location
            The current value of location.
        """
        return self.location

    def setLocation(self, location:Location):
        """Set location.

        Parameters
        ----------
        location : Location
            The value to assign.
        """
        assert isinstance(location, Location), f"Error: '{location}' is not of type Location"
        self.location = location
    
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
        self.id = self.ns + '/' + name # This is a hack to set the id of the dataset based on the name

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
    
    def getOriginalDataUrl(self) -> str:
        """Get originalDataUrl.

        Returns
        -------
        str
            The current value of originalDataUrl.
        """
        return self.originalDataUrl

    def setOriginalDataUrl(self, originalDataUrl:str):
        """Set originalDataUrl.

        Parameters
        ----------
        originalDataUrl : str
            The value to assign.
        """
        assert isinstance(originalDataUrl, str), f"Error: '{originalDataUrl}' is not of type str"
        self.originalDataUrl = originalDataUrl
    
    def getPaleoData(self) -> list[PaleoData]:
        """Get paleoData list.

        Returns
        -------
        list[PaleoData]
            A list of PaleoData objects.
        """
        return self.paleoData

    def setPaleoData(self, paleoData:list[PaleoData]):
        """Set the paleoData list.

        Parameters
        ----------
        paleoData : list[PaleoData]
            The list to assign.
        """
        assert isinstance(paleoData, list), "Error: paleoData is not a list"
        assert all(isinstance(x, PaleoData) for x in paleoData), f"Error: '{paleoData}' is not of type PaleoData"
        self.paleoData = paleoData

    def addPaleoData(self, paleoData:PaleoData):
        """Add a value to the paleoData list.

        Parameters
        ----------
        paleoData : PaleoData
            The value to append.
        """
        assert isinstance(paleoData, PaleoData), f"Error: '{paleoData}' is not of type PaleoData"
        self.paleoData.append(paleoData)
        
    def getPublications(self) -> list[Publication]:
        """Get publications list.

        Returns
        -------
        list[Publication]
            A list of Publication objects.
        """
        return self.publications

    def setPublications(self, publications:list[Publication]):
        """Set the publications list.

        Parameters
        ----------
        publications : list[Publication]
            The list to assign.
        """
        assert isinstance(publications, list), "Error: publications is not a list"
        assert all(isinstance(x, Publication) for x in publications), f"Error: '{publications}' is not of type Publication"
        self.publications = publications

    def addPublication(self, publications:Publication):
        """Add a value to the publications list.

        Parameters
        ----------
        publications : Publication
            The value to append.
        """
        assert isinstance(publications, Publication), f"Error: '{publications}' is not of type Publication"
        self.publications.append(publications)
        
    def getSpreadsheetLink(self) -> str:
        """Get spreadsheetLink.

        Returns
        -------
        str
            The current value of spreadsheetLink.
        """
        return self.spreadsheetLink

    def setSpreadsheetLink(self, spreadsheetLink:str):
        """Set spreadsheetLink.

        Parameters
        ----------
        spreadsheetLink : str
            The value to assign.
        """
        assert isinstance(spreadsheetLink, str), f"Error: '{spreadsheetLink}' is not of type str"
        self.spreadsheetLink = spreadsheetLink
    
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
    