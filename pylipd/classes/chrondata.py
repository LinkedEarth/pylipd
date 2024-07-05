
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.datatable import DataTable
from pylipd.classes.model import Model

class ChronData:

    def __init__(self):
        self.measurementTables: list[DataTable] = []
        self.modeledBy: list[Model] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#ChronData"
        self.id = self.ns + "/" + uniqid("ChronData.")

    @staticmethod
    def from_data(id, data) -> 'ChronData':
        self = ChronData()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
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

        if len(self.measurementTables):
            data[self.id]["hasMeasurementTable"] = []
        for value_obj in self.measurementTables:
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
            data[self.id]["hasMeasurementTable"].append(obj)

        if len(self.modeledBy):
            data[self.id]["modeledBy"] = []
        for value_obj in self.modeledBy:
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
            data[self.id]["modeledBy"].append(obj)
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

    def to_json(self):
        data = {
            "@id": self.id
        }

        if len(self.measurementTables):
            data["measurementTable"] = []
        for value_obj in self.measurementTables:
            obj = value_obj.to_json()
            data["measurementTable"].append(obj)

        if len(self.modeledBy):
            data["model"] = []
        for value_obj in self.modeledBy:
            obj = value_obj.to_json()
            data["model"].append(obj)

        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data

    @staticmethod
    def from_json(data) -> 'ChronData':
        self = ChronData()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue
            elif key == "measurementTable":
                for value in pvalue:
                    obj = DataTable.from_json(value)
                    self.measurementTables.append(obj)
            elif key == "model":
                for value in pvalue:
                    obj = Model.from_json(value)
                    self.modeledBy.append(obj)
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
        
    def getMeasurementTables(self) -> list[DataTable]:
        return self.measurementTables

    def setMeasurementTables(self, measurementTables:list[DataTable]):
        self.measurementTables = measurementTables

    def addMeasurementTable(self, measurementTables:DataTable):
        self.measurementTables.append(measurementTables)
        
    def getModeledBy(self) -> list[Model]:
        return self.modeledBy

    def setModeledBy(self, modeledBy:list[Model]):
        self.modeledBy = modeledBy

    def addModeledBy(self, modeledBy:Model):
        self.modeledBy.append(modeledBy)
        