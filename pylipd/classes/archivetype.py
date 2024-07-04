
##############################
# Auto-generated. Do not Edit
##############################

from ..globals.synonyms import SYNONYMS

class ArchiveType:
    synonyms = SYNONYMS["ARCHIVES"]["ArchiveType"]

    def __init__(self, id, label):
        self.id = id
        self.label = label
    
    def __eq__(self, value: object) -> bool:
            self.id == value.id
        
    def getLabel(self):
        return self.label

    def getId(self):
        return self.id
    
    def to_data(self, data={}):
        data[self.id] ={
            "label": [
                {
                    "@datatype": None,
                    "@type": "literal",
                    "@value": self.label
                }
            ]
        }
        return data
    
    @classmethod
    def from_synonym(cls, synonym):
        if synonym.lower() in ArchiveType.synonyms:
            synobj = ArchiveType.synonyms[synonym.lower()]
            return ArchiveType(synobj['id'], synobj['label'])
        return None
    
class ArchiveTypeConstants:
    Borehole = ArchiveType("http://linked.earth/ontology/archive#Borehole", "Borehole")
    Coral = ArchiveType("http://linked.earth/ontology/archive#Coral", "Coral")
    FluvialSediment = ArchiveType("http://linked.earth/ontology/archive#FluvialSediment", "Fluvial sediment")
    GlacierIce = ArchiveType("http://linked.earth/ontology/archive#GlacierIce", "Glacier ice")
    GroundIce = ArchiveType("http://linked.earth/ontology/archive#GroundIce", "Ground ice")
    LakeSediment = ArchiveType("http://linked.earth/ontology/archive#LakeSediment", "Lake sediment")
    MarineSediment = ArchiveType("http://linked.earth/ontology/archive#MarineSediment", "Marine sediment")
    Midden = ArchiveType("http://linked.earth/ontology/archive#Midden", "Midden")
    MolluskShell = ArchiveType("http://linked.earth/ontology/archive#MolluskShell", "Mollusk shell")
    Peat = ArchiveType("http://linked.earth/ontology/archive#Peat", "Peat")
    Sclerosponge = ArchiveType("http://linked.earth/ontology/archive#Sclerosponge", "Sclerosponge")
    Shoreline = ArchiveType("http://linked.earth/ontology/archive#Shoreline", "Shoreline")
    Speleothem = ArchiveType("http://linked.earth/ontology/archive#Speleothem", "Speleothem")
    TerrestrialSediment = ArchiveType("http://linked.earth/ontology/archive#TerrestrialSediment", "Terrestrial sediment")
    Wood = ArchiveType("http://linked.earth/ontology/archive#Wood", "Wood")
    Documents = ArchiveType("http://linked.earth/ontology/archive#Documents", "Documents")
    Other = ArchiveType("http://linked.earth/ontology/archive#Other", "Other")