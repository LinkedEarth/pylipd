
##############################
# Auto-generated. Do not Edit
##############################
from pylipd.globals.synonyms import SYNONYMS

class ArchiveType:
    """Controlled-vocabulary class for `ArchiveType` terms."""
    synonyms = SYNONYMS["ARCHIVES"]["ArchiveType"]

    def __init__(self, id, label):
        """Initialize a ArchiveType term.

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
        """Create a ArchiveType instance from a synonym string.

        Parameters
        ----------
        synonym : str
            A synonym or alternative name for the term.

        Returns
        -------
        ArchiveType or None
            The ArchiveType instance if found, None otherwise.
        """
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