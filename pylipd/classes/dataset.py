
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.archivetype import ArchiveType
from pylipd.classes.paleodata import PaleoData
from pylipd.classes.person import Person
from pylipd.classes.funding import Funding
from pylipd.classes.publication import Publication
from pylipd.classes.chrondata import ChronData
from pylipd.classes.changelog import ChangeLog
from pylipd.classes.location import Location

class Dataset:

    def __init__(self):
        self.chronData: list[ChronData] = []
        self.originalDataUrl: str = None
        self.paleoData: list[PaleoData] = []
        self.name: str = None
        self.investigators: list[Person] = []
        self.collectionYear: str = None
        self.creators: list[Person] = []
        self.datasetId: str = None
        self.collectionName: str = None
        self.publications: list[Publication] = []
        self.location: Location = None
        self.version: str = None
        self.dataSource: str = None
        self.fundings: list[Funding] = []
        self.notes: str = None
        self.spreadsheetLink: str = None
        self.changeLog: ChangeLog = None
        self.contributor: Person = None
        self.archiveType: ArchiveType = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Dataset':
        self = Dataset()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasOriginalDataUrl":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.originalDataUrl = obj
        
            elif key == "hasSpreadsheetLink":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.spreadsheetLink = obj
        
            elif key == "hasContributor":

                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.contributor = obj
        
            elif key == "hasChangeLog":

                for val in value:
                    if "@id" in val:
                        obj = ChangeLog.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.changeLog = obj
        
            elif key == "hasFunding":

                for val in value:
                    if "@id" in val:
                        obj = Funding.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.fundings.append(obj)
        
            elif key == "hasName":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "hasCreator":

                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.creators.append(obj)
        
            elif key == "hasCollectionName":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.collectionName = obj
        
            elif key == "hasArchiveType":

                for val in value:
                    obj = ArchiveType.from_synonym(re.sub("^.*?#", "", val["@id"]))
                                    
                    self.archiveType = obj
        
            elif key == "hasVersion":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.version = obj
        
            elif key == "hasPaleoData":

                for val in value:
                    if "@id" in val:
                        obj = PaleoData.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.paleoData.append(obj)
        
            elif key == "hasNotes":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasInvestigator":

                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.investigators.append(obj)
        
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
        
            elif key == "hasPublication":

                for val in value:
                    if "@id" in val:
                        obj = Publication.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.publications.append(obj)
        
            elif key == "hasLocation":

                for val in value:
                    if "@id" in val:
                        obj = Location.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.location = obj
        
            elif key == "hasCollectionYear":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.collectionYear = obj
        
            elif key == "hasChronData":

                for val in value:
                    if "@id" in val:
                        obj = ChronData.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.chronData.append(obj)
            else:
                for val in value:
                    obj = None
                    if "@id" in val:
                        obj = mydata[val["@id"]]
                    elif "@value" in val:
                        obj = val["@value"]
                    self.set_non_standard_property(key, obj)
        
        return self

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
        
    def getPaleoData(self) -> list[PaleoData]:
        return self.paleoData

    def setPaleoData(self, paleoData:list[PaleoData]):
        self.paleoData = paleoData

    def addPaleoData(self, paleoData:PaleoData):
        self.paleoData.append(paleoData)
        
    def getSpreadsheetLink(self) -> str:
        return self.spreadsheetLink

    def setSpreadsheetLink(self, spreadsheetLink:str):
        self.spreadsheetLink = spreadsheetLink

    def getLocation(self) -> Location:
        return self.location

    def setLocation(self, location:Location):
        self.location = location

    def getArchiveType(self) -> ArchiveType:
        return self.archiveType

    def setArchiveType(self, archiveType:ArchiveType):
        self.archiveType = archiveType

    def getContributor(self) -> Person:
        return self.contributor

    def setContributor(self, contributor:Person):
        self.contributor = contributor

    def getChronData(self) -> list[ChronData]:
        return self.chronData

    def setChronData(self, chronData:list[ChronData]):
        self.chronData = chronData

    def addChronData(self, chronData:ChronData):
        self.chronData.append(chronData)
        
    def getDatasetId(self) -> str:
        return self.datasetId

    def setDatasetId(self, datasetId:str):
        self.datasetId = datasetId

    def getFundings(self) -> list[Funding]:
        return self.fundings

    def setFundings(self, fundings:list[Funding]):
        self.fundings = fundings

    def addFunding(self, funding:Funding):
        self.fundings.append(funding)
        
    def getChangeLog(self) -> ChangeLog:
        return self.changeLog

    def setChangeLog(self, changeLog:ChangeLog):
        self.changeLog = changeLog

    def getInvestigators(self) -> list[Person]:
        return self.investigators

    def setInvestigators(self, investigators:list[Person]):
        self.investigators = investigators

    def addInvestigator(self, investigator:Person):
        self.investigators.append(investigator)
        
    def getDataSource(self) -> str:
        return self.dataSource

    def setDataSource(self, dataSource:str):
        self.dataSource = dataSource

    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        self.name = name

    def getCollectionYear(self) -> str:
        return self.collectionYear

    def setCollectionYear(self, collectionYear:str):
        self.collectionYear = collectionYear

    def getCreators(self) -> list[Person]:
        return self.creators

    def setCreators(self, creators:list[Person]):
        self.creators = creators

    def addCreator(self, creator:Person):
        self.creators.append(creator)
        
    def getCollectionName(self) -> str:
        return self.collectionName

    def setCollectionName(self, collectionName:str):
        self.collectionName = collectionName

    def getPublications(self) -> list[Publication]:
        return self.publications

    def setPublications(self, publications:list[Publication]):
        self.publications = publications

    def addPublication(self, publication:Publication):
        self.publications.append(publication)
        
    def getOriginalDataUrl(self) -> str:
        return self.originalDataUrl

    def setOriginalDataUrl(self, originalDataUrl:str):
        self.originalDataUrl = originalDataUrl

    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes

    def getVersion(self) -> str:
        return self.version

    def setVersion(self, version:str):
        self.version = version
