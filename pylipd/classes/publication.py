
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.person import Person

class Publication:
    """Auto-generated LinkedEarth class representing `Publication`."""
    def __init__(self):
        """Initialize a new Publication instance."""
        
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
        """Instantiate `Publication` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        Publication
            The populated `Publication` instance.
        """
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

        if len(self.authors):
            data[self.id]["hasAuthor"] = []
        for value_obj in self.authors:
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

        if len(self.authors):
            data["author"] = []
        for value_obj in self.authors:
            obj = value_obj.to_json()
            data["author"].append(obj)

        if len(self.dataUrls):
            data["dataUrl"] = []
        for value_obj in self.dataUrls:
            obj = value_obj
            data["dataUrl"].append(obj)

        if len(self.urls):
            data["url"] = []
        for value_obj in self.urls:
            obj = value_obj
            data["url"].append(obj)

        if self.abstract:
            value_obj = self.abstract
            obj = value_obj
            data["abstract"] = obj

        if self.citation:
            value_obj = self.citation
            obj = value_obj
            data["citation"] = obj

        if self.citeKey:
            value_obj = self.citeKey
            obj = value_obj
            data["citeKey"] = obj

        if self.dOI:
            value_obj = self.dOI
            obj = value_obj
            data["doi"] = obj

        if self.firstAuthor:
            value_obj = self.firstAuthor
            obj = value_obj.to_json()
            data["firstauthor"] = obj

        if self.institution:
            value_obj = self.institution
            obj = value_obj
            data["institution"] = obj

        if self.issue:
            value_obj = self.issue
            obj = value_obj
            data["issue"] = obj

        if self.journal:
            value_obj = self.journal
            obj = value_obj
            data["journal"] = obj

        if self.pages:
            value_obj = self.pages
            obj = value_obj
            data["pages"] = obj

        if self.publicationType:
            value_obj = self.publicationType
            obj = value_obj
            data["type"] = obj

        if self.publisher:
            value_obj = self.publisher
            obj = value_obj
            data["publisher"] = obj

        if self.report:
            value_obj = self.report
            obj = value_obj
            data["report"] = obj

        if self.title:
            value_obj = self.title
            obj = value_obj
            data["title"] = obj

        if self.volume:
            value_obj = self.volume
            obj = value_obj
            data["volume"] = obj

        if self.year:
            value_obj = self.year
            obj = value_obj
            data["year"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Publication':
        """Instantiate `Publication` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        Publication
            The populated `Publication` instance.
        """
        self = Publication()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "abstract":
                    value = pvalue
                    obj = value
                    self.abstract = obj
            elif key == "author":
                for value in pvalue:
                    obj = Person.from_json(value)
                    self.authors.append(obj)
            elif key == "citation":
                    value = pvalue
                    obj = value
                    self.citation = obj
            elif key == "citeKey":
                    value = pvalue
                    obj = value
                    self.citeKey = obj
            elif key == "dataUrl":
                for value in pvalue:
                    obj = value
                    self.dataUrls.append(obj)
            elif key == "doi":
                    value = pvalue
                    obj = value
                    self.dOI = obj
            elif key == "firstauthor":
                    value = pvalue
                    obj = Person.from_json(value)
                    self.firstAuthor = obj
            elif key == "institution":
                    value = pvalue
                    obj = value
                    self.institution = obj
            elif key == "issue":
                    value = pvalue
                    obj = value
                    self.issue = obj
            elif key == "journal":
                    value = pvalue
                    obj = value
                    self.journal = obj
            elif key == "pages":
                    value = pvalue
                    obj = value
                    self.pages = obj
            elif key == "publisher":
                    value = pvalue
                    obj = value
                    self.publisher = obj
            elif key == "report":
                    value = pvalue
                    obj = value
                    self.report = obj
            elif key == "title":
                    value = pvalue
                    obj = value
                    self.title = obj
            elif key == "type":
                    value = pvalue
                    obj = value
                    self.publicationType = obj
            elif key == "url":
                for value in pvalue:
                    obj = value
                    self.urls.append(obj)
            elif key == "volume":
                    value = pvalue
                    obj = value
                    self.volume = obj
            elif key == "year":
                    value = pvalue
                    obj = value
                    self.year = obj
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
        
    def getAbstract(self) -> str:
        """Get abstract.

        Returns
        -------
        str
            The current value of abstract.
        """
        return self.abstract

    def setAbstract(self, abstract:str):
        """Set abstract.

        Parameters
        ----------
        abstract : str
            The value to assign.
        """
        assert isinstance(abstract, str), f"Error: '{abstract}' is not of type str"
        self.abstract = abstract
    
    def getAuthors(self) -> list[Person]:
        """Get authors list.

        Returns
        -------
        list[Person]
            A list of Person objects.
        """
        return self.authors

    def setAuthors(self, authors:list[Person]):
        """Set the authors list.

        Parameters
        ----------
        authors : list[Person]
            The list to assign.
        """
        assert isinstance(authors, list), "Error: authors is not a list"
        assert all(isinstance(x, Person) for x in authors), f"Error: '{authors}' is not of type Person"
        self.authors = authors

    def addAuthor(self, authors:Person):
        """Add a value to the authors list.

        Parameters
        ----------
        authors : Person
            The value to append.
        """
        assert isinstance(authors, Person), f"Error: '{authors}' is not of type Person"
        self.authors.append(authors)
        
    def getCitation(self) -> str:
        """Get citation.

        Returns
        -------
        str
            The current value of citation.
        """
        return self.citation

    def setCitation(self, citation:str):
        """Set citation.

        Parameters
        ----------
        citation : str
            The value to assign.
        """
        assert isinstance(citation, str), f"Error: '{citation}' is not of type str"
        self.citation = citation
    
    def getCiteKey(self) -> str:
        """Get citeKey.

        Returns
        -------
        str
            The current value of citeKey.
        """
        return self.citeKey

    def setCiteKey(self, citeKey:str):
        """Set citeKey.

        Parameters
        ----------
        citeKey : str
            The value to assign.
        """
        assert isinstance(citeKey, str), f"Error: '{citeKey}' is not of type str"
        self.citeKey = citeKey
    
    def getDOI(self) -> str:
        """Get dOI.

        Returns
        -------
        str
            The current value of dOI.
        """
        return self.dOI

    def setDOI(self, dOI:str):
        """Set dOI.

        Parameters
        ----------
        dOI : str
            The value to assign.
        """
        assert isinstance(dOI, str), f"Error: '{dOI}' is not of type str"
        self.dOI = dOI
    
    def getDataUrls(self) -> list[str]:
        """Get dataUrls list.

        Returns
        -------
        list[str]
            A list of str objects.
        """
        return self.dataUrls

    def setDataUrls(self, dataUrls:list[str]):
        """Set the dataUrls list.

        Parameters
        ----------
        dataUrls : list[str]
            The list to assign.
        """
        assert isinstance(dataUrls, list), "Error: dataUrls is not a list"
        assert all(isinstance(x, str) for x in dataUrls), f"Error: '{dataUrls}' is not of type str"
        self.dataUrls = dataUrls

    def addDataUrl(self, dataUrls:str):
        """Add a value to the dataUrls list.

        Parameters
        ----------
        dataUrls : str
            The value to append.
        """
        assert isinstance(dataUrls, str), f"Error: '{dataUrls}' is not of type str"
        self.dataUrls.append(dataUrls)
        
    def getFirstAuthor(self) -> Person:
        """Get firstAuthor.

        Returns
        -------
        Person
            The current value of firstAuthor.
        """
        return self.firstAuthor

    def setFirstAuthor(self, firstAuthor:Person):
        """Set firstAuthor.

        Parameters
        ----------
        firstAuthor : Person
            The value to assign.
        """
        assert isinstance(firstAuthor, Person), f"Error: '{firstAuthor}' is not of type Person"
        self.firstAuthor = firstAuthor
    
    def getInstitution(self) -> str:
        """Get institution.

        Returns
        -------
        str
            The current value of institution.
        """
        return self.institution

    def setInstitution(self, institution:str):
        """Set institution.

        Parameters
        ----------
        institution : str
            The value to assign.
        """
        assert isinstance(institution, str), f"Error: '{institution}' is not of type str"
        self.institution = institution
    
    def getIssue(self) -> str:
        """Get issue.

        Returns
        -------
        str
            The current value of issue.
        """
        return self.issue

    def setIssue(self, issue:str):
        """Set issue.

        Parameters
        ----------
        issue : str
            The value to assign.
        """
        assert isinstance(issue, str), f"Error: '{issue}' is not of type str"
        self.issue = issue
    
    def getJournal(self) -> str:
        """Get journal.

        Returns
        -------
        str
            The current value of journal.
        """
        return self.journal

    def setJournal(self, journal:str):
        """Set journal.

        Parameters
        ----------
        journal : str
            The value to assign.
        """
        assert isinstance(journal, str), f"Error: '{journal}' is not of type str"
        self.journal = journal
    
    def getPages(self) -> str:
        """Get pages.

        Returns
        -------
        str
            The current value of pages.
        """
        return self.pages

    def setPages(self, pages:str):
        """Set pages.

        Parameters
        ----------
        pages : str
            The value to assign.
        """
        assert isinstance(pages, str), f"Error: '{pages}' is not of type str"
        self.pages = pages
    
    def getPublicationType(self) -> str:
        """Get publicationType.

        Returns
        -------
        str
            The current value of publicationType.
        """
        return self.publicationType

    def setPublicationType(self, publicationType:str):
        """Set publicationType.

        Parameters
        ----------
        publicationType : str
            The value to assign.
        """
        assert isinstance(publicationType, str), f"Error: '{publicationType}' is not of type str"
        self.publicationType = publicationType
    
    def getPublisher(self) -> str:
        """Get publisher.

        Returns
        -------
        str
            The current value of publisher.
        """
        return self.publisher

    def setPublisher(self, publisher:str):
        """Set publisher.

        Parameters
        ----------
        publisher : str
            The value to assign.
        """
        assert isinstance(publisher, str), f"Error: '{publisher}' is not of type str"
        self.publisher = publisher
    
    def getReport(self) -> str:
        """Get report.

        Returns
        -------
        str
            The current value of report.
        """
        return self.report

    def setReport(self, report:str):
        """Set report.

        Parameters
        ----------
        report : str
            The value to assign.
        """
        assert isinstance(report, str), f"Error: '{report}' is not of type str"
        self.report = report
    
    def getTitle(self) -> str:
        """Get title.

        Returns
        -------
        str
            The current value of title.
        """
        return self.title

    def setTitle(self, title:str):
        """Set title.

        Parameters
        ----------
        title : str
            The value to assign.
        """
        assert isinstance(title, str), f"Error: '{title}' is not of type str"
        self.title = title
    
    def getUrls(self) -> list[str]:
        """Get urls list.

        Returns
        -------
        list[str]
            A list of str objects.
        """
        return self.urls

    def setUrls(self, urls:list[str]):
        """Set the urls list.

        Parameters
        ----------
        urls : list[str]
            The list to assign.
        """
        assert isinstance(urls, list), "Error: urls is not a list"
        assert all(isinstance(x, str) for x in urls), f"Error: '{urls}' is not of type str"
        self.urls = urls

    def addUrl(self, urls:str):
        """Add a value to the urls list.

        Parameters
        ----------
        urls : str
            The value to append.
        """
        assert isinstance(urls, str), f"Error: '{urls}' is not of type str"
        self.urls.append(urls)
        
    def getVolume(self) -> str:
        """Get volume.

        Returns
        -------
        str
            The current value of volume.
        """
        return self.volume

    def setVolume(self, volume:str):
        """Set volume.

        Parameters
        ----------
        volume : str
            The value to assign.
        """
        assert isinstance(volume, str), f"Error: '{volume}' is not of type str"
        self.volume = volume
    
    def getYear(self) -> int:
        """Get year.

        Returns
        -------
        int
            The current value of year.
        """
        return self.year

    def setYear(self, year:int):
        """Set year.

        Parameters
        ----------
        year : int
            The value to assign.
        """
        assert isinstance(year, int), f"Error: '{year}' is not of type int"
        self.year = year
    