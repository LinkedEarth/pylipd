
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.person import Person

class Publication:

    def __init__(self):
        self.abstract: str = None
        self.authors: list[Person] = []
        self.citation: str = None
        self.citeKey: str = None
        self.dOI: str = None
        self.dataUrls: list[str] = []
        self.firstAuthor: Person = None
        self.institution: str = None
        self.issue: str = None
        self.journal: str = None
        self.pages: str = None
        self.publicationType: str = None
        self.publisher: str = None
        self.report: str = None
        self.title: str = None
        self.urls: list[str] = []
        self.volume: str = None
        self.year: int = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Publication"
        self.id = self.ns + "/" + uniqid("Publication.")

    @staticmethod
    def from_data(id, data) -> 'Publication':
        self = Publication()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasAbstract":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.abstract = obj
        
            elif key == "hasAuthor":
                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.authors.append(obj)
        
            elif key == "hasCitation":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.citation = obj
        
            elif key == "hasCiteKey":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.citeKey = obj
        
            elif key == "hasDOI":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.dOI = obj
        
            elif key == "hasDataUrl":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.dataUrls.append(obj)
        
            elif key == "hasFirstAuthor":
                for val in value:
                    if "@id" in val:
                        obj = Person.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
                                    
                    self.firstAuthor = obj
        
            elif key == "hasInstitution":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.institution = obj
        
            elif key == "hasIssue":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.issue = obj
        
            elif key == "hasJournal":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.journal = obj
        
            elif key == "hasPages":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.pages = obj
        
            elif key == "hasPublisher":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.publisher = obj
        
            elif key == "hasReport":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.report = obj
        
            elif key == "hasTitle":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.title = obj
        
            elif key == "hasType":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.publicationType = obj
        
            elif key == "hasUrl":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]
                    self.urls.append(obj)
        
            elif key == "hasVolume":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.volume = obj
        
            elif key == "hasYear":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.year = obj
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

        if len(self.authors):
            data[self.id]["hasAuthor"] = []
        for value_obj in self.authors: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasAuthor"].append(obj)

        if len(self.dataUrls):
            data[self.id]["hasDataUrl"] = []
        for value_obj in self.dataUrls:
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDataUrl"].append(obj)

        if len(self.urls):
            data[self.id]["hasUrl"] = []
        for value_obj in self.urls:
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasUrl"].append(obj)

        if self.abstract:
            value_obj = self.abstract
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasAbstract"] = [obj]
                

        if self.citation:
            value_obj = self.citation
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCitation"] = [obj]
                

        if self.citeKey:
            value_obj = self.citeKey
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCiteKey"] = [obj]
                

        if self.dOI:
            value_obj = self.dOI
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDOI"] = [obj]
                

        if self.firstAuthor:
            value_obj = self.firstAuthor 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            data[self.id]["hasFirstAuthor"] = [obj]
                

        if self.institution:
            value_obj = self.institution
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasInstitution"] = [obj]
                

        if self.issue:
            value_obj = self.issue
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasIssue"] = [obj]
                

        if self.journal:
            value_obj = self.journal
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasJournal"] = [obj]
                

        if self.pages:
            value_obj = self.pages
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasPages"] = [obj]
                

        if self.publicationType:
            value_obj = self.publicationType
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasType"] = [obj]
                

        if self.publisher:
            value_obj = self.publisher
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasPublisher"] = [obj]
                

        if self.report:
            value_obj = self.report
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasReport"] = [obj]
                

        if self.title:
            value_obj = self.title
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasTitle"] = [obj]
                

        if self.volume:
            value_obj = self.volume
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasVolume"] = [obj]
                

        if self.year:
            value_obj = self.year
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#integer"
            }
            data[self.id]["hasYear"] = [obj]
                
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
        
    def getAbstract(self) -> str:
        return self.abstract

    def setAbstract(self, abstract:str):
        self.abstract = abstract
    
    def getAuthors(self) -> list[Person]:
        return self.authors

    def setAuthors(self, authors:list[Person]):
        self.authors = authors

    def addAuthor(self, authors:Person):
        self.authors.append(authors)
        
    def getCitation(self) -> str:
        return self.citation

    def setCitation(self, citation:str):
        self.citation = citation
    
    def getCiteKey(self) -> str:
        return self.citeKey

    def setCiteKey(self, citeKey:str):
        self.citeKey = citeKey
    
    def getDOI(self) -> str:
        return self.dOI

    def setDOI(self, dOI:str):
        self.dOI = dOI
    
    def getDataUrls(self) -> list[str]:
        return self.dataUrls

    def setDataUrls(self, dataUrls:list[str]):
        self.dataUrls = dataUrls

    def addDataUrl(self, dataUrls:str):
        self.dataUrls.append(dataUrls)
        
    def getFirstAuthor(self) -> Person:
        return self.firstAuthor

    def setFirstAuthor(self, firstAuthor:Person):
        self.firstAuthor = firstAuthor
    
    def getInstitution(self) -> str:
        return self.institution

    def setInstitution(self, institution:str):
        self.institution = institution
    
    def getIssue(self) -> str:
        return self.issue

    def setIssue(self, issue:str):
        self.issue = issue
    
    def getJournal(self) -> str:
        return self.journal

    def setJournal(self, journal:str):
        self.journal = journal
    
    def getPages(self) -> str:
        return self.pages

    def setPages(self, pages:str):
        self.pages = pages
    
    def getPublicationType(self) -> str:
        return self.publicationType

    def setPublicationType(self, publicationType:str):
        self.publicationType = publicationType
    
    def getPublisher(self) -> str:
        return self.publisher

    def setPublisher(self, publisher:str):
        self.publisher = publisher
    
    def getReport(self) -> str:
        return self.report

    def setReport(self, report:str):
        self.report = report
    
    def getTitle(self) -> str:
        return self.title

    def setTitle(self, title:str):
        self.title = title
    
    def getUrls(self) -> list[str]:
        return self.urls

    def setUrls(self, urls:list[str]):
        self.urls = urls

    def addUrl(self, urls:str):
        self.urls.append(urls)
        
    def getVolume(self) -> str:
        return self.volume

    def setVolume(self, volume:str):
        self.volume = volume
    
    def getYear(self) -> int:
        return self.year

    def setYear(self, year:int):
        self.year = year
    