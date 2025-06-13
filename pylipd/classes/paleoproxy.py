
##############################
# Auto-generated. Do not Edit
##############################
from pylipd.globals.synonyms import SYNONYMS

class PaleoProxy:
    """Controlled-vocabulary class for `PaleoProxy` terms."""
    synonyms = SYNONYMS["PROXIES"]["PaleoProxy"]

    def __init__(self, id, label):
        """Initialize a PaleoProxy term.

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
        """Create a PaleoProxy instance from a synonym string.

        Parameters
        ----------
        synonym : str
            A synonym or alternative name for the term.

        Returns
        -------
        PaleoProxy or None
            The PaleoProxy instance if found, None otherwise.
        """
        if synonym.lower() in PaleoProxy.synonyms:
            synobj = PaleoProxy.synonyms[synonym.lower()]
            return PaleoProxy(synobj['id'], synobj['label'])
        return None
        
class PaleoProxyConstants:
    accumulation_rate = PaleoProxy("http://linked.earth/ontology/paleo_proxy#accumulation_rate", "accumulation rate")
    ACL = PaleoProxy("http://linked.earth/ontology/paleo_proxy#ACL", "ACL")
    Al2O3 = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Al2O3", "Al2O3")
    alkenone = PaleoProxy("http://linked.earth/ontology/paleo_proxy#alkenone", "alkenone")
    amoeba = PaleoProxy("http://linked.earth/ontology/paleo_proxy#amoeba", "amoeba")
    Ba_Al = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Ba_Al", "Ba/Al")
    Ba_Ca = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Ba_Ca", "Ba/Ca")
    biomarker = PaleoProxy("http://linked.earth/ontology/paleo_proxy#biomarker", "biomarker")
    BIT = PaleoProxy("http://linked.earth/ontology/paleo_proxy#BIT", "BIT")
    borehole = PaleoProxy("http://linked.earth/ontology/paleo_proxy#borehole", "borehole")
    BSi = PaleoProxy("http://linked.earth/ontology/paleo_proxy#BSi", "BSi")
    bubble_frequency = PaleoProxy("http://linked.earth/ontology/paleo_proxy#bubble_frequency", "bubble frequency")
    bulk_density = PaleoProxy("http://linked.earth/ontology/paleo_proxy#bulk_density", "bulk density")
    bulk_sediment = PaleoProxy("http://linked.earth/ontology/paleo_proxy#bulk_sediment", "bulk sediment")
    C_N = PaleoProxy("http://linked.earth/ontology/paleo_proxy#C_N", "C/N")
    Ca_K = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Ca_K", "Ca/K")
    Ca_Ti = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Ca_Ti", "Ca/Ti")
    CaCO3 = PaleoProxy("http://linked.earth/ontology/paleo_proxy#CaCO3", "CaCO3")
    calcification_rate = PaleoProxy("http://linked.earth/ontology/paleo_proxy#calcification_rate", "calcification rate")
    calcite = PaleoProxy("http://linked.earth/ontology/paleo_proxy#calcite", "calcite")
    carbonate = PaleoProxy("http://linked.earth/ontology/paleo_proxy#carbonate", "carbonate")
    cellulose = PaleoProxy("http://linked.earth/ontology/paleo_proxy#cellulose", "cellulose")
    charcoal = PaleoProxy("http://linked.earth/ontology/paleo_proxy#charcoal", "charcoal")
    chironomid = PaleoProxy("http://linked.earth/ontology/paleo_proxy#chironomid", "chironomid")
    chlorophyll = PaleoProxy("http://linked.earth/ontology/paleo_proxy#chlorophyll", "chlorophyll")
    chrysophyte_assemblage = PaleoProxy("http://linked.earth/ontology/paleo_proxy#chrysophyte_assemblage", "chrysophyte assemblage")
    cladoceran = PaleoProxy("http://linked.earth/ontology/paleo_proxy#cladoceran", "cladoceran")
    coccolithophore = PaleoProxy("http://linked.earth/ontology/paleo_proxy#coccolithophore", "coccolithophore")
    d13C = PaleoProxy("http://linked.earth/ontology/paleo_proxy#d13C", "d13C")
    d15N = PaleoProxy("http://linked.earth/ontology/paleo_proxy#d15N", "d15N")
    d15N_d40Ar = PaleoProxy("http://linked.earth/ontology/paleo_proxy#d15N_d40Ar", "d15N/d40Ar")
    d18O = PaleoProxy("http://linked.earth/ontology/paleo_proxy#d18O", "d18O")
    dD = PaleoProxy("http://linked.earth/ontology/paleo_proxy#dD", "dD")
    deuterium_excess = PaleoProxy("http://linked.earth/ontology/paleo_proxy#deuterium_excess", "deuterium excess")
    diatom = PaleoProxy("http://linked.earth/ontology/paleo_proxy#diatom", "diatom")
    dinocyst = PaleoProxy("http://linked.earth/ontology/paleo_proxy#dinocyst", "dinocyst")
    dry_bulk_density = PaleoProxy("http://linked.earth/ontology/paleo_proxy#dry_bulk_density", "dry bulk density")
    Eu_Zr = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Eu_Zr", "Eu/Zr")
    Fe = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Fe", "Fe")
    Fe_Al = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Fe_Al", "Fe/Al")
    foraminifera = PaleoProxy("http://linked.earth/ontology/paleo_proxy#foraminifera", "foraminifera")
    GDGT = PaleoProxy("http://linked.earth/ontology/paleo_proxy#GDGT", "GDGT")
    grain_size = PaleoProxy("http://linked.earth/ontology/paleo_proxy#grain_size", "grain size")
    HBI = PaleoProxy("http://linked.earth/ontology/paleo_proxy#HBI", "HBI")
    historical = PaleoProxy("http://linked.earth/ontology/paleo_proxy#historical", "historical")
    humification = PaleoProxy("http://linked.earth/ontology/paleo_proxy#humification", "humification")
    ice_accumulation = PaleoProxy("http://linked.earth/ontology/paleo_proxy#ice_accumulation", "ice accumulation")
    ice_melt = PaleoProxy("http://linked.earth/ontology/paleo_proxy#ice_melt", "ice melt")
    inorganic_carbon = PaleoProxy("http://linked.earth/ontology/paleo_proxy#inorganic_carbon", "inorganic carbon")
    IP25 = PaleoProxy("http://linked.earth/ontology/paleo_proxy#IP25", "IP25")
    lake_level = PaleoProxy("http://linked.earth/ontology/paleo_proxy#lake_level", "lake level")
    latewood_cellulose = PaleoProxy("http://linked.earth/ontology/paleo_proxy#latewood_cellulose", "latewood cellulose")
    LDI = PaleoProxy("http://linked.earth/ontology/paleo_proxy#LDI", "LDI")
    macrofossils = PaleoProxy("http://linked.earth/ontology/paleo_proxy#macrofossils", "macrofossils")
    magnetic = PaleoProxy("http://linked.earth/ontology/paleo_proxy#magnetic", "magnetic")
    magnetic_susceptibility = PaleoProxy("http://linked.earth/ontology/paleo_proxy#magnetic_susceptibility", "magnetic susceptibility")
    mass_accumulation_rate = PaleoProxy("http://linked.earth/ontology/paleo_proxy#mass_accumulation_rate", "mass accumulation rate")
    maximum_latewood_density = PaleoProxy("http://linked.earth/ontology/paleo_proxy#maximum_latewood_density", "maximum latewood density")
    Mg = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Mg", "Mg")
    Mg_Ca = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Mg_Ca", "Mg/Ca")
    multiproxy = PaleoProxy("http://linked.earth/ontology/paleo_proxy#multiproxy", "multiproxy")
    Ti = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Ti", "Ti")
    needs_to_be_changed = PaleoProxy("http://linked.earth/ontology/paleo_proxy#needs_to_be_changed", "needs to be changed")
    needsToBeChanged = PaleoProxy("http://linked.earth/ontology/paleo_proxy#needsToBeChanged", "needsToBeChanged")
    ostracod = PaleoProxy("http://linked.earth/ontology/paleo_proxy#ostracod", "ostracod")
    P_aqueous = PaleoProxy("http://linked.earth/ontology/paleo_proxy#P-aqueous", "P-aqueous")
    peat_ash = PaleoProxy("http://linked.earth/ontology/paleo_proxy#peat_ash", "peat ash")
    pH = PaleoProxy("http://linked.earth/ontology/paleo_proxy#pH", "pH")
    pollen = PaleoProxy("http://linked.earth/ontology/paleo_proxy#pollen", "pollen")
    radiolaria = PaleoProxy("http://linked.earth/ontology/paleo_proxy#radiolaria", "radiolaria")
    Rb = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Rb", "Rb")
    Rb_Sr = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Rb_Sr", "Rb/Sr")
    reflectance = PaleoProxy("http://linked.earth/ontology/paleo_proxy#reflectance", "reflectance")
    ring_width = PaleoProxy("http://linked.earth/ontology/paleo_proxy#ring_width", "ring width")
    Sr = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Sr", "Sr")
    Sr_Ca = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Sr_Ca", "Sr/Ca")
    stratigraphy = PaleoProxy("http://linked.earth/ontology/paleo_proxy#stratigraphy", "stratigraphy")
    sulfur = PaleoProxy("http://linked.earth/ontology/paleo_proxy#sulfur", "sulfur")
    TEX86 = PaleoProxy("http://linked.earth/ontology/paleo_proxy#TEX86", "TEX86")
    Ti_Al = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Ti_Al", "Ti/Al")
    Ti_Ca = PaleoProxy("http://linked.earth/ontology/paleo_proxy#Ti_Ca", "Ti/Ca")
    TOC = PaleoProxy("http://linked.earth/ontology/paleo_proxy#TOC", "TOC")
    total_nitrogen = PaleoProxy("http://linked.earth/ontology/paleo_proxy#total_nitrogen", "total nitrogen")
    varve_thickness = PaleoProxy("http://linked.earth/ontology/paleo_proxy#varve_thickness", "varve thickness")