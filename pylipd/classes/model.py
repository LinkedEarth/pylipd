
##############################
# Auto-generated. Do not Edit
##############################

import re
from pylipd.utils import uniqid
from pylipd.classes.datatable import DataTable

class Model:

    def __init__(self):
        self.ensembleTables: list[DataTable] = []
        self.distributionTables: list[DataTable] = []
        self.code: str = None
        self.summaryTables: list[DataTable] = []
        self.misc = {}
        self.ontns = "http://linked.earth/ontology#"
        self.ns = "http://linked.earth/lipd"
        self.type = "http://linked.earth/ontology#Model"
        self.id = self.ns + "/" + uniqid("Model")

    @staticmethod
    def from_data(id, data) -> 'Model':
        self = Model()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]
        
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
        
            elif key == "hasDistributionTable":

                for val in value:
                    if "@id" in val:
                        obj = DataTable.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            
                    self.distributionTables.append(obj)
        
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

    def to_data(self, data={}):
        data[self.id] = {}
        data[self.id]["type"] = [
            {
                "@id": self.type,
                "@type": "uri"
            }
        ]

        
        if self.code:
            value_obj = self.code
            obj = {
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#string"
            }
            data[self.id]["hasCode"] = [obj]
            
        
        if len(self.ensembleTables):
            data[self.id]["hasEnsembleTable"] = []
        for value_obj in self.ensembleTables: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            
            data[self.id]["hasEnsembleTable"].append(obj)
        
        if len(self.distributionTables):
            data[self.id]["hasDistributionTable"] = []
        for value_obj in self.distributionTables: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            
            data[self.id]["hasDistributionTable"].append(obj)
        
        if len(self.summaryTables):
            data[self.id]["hasSummaryTable"] = []
        for value_obj in self.summaryTables: 
            obj = {
                "@id": value_obj.id,
                "@type": "uri"
            }
            data = value_obj.to_data(data)
            
            data[self.id]["hasSummaryTable"].append(obj)

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
        
    def getSummaryTables(self) -> list[DataTable]:
        return self.summaryTables

    def setSummaryTables(self, summaryTables:list[DataTable]):
        self.summaryTables = summaryTables

    def addSummaryTable(self, summaryTable:DataTable):
        self.summaryTables.append(summaryTable)
        
    def getCode(self) -> str:
        return self.code

    def setCode(self, code:str):
        self.code = code

    def getEnsembleTables(self) -> list[DataTable]:
        return self.ensembleTables

    def setEnsembleTables(self, ensembleTables:list[DataTable]):
        self.ensembleTables = ensembleTables

    def addEnsembleTable(self, ensembleTable:DataTable):
        self.ensembleTables.append(ensembleTable)
        
    def getDistributionTables(self) -> list[DataTable]:
        return self.distributionTables

    def setDistributionTables(self, distributionTables:list[DataTable]):
        self.distributionTables = distributionTables

    def addDistributionTable(self, distributionTable:DataTable):
        self.distributionTables.append(distributionTable)
        