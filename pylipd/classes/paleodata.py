
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.datatable import DataTable
from pylipd.classes.model import Model

class PaleoData:

    def __init__(self):
        self.modeledBy: list[Model] = []
        self.name: str = None
        self.measurementTables: list[DataTable] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#PaleoData"
        self.id = self.ns + "/" + uniqid("PaleoData")

    @staticmethod
    def from_data(id, data) -> 'PaleoData':
        self = PaleoData()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
            elif key == "hasName":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.name = obj
        
            elif key == "hasMeasurementTable":

                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.measurementTables.append(obj)
        
            elif key == "modeledBy":

                for val in value:
                    if "@id" in val:
                        obj = Model.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.modeledBy.append(obj)
            else:
                for val in value:
                    obj = None
                    if "@id" in val:
                        obj = mydata[val["@id"]]
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

        
        if len(self.modeledBy):
            data[self.id]["modeledBy"] = []
        for value_obj in self.modeledBy: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            
            data[self.id]["modeledBy"].append(obj)
        
        if len(self.measurementTables):
            data[self.id]["hasMeasurementTable"] = []
        for value_obj in self.measurementTables: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            
            data[self.id]["hasMeasurementTable"].append(obj)
        
        if self.name:
            value_obj = self.name
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasName"] = [obj]
            

        for key in self.misc:
            value = self.misc[key]
            data[self.id][key] = []
            ptype = None
            tp = type(value).__name__
            if tp == "int":
                ptype = "http://www.w3.org/2001/XMLSchema#integer"
            elif tp == "float":
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
        
    def getName(self) -> str:
        return self.name

    def setName(self, name:str):
        self.name = name

    def getModeledBy(self) -> list[Model]:
        return self.modeledBy

    def setModeledBy(self, modeledBy:list[Model]):
        self.modeledBy = modeledBy

    def addModeledBy(self, modeledBy:Model):
        self.modeledBy.append(modeledBy)
        
    def getMeasurementTables(self) -> list[DataTable]:
        return self.measurementTables

    def setMeasurementTables(self, measurementTables:list[DataTable]):
        self.measurementTables = measurementTables

    def addMeasurementTable(self, measurementTable:DataTable):
        self.measurementTables.append(measurementTable)
        