
##############################
# Auto-generated. Do not Edit
##############################

import re

class ChangeLog:

    def __init__(self):
        self.changes: None = None
        self.notes: str = None
        self.misc = {}

    @staticmethod
    def from_data(id, data) -> 'ChangeLog':
        self = ChangeLog()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue
        
            elif key == "hasChanges":

                for val in value:
                    obj = val["@id"]                        
                    self.changes = obj
        
            elif key == "hasNotes":

                for val in value:
                    if "@value" in val:
                        obj = val["@value"]                        
                    self.notes = obj
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
        
    def getChanges(self) -> None:
        return self.changes

    def setChanges(self, changes:None):
        self.changes = changes

    def getNotes(self) -> str:
        return self.notes

    def setNotes(self, notes:str):
        self.notes = notes
