
##############################
# Auto-generated. Do not Edit
##############################

import re

class Location:

    def __init__(self):
        self.latitude: str = None
        self.description: str = None
        self.countryOcean: str = None
        self.ocean: str = None
        self.siteName: str = None
        self.locationName: str = None
        self.country: str = None
        self.geometryType: str = None
        self.continent: str = None
        self.notes: str = None
        self.coordinatesFor: None = None
        self.longitude: str = None
        self.elevation: str = None
        self.coordinates: list = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Location':
        self = Location()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasGeometryType":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.geometryType = obj
        
            elif key == "hasCountryOcean":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.countryOcean = obj
        
            elif key == "hasLocationName":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.locationName = obj
        
            elif key == "hasLatitude":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.latitude = obj
        
            elif key == "coordinates":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.coordinates = obj
        
            elif key == "hasContinent":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.continent = obj
        
            elif key == "hasNotes":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
        
            elif key == "hasSiteName":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.siteName = obj
        
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
        
            elif key == "hasLongitude":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.longitude = obj
        
            elif key == "hasCountry":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.country = obj
        
            elif key == "coordinatesFor":

                for val in value:
                    obj = val["@id"]                        
                    self.coordinatesFor = obj
        
            elif key == "hasOcean":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.ocean = obj
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
        
    def getDescription(self) -> str:
        return self.description

    def setDescription(self, description:str):
        self.description = description

    def getGeometryType(self) -> str:
        return self.geometryType

    def setGeometryType(self, geometryType:str):
        self.geometryType = geometryType

    def getLatitude(self) -> str:
        return self.latitude

    def setLatitude(self, latitude:str):
        self.latitude = latitude

    def getLocationName(self) -> str:
        return self.locationName

    def setLocationName(self, locationName:str):
        self.locationName = locationName

    def getSiteName(self) -> str:
        return self.siteName

    def setSiteName(self, siteName:str):
        self.siteName = siteName

    def getCoordinatesFor(self) -> None:
        return self.coordinatesFor

    def setCoordinatesFor(self, coordinatesFor:None):
        self.coordinatesFor = coordinatesFor

    def getOcean(self) -> str:
        return self.ocean

    def setOcean(self, ocean:str):
        self.ocean = ocean

    def getCountry(self) -> str:
        return self.country

    def setCountry(self, country:str):
        self.country = country

    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes

    def getCoordinates(self) -> list:
        return self.coordinates

    def setCoordinates(self, coordinates:list):
        self.coordinates = coordinates

    def getCountryOcean(self) -> str:
        return self.countryOcean

    def setCountryOcean(self, countryOcean:str):
        self.countryOcean = countryOcean

    def getLongitude(self) -> str:
        return self.longitude

    def setLongitude(self, longitude:str):
        self.longitude = longitude

    def getContinent(self) -> str:
        return self.continent

    def setContinent(self, continent:str):
        self.continent = continent

    def getElevation(self) -> str:
        return self.elevation

    def setElevation(self, elevation:str):
        self.elevation = elevation
