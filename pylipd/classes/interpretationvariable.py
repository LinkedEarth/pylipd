
##############################
# Auto-generated. Do not Edit
##############################

from ..globals.synonyms import SYNONYMS

class InterpretationVariable:
    synonyms = SYNONYMS["INTERPRETATION"]["InterpretationVariable"]

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
        if synonym.lower() in InterpretationVariable.synonyms:
            synobj = InterpretationVariable.synonyms[synonym.lower()]
            return InterpretationVariable(synobj['id'], synobj['label'])
        return None
    
class InterpretationVariableConstants:
    C3C4Ratio = InterpretationVariable("http://linked.earth/ontology/interpretation#C3C4Ratio", "C3C4Ratio")
    circulationIndex = InterpretationVariable("http://linked.earth/ontology/interpretation#circulationIndex", "circulationIndex")
    circulationVariable = InterpretationVariable("http://linked.earth/ontology/interpretation#circulationVariable", "circulationVariable")
    dissolvedOxygen = InterpretationVariable("http://linked.earth/ontology/interpretation#dissolvedOxygen", "dissolvedOxygen")
    dust = InterpretationVariable("http://linked.earth/ontology/interpretation#dust", "dust")
    ELA = InterpretationVariable("http://linked.earth/ontology/interpretation#ELA", "ELA")
    evaporation = InterpretationVariable("http://linked.earth/ontology/interpretation#evaporation", "evaporation")
    fire = InterpretationVariable("http://linked.earth/ontology/interpretation#fire", "fire")
    growingDegreeDays = InterpretationVariable("http://linked.earth/ontology/interpretation#growingDegreeDays", "growingDegreeDays")
    hydrologicBalance = InterpretationVariable("http://linked.earth/ontology/interpretation#hydrologicBalance", "hydrologicBalance")
    lakeWaterIsotope = InterpretationVariable("http://linked.earth/ontology/interpretation#lakeWaterIsotope", "lakeWaterIsotope")
    meltwater = InterpretationVariable("http://linked.earth/ontology/interpretation#meltwater", "meltwater")
    needsToBeReplaced = InterpretationVariable("http://linked.earth/ontology/interpretation#needsToBeReplaced", "needsToBeReplaced")
    P_E = InterpretationVariable("http://linked.earth/ontology/interpretation#P-E", "P-E")
    precipitation = InterpretationVariable("http://linked.earth/ontology/interpretation#precipitation", "precipitation")
    precipitationDeuteriumExcess = InterpretationVariable("http://linked.earth/ontology/interpretation#precipitationDeuteriumExcess", "precipitationDeuteriumExcess")
    precipitationIsotope = InterpretationVariable("http://linked.earth/ontology/interpretation#precipitationIsotope", "precipitationIsotope")
    productivity = InterpretationVariable("http://linked.earth/ontology/interpretation#productivity", "productivity")
    relativeHumidity = InterpretationVariable("http://linked.earth/ontology/interpretation#relativeHumidity", "relativeHumidity")
    salinity = InterpretationVariable("http://linked.earth/ontology/interpretation#salinity", "salinity")
    seaIce = InterpretationVariable("http://linked.earth/ontology/interpretation#seaIce", "seaIce")
    seasonality = InterpretationVariable("http://linked.earth/ontology/interpretation#seasonality", "seasonality")
    seawaterIsotope = InterpretationVariable("http://linked.earth/ontology/interpretation#seawaterIsotope", "seawaterIsotope")
    streamflow = InterpretationVariable("http://linked.earth/ontology/interpretation#streamflow", "streamflow")
    sunlight = InterpretationVariable("http://linked.earth/ontology/interpretation#sunlight", "sunlight")
    surfacePressure = InterpretationVariable("http://linked.earth/ontology/interpretation#surfacePressure", "surfacePressure")
    temperature = InterpretationVariable("http://linked.earth/ontology/interpretation#temperature", "temperature")
    upwelling = InterpretationVariable("http://linked.earth/ontology/interpretation#upwelling", "upwelling")
    windSpeed = InterpretationVariable("http://linked.earth/ontology/interpretation#windSpeed", "windSpeed")