
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.classes.datatable import DataTable

class Model:

    def __init__(self):
        self.distributionTables: list[DataTable] = []
        self.ensembleTables: list[DataTable] = []
        self.code: str = None
        self.summaryTables: list[DataTable] = []
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'Model':
        self = Model()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasDistributionTable":

                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.distributionTables.append(obj)
        
            elif key == "hasEnsembleTable":

                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.ensembleTables.append(obj)
        
            elif key == "hasSummaryTable":

                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.summaryTables.append(obj)
        
            elif key == "hasCode":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.code = obj
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
        
    def getDistributionTables(self) -> list[DataTable]:
        return self.distributionTables

    def setDistributionTables(self, distributionTables:list[DataTable]):
        self.distributionTables = distributionTables

    def addDistributionTable(self, distributionTable:DataTable):
        self.distributionTables.append(distributionTable)
        
    def getEnsembleTables(self) -> list[DataTable]:
        return self.ensembleTables

    def setEnsembleTables(self, ensembleTables:list[DataTable]):
        self.ensembleTables = ensembleTables

    def addEnsembleTable(self, ensembleTable:DataTable):
        self.ensembleTables.append(ensembleTable)
        
    def getCode(self) -> str:
        return self.code

    def setCode(self, code:str):
        self.code = code

    def getSummaryTables(self) -> list[DataTable]:
        return self.summaryTables

    def setSummaryTables(self, summaryTables:list[DataTable]):
        self.summaryTables = summaryTables

    def addSummaryTable(self, summaryTable:DataTable):
        self.summaryTables.append(summaryTable)
        