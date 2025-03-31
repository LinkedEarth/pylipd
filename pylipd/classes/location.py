
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid

class Location:

    def __init__(self):
        self.continent: str = None
        self.coordinates: str = None
        self.coordinatesFor: None = None
        self.country: str = None
        self.countryOcean: str = None
        self.description: str = None
        self.elevation: str = None
        self.geometryType: str = None
        self.latitude: str = None
        self.locationName: str = None
        self.locationType: str = None
        self.longitude: str = None
        self.notes: str = None
        self.ocean: str = None
        self.siteName: str = None
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Location"
        self.id = self.ns + "/" + uniqid("Location.")

    @staticmethod
    def from_data(id, data) -> 'Location':
        self = Location()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "coordinates":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.coordinates = obj
        
            elif key == "coordinatesFor":
                for val in value:
                    obj = val["@id"]                        
                    self.coordinatesFor = obj
        
            elif key == "hasContinent":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.continent = obj
        
            elif key == "hasCountry":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.country = obj
        
            elif key == "hasCountryOcean":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.countryOcean = obj
        
            elif key == "hasDescription":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.description = obj
        
            elif key == "hasElevation":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.elevation = obj
        
            elif key == "hasGeometryType":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.geometryType = obj
        
            elif key == "hasLatitude":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.latitude = obj
        
            elif key == "hasLocationName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.locationName = obj
        
            elif key == "hasLongitude":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.longitude = obj
        
            elif key == "hasNotes":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasOcean":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.ocean = obj
        
            elif key == "hasSiteName":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.siteName = obj
        
            elif key == "hasType":
                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.locationType = obj
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

        if self.continent:
            value_obj = self.continent
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasContinent"] = [obj]
                

        if self.coordinates:
            value_obj = self.coordinates
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["coordinates"] = [obj]
                

        if self.coordinatesFor:
            value_obj = self.coordinatesFor
            obj = {
                "@id": value_obj,
                "@type": "uri"
            }
            data[self.id]["coordinatesFor"] = [obj]
                

        if self.country:
            value_obj = self.country
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCountry"] = [obj]
                

        if self.countryOcean:
            value_obj = self.countryOcean
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCountryOcean"] = [obj]
                

        if self.description:
            value_obj = self.description
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasDescription"] = [obj]
                

        if self.elevation:
            value_obj = self.elevation
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasElevation"] = [obj]
                

        if self.geometryType:
            value_obj = self.geometryType
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasGeometryType"] = [obj]
                

        if self.latitude:
            value_obj = self.latitude
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasLatitude"] = [obj]
                

        if self.locationName:
            value_obj = self.locationName
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasLocationName"] = [obj]
                

        if self.locationType:
            value_obj = self.locationType
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasType"] = [obj]
                

        if self.longitude:
            value_obj = self.longitude
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasLongitude"] = [obj]
                

        if self.notes:
            value_obj = self.notes
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasNotes"] = [obj]
                

        if self.ocean:
            value_obj = self.ocean
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasOcean"] = [obj]
                

        if self.siteName:
            value_obj = self.siteName
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasSiteName"] = [obj]
                
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
        data = {
            "@id": self.id
        }

        if self.continent:
            value_obj = self.continent
            obj = value_obj
            data["continent"] = obj

        if self.coordinates:
            value_obj = self.coordinates
            obj = value_obj
            data["coordinates"] = obj

        if self.coordinatesFor:
            value_obj = self.coordinatesFor
            obj = value_obj
            data["coordinatesFor"] = obj

        if self.country:
            value_obj = self.country
            obj = value_obj
            data["country"] = obj

        if self.countryOcean:
            value_obj = self.countryOcean
            obj = value_obj
            data["countryOcean"] = obj

        if self.description:
            value_obj = self.description
            obj = value_obj
            data["description"] = obj

        if self.elevation:
            value_obj = self.elevation
            obj = value_obj
            data["elevation"] = obj

        if self.geometryType:
            value_obj = self.geometryType
            obj = value_obj
            data["geometryType"] = obj

        if self.latitude:
            value_obj = self.latitude
            obj = value_obj
            data["latitude"] = obj

        if self.locationName:
            value_obj = self.locationName
            obj = value_obj
            data["locationName"] = obj

        if self.locationType:
            value_obj = self.locationType
            obj = value_obj
            data["type"] = obj

        if self.longitude:
            value_obj = self.longitude
            obj = value_obj
            data["longitude"] = obj

        if self.notes:
            value_obj = self.notes
            obj = value_obj
            data["notes"] = obj

        if self.ocean:
            value_obj = self.ocean
            obj = value_obj
            data["ocean"] = obj

        if self.siteName:
            value_obj = self.siteName
            obj = value_obj
            data["siteName"] = obj

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'Location':
        self = Location()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "continent":
                    value = pvalue
                    obj = value
                    self.continent = obj
            elif key == "coordinates":
                    value = pvalue
                    obj = value
                    self.coordinates = obj
            elif key == "coordinatesFor":
                    value = pvalue
                    obj = value
                    self.coordinatesFor = obj
            elif key == "country":
                    value = pvalue
                    obj = value
                    self.country = obj
            elif key == "countryOcean":
                    value = pvalue
                    obj = value
                    self.countryOcean = obj
            elif key == "description":
                    value = pvalue
                    obj = value
                    self.description = obj
            elif key == "elevation":
                    value = pvalue
                    obj = value
                    self.elevation = obj
            elif key == "geometryType":
                    value = pvalue
                    obj = value
                    self.geometryType = obj
            elif key == "latitude":
                    value = pvalue
                    obj = value
                    self.latitude = obj
            elif key == "locationName":
                    value = pvalue
                    obj = value
                    self.locationName = obj
            elif key == "longitude":
                    value = pvalue
                    obj = value
                    self.longitude = obj
            elif key == "notes":
                    value = pvalue
                    obj = value
                    self.notes = obj
            elif key == "ocean":
                    value = pvalue
                    obj = value
                    self.ocean = obj
            elif key == "siteName":
                    value = pvalue
                    obj = value
                    self.siteName = obj
            elif key == "type":
                    value = pvalue
                    obj = value
                    self.locationType = obj
            else:
                self.set_non_standard_property(key, pvalue)
                   
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
        
    def getContinent(self) -> str:
        return self.continent

    def setContinent(self, continent:str):
        assert isinstance(continent, str), f"Error: '{continent}' is not of type str"
        self.continent = continent
    
    def getCoordinates(self) -> str:
        return self.coordinates

    def setCoordinates(self, coordinates:str):
        assert isinstance(coordinates, str), f"Error: '{coordinates}' is not of type str"
        self.coordinates = coordinates
    
    def getCoordinatesFor(self) -> object:
        return self.coordinatesFor

    def setCoordinatesFor(self, coordinatesFor:object):
        assert isinstance(coordinatesFor, object), f"Error: '{coordinatesFor}' is not of type object"
        self.coordinatesFor = coordinatesFor
    
    def getCountry(self) -> str:
        return self.country

    def setCountry(self, country:str):
        assert isinstance(country, str), f"Error: '{country}' is not of type str"
        self.country = country
    
    def getCountryOcean(self) -> str:
        return self.countryOcean

    def setCountryOcean(self, countryOcean:str):
        assert isinstance(countryOcean, str), f"Error: '{countryOcean}' is not of type str"
        self.countryOcean = countryOcean
    
    def getDescription(self) -> str:
        return self.description

    def setDescription(self, description:str):
        assert isinstance(description, str), f"Error: '{description}' is not of type str"
        self.description = description
    
    def getElevation(self) -> str:
        return self.elevation

    def setElevation(self, elevation:str):
        assert isinstance(elevation, str), f"Error: '{elevation}' is not of type str"
        self.elevation = elevation
    
    def getGeometryType(self) -> str:
        return self.geometryType

    def setGeometryType(self, geometryType:str):
        assert isinstance(geometryType, str), f"Error: '{geometryType}' is not of type str"
        self.geometryType = geometryType
    
    def getLatitude(self) -> str:
        return self.latitude

    def setLatitude(self, latitude:str):
        assert isinstance(latitude, str), f"Error: '{latitude}' is not of type str"
        self.latitude = latitude
    
    def getLocationName(self) -> str:
        return self.locationName

    def setLocationName(self, locationName:str):
        assert isinstance(locationName, str), f"Error: '{locationName}' is not of type str"
        self.locationName = locationName
    
    def getLocationType(self) -> str:
        return self.locationType

    def setLocationType(self, locationType:str):
        assert isinstance(locationType, str), f"Error: '{locationType}' is not of type str"
        self.locationType = locationType
    
    def getLongitude(self) -> str:
        return self.longitude

    def setLongitude(self, longitude:str):
        assert isinstance(longitude, str), f"Error: '{longitude}' is not of type str"
        self.longitude = longitude
    
    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        assert isinstance(notes, str), f"Error: '{notes}' is not of type str"
        self.notes = notes
    
    def getOcean(self) -> str:
        return self.ocean

    def setOcean(self, ocean:str):
        assert isinstance(ocean, str), f"Error: '{ocean}' is not of type str"
        self.ocean = ocean
    
    def getSiteName(self) -> str:
        return self.siteName

    def setSiteName(self, siteName:str):
        assert isinstance(siteName, str), f"Error: '{siteName}' is not of type str"
        self.siteName = siteName
    