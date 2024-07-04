
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.model import Model
from pylipd.classes.datatable import DataTable

class ChronData:

    def __init__(self):
        self.measurementTables: list[DataTable] = []
        self.modeledBys: list[Model] = []
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'ChronData':
        self = ChronData()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
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
            
                    self.modeledBys.append(obj)
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
        
    def getModeledBys(self) -> list[Model]:
        return self.modeledBys

    def setModeledBys(self, modeledBys:list[Model]):
        self.modeledBys = modeledBys

    def addModeledBy(self, modeledBy:Model):
        self.modeledBys.append(modeledBy)
        
    def getMeasurementTables(self) -> list[DataTable]:
        return self.measurementTables

    def setMeasurementTables(self, measurementTables:list[DataTable]):
        self.measurementTables = measurementTables

    def addMeasurementTable(self, measurementTable:DataTable):
        self.measurementTables.append(measurementTable)
        