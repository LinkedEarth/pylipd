
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

    def __init__(self):
        self.archiveType: ArchiveType = None
        self.changeLog: ChangeLog = None
        self.chronData: list[ChronData] = []
        self.collectionName: str = None
        self.collectionYear: str = None
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
                                    
                    self.changeLog = obj
        
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
        data[self.id] = {}
        data[self.id]["type"] = [
            {
                "@id": self.type,
                "@type": "uri"
            }
        ]

        if len(self.chronData):
            data[self.id]["hasChronData"] = []
        for value_obj in self.chronData: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasChronData"].append(obj)

        if len(self.creators):
            data[self.id]["hasCreator"] = []
        for value_obj in self.creators: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasCreator"].append(obj)

        if len(self.fundings):
            data[self.id]["hasFunding"] = []
        for value_obj in self.fundings: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasFunding"].append(obj)

        if len(self.investigators):
            data[self.id]["hasInvestigator"] = []
        for value_obj in self.investigators: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasInvestigator"].append(obj)

        if len(self.paleoData):
            data[self.id]["hasPaleoData"] = []
        for value_obj in self.paleoData: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasPaleoData"].append(obj)

        if len(self.publications):
            data[self.id]["hasPublication"] = []
        for value_obj in self.publications: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasPublication"].append(obj)

        if self.archiveType:
            value_obj = self.archiveType 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasArchiveType"] = [obj]
                

        if self.changeLog:
            value_obj = self.changeLog 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasChangeLog"] = [obj]
                

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
                

        if self.contributor:
            value_obj = self.contributor 
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
                if re.match("\d{4}-\d{2}-\d{2}", value):
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
        
    def getArchiveType(self) -> ArchiveType:
        return self.archiveType

    def setArchiveType(self, archiveType:ArchiveType):
        self.archiveType = archiveType
    
    def getChangeLog(self) -> ChangeLog:
        return self.changeLog

    def setChangeLog(self, changeLog:ChangeLog):
        self.changeLog = changeLog
    
    def getChronData(self) -> list[ChronData]:
        return self.chronData

    def setChronData(self, chronData:list[ChronData]):
        self.chronData = chronData

    def addChronData(self, chronData:ChronData):
        self.chronData.append(chronData)
        
    def getCollectionName(self) -> str:
        return self.collectionName

    def setCollectionName(self, collectionName:str):
        self.collectionName = collectionName
    
    def getCollectionYear(self) -> str:
        return self.collectionYear

    def setCollectionYear(self, collectionYear:str):
        self.collectionYear = collectionYear
    
    def getContributor(self) -> Person:
        return self.contributor

    def setContributor(self, contributor:Person):
        self.contributor = contributor
    
    def getCreators(self) -> list[Person]:
        return self.creators

    def setCreators(self, creators:list[Person]):
        self.creators = creators

    def addCreator(self, creators:Person):
        self.creators.append(creators)
        
    def getDataSource(self) -> str:
        return self.dataSource

    def setDataSource(self, dataSource:str):
        self.dataSource = dataSource
    
    def getDatasetId(self) -> str:
        return self.datasetId

    def setDatasetId(self, datasetId:str):
        self.datasetId = datasetId
    
    def getFundings(self) -> list[Funding]:
        return self.fundings

    def setFundings(self, fundings:list[Funding]):
        self.fundings = fundings

    def addFunding(self, fundings:Funding):
        self.fundings.append(fundings)
        
    def getInvestigators(self) -> list[Person]:
        return self.investigators

    def setInvestigators(self, investigators:list[Person]):
        self.investigators = investigators

    def addInvestigator(self, investigators:Person):
        self.investigators.append(investigators)
        
    def getLocation(self) -> Location:
        return self.location

    def setLocation(self, location:Location):
        self.location = location
    
    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        self.name = name
    
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes
    
    def getOriginalDataUrl(self) -> str:
        return self.originalDataUrl

    def setOriginalDataUrl(self, originalDataUrl:str):
        self.originalDataUrl = originalDataUrl
    
    def getPaleoData(self) -> list[PaleoData]:
        return self.paleoData

    def setPaleoData(self, paleoData:list[PaleoData]):
        self.paleoData = paleoData

    def addPaleoData(self, paleoData:PaleoData):
        self.paleoData.append(paleoData)
        
    def getPublications(self) -> list[Publication]:
        return self.publications

    def setPublications(self, publications:list[Publication]):
        self.publications = publications

    def addPublication(self, publications:Publication):
        self.publications.append(publications)
        
    def getSpreadsheetLink(self) -> str:
        return self.spreadsheetLink

    def setSpreadsheetLink(self, spreadsheetLink:str):
        self.spreadsheetLink = spreadsheetLink
    
    def getVersion(self) -> str:
        return self.version

    def setVersion(self, version:str):
        self.version = version
    