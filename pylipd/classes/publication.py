
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.person import Person

class Publication:

    def __init__(self):
        self.issue: str = None
        self.publisher: str = None
        self.year: str = None
        self.institution: str = None
        self.urls: list[str] = []
        self.journal: str = None
        self.citeKey: str = None
        self.type: str = None
        self.authors: list[Person] = []
        self.report: str = None
        self.pages: str = None
        self.firstAuthor: Person = None
        self.abstract: str = None
        self.title: str = None
        self.volume: str = None
        self.dOI: str = None
        self.dataUrls: list[str] = []
        self.citation: str = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Publication':
        self = Publication()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasAbstract":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.abstract = obj
        
            elif key == "hasIssue":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.issue = obj
        
            elif key == "hasFirstAuthor":

                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.firstAuthor = obj
        
            elif key == "hasAuthor":

                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.authors.append(obj)
        
            elif key == "hasVolume":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.volume = obj
        
            elif key == "hasType":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.type = obj
        
            elif key == "hasTitle":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.title = obj
        
            elif key == "hasPages":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.pages = obj
        
            elif key == "hasCitation":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.citation = obj
        
            elif key == "hasUrl":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.urls.append(obj)
        
            elif key == "hasDOI":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.dOI = obj
        
            elif key == "hasJournal":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.journal = obj
        
            elif key == "hasPublisher":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.publisher = obj
        
            elif key == "hasYear":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.year = obj
        
            elif key == "hasReport":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.report = obj
        
            elif key == "hasDataUrl":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.dataUrls.append(obj)
        
            elif key == "hasInstitution":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.institution = obj
        
            elif key == "hasCiteKey":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.citeKey = obj
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
        
    def getUrls(self) -> list[str]:
        return self.urls

    def setUrls(self, urls:list[str]):
        self.urls = urls

    def addUrl(self, url:str):
        self.urls.append(url)
        
    def getVolume(self) -> str:
        return self.volume

    def setVolume(self, volume:str):
        self.volume = volume

    def getReport(self) -> str:
        return self.report

    def setReport(self, report:str):
        self.report = report

    def getPages(self) -> str:
        return self.pages

    def setPages(self, pages:str):
        self.pages = pages

    def getAbstract(self) -> str:
        return self.abstract

    def setAbstract(self, abstract:str):
        self.abstract = abstract

    def getInstitution(self) -> str:
        return self.institution

    def setInstitution(self, institution:str):
        self.institution = institution

    def getYear(self) -> str:
        return self.year

    def setYear(self, year:str):
        self.year = year

    def getDataUrls(self) -> list[str]:
        return self.dataUrls

    def setDataUrls(self, dataUrls:list[str]):
        self.dataUrls = dataUrls

    def addDataUrl(self, dataUrl:str):
        self.dataUrls.append(dataUrl)
        
    def getIssue(self) -> str:
        return self.issue

    def setIssue(self, issue:str):
        self.issue = issue

    def getType(self) -> str:
        return self.type

    def setType(self, type:str):
        self.type = type

    def getPublisher(self) -> str:
        return self.publisher

    def setPublisher(self, publisher:str):
        self.publisher = publisher

    def getAuthors(self) -> list[Person]:
        return self.authors

    def setAuthors(self, authors:list[Person]):
        self.authors = authors

    def addAuthor(self, author:Person):
        self.authors.append(author)
        
    def getFirstAuthor(self) -> Person:
        return self.firstAuthor

    def setFirstAuthor(self, firstAuthor:Person):
        self.firstAuthor = firstAuthor

    def getTitle(self) -> str:
        return self.title

    def setTitle(self, title:str):
        self.title = title

    def getJournal(self) -> str:
        return self.journal

    def setJournal(self, journal:str):
        self.journal = journal

    def getCiteKey(self) -> str:
        return self.citeKey

    def setCiteKey(self, citeKey:str):
        self.citeKey = citeKey

    def getCitation(self) -> str:
        return self.citation

    def setCitation(self, citation:str):
        self.citation = citation

    def getDOI(self) -> str:
        return self.dOI

    def setDOI(self, dOI:str):
        self.dOI = dOI
