
##############################
# Auto-generated. Do not Edit
##############################
from pylipd.globals.synonyms import SYNONYMS

class PaleoProxyGeneral:
    """Enumeration helper representing LiPD controlled vocabulary term group `PaleoProxyGeneral`.
    AUTO-GENERATED – do not modify by hand.
    """
    synonyms = SYNONYMS["PROXIES"]["PaleoProxyGeneral"]

    def __init__(self, id, label):
        self.id = id
        self.label = label
    
    def __eq__(self, value: object) -> bool:
            self.id == value.id
        
    def getLabel(self):
        """Return the human-readable label for this enumeration value."""
        return self.label

    def getId(self):
        """Return the identifier/URI for this enumeration value."""
        return self.id
    
    def to_data(self, data={}):
        """Serialise this enumeration value to the internal JSON-LD graph format."""
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

    def to_json(self):
        """Return a minimal JSON value (string) corresponding to this synonym."""
        data = self.label
        return data

    @classmethod
    def from_synonym(cls, synonym):
        """Return a new `PaleoProxyGeneral` instance matching a synonym string, or `None`."""
        if synonym.lower() in PaleoProxyGeneral.synonyms:
            synobj = PaleoProxyGeneral.synonyms[synonym.lower()]
            return PaleoProxyGeneral(synobj['id'], synobj['label'])
        return None
        
class PaleoProxyGeneralConstants:
    """Namespace-style container holding pre-instantiated PaleoProxyGeneral enumeration values.
    Each attribute corresponds to one controlled vocabulary entry.
    """
    biogenic = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#biogenic", "biogenic")
    cryophysical = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#cryophysical", "cryophysical")
    dendrophysical = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#dendrophysical", "dendrophysical")
    elemental = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#elemental", "elemental")
    faunal_assemblage = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#faunal_assemblage", "faunal assemblage")
    floral_assemblage = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#floral_assemblage", "floral assemblage")
    isotopic = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#isotopic", "isotopic")
    mineral = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#mineral", "mineral")
    pyrogenic = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#pyrogenic", "pyrogenic")
    sedimentology = PaleoProxyGeneral("http://linked.earth/ontology/paleo_proxy#sedimentology", "sedimentology")