
##############################
# Auto-generated. Do not Edit
##############################
from pylipd.globals.synonyms import SYNONYMS

class PaleoProxyGeneral:
    """Controlled-vocabulary class for `PaleoProxyGeneral` terms."""
    synonyms = SYNONYMS["PROXIES"]["PaleoProxyGeneral"]

    def __init__(self, id, label):
        """Initialize a PaleoProxyGeneral term.

        Parameters
        ----------
        id : str
            The full URI identifier for this term.
        label : str
            The human-readable label for this term.
        """
        self.id = id
        self.label = label
    
    def __eq__(self, value: object) -> bool:
        """Check equality based on term ID.

        Parameters
        ----------
        value : object
            The object to compare against.

        Returns
        -------
        bool
            True if the IDs match, False otherwise.
        """
        return self.id == value.id
        
    def getLabel(self):
        """Return the human-readable label of the term.

        Returns
        -------
        str
            The label for this term.
        """
        return self.label

    def getId(self):
        """Return the full URI identifier of the term.

        Returns
        -------
        str
            The URI identifier for this term.
        """
        return self.id
    
    def to_data(self, data={}):
        """Serialize this term to JSON-LD format.

        Parameters
        ----------
        data : dict, optional
            Existing data dictionary to extend.

        Returns
        -------
        dict
            The updated data dictionary.
        """
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
        """Return the plain-text label (used in lightweight JSON).

        Returns
        -------
        str
            The label for this term.
        """
        data = self.label
        return data

    @classmethod
    def from_synonym(cls, synonym):
        """Create a PaleoProxyGeneral instance from a synonym string.

        Parameters
        ----------
        synonym : str
            A synonym or alternative name for the term.

        Returns
        -------
        PaleoProxyGeneral or None
            The PaleoProxyGeneral instance if found, None otherwise.
        """
        if synonym.lower() in PaleoProxyGeneral.synonyms:
            synobj = PaleoProxyGeneral.synonyms[synonym.lower()]
            return PaleoProxyGeneral(synobj['id'], synobj['label'])
        return None
        
class PaleoProxyGeneralConstants:
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