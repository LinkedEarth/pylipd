
##############################
# Auto-generated. Do not Edit
##############################

from ..globals.synonyms import SYNONYMS

class PaleoProxy:
    synonyms = SYNONYMS["PROXIES"]["PaleoProxy"]

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
        if synonym.lower() in PaleoProxy.synonyms:
            synobj = PaleoProxy.synonyms[synonym.lower()]
            return PaleoProxy(synobj['id'], synobj['label'])
        return None
    
class PaleoProxyConstants:
    accumulation_rate = PaleoProxy("http://linked.earth/ontology/proxy#accumulation_rate", "accumulation rate")
    ACL = PaleoProxy("http://linked.earth/ontology/proxy#ACL", "ACL")
    Al2O3 = PaleoProxy("http://linked.earth/ontology/proxy#Al2O3", "Al2O3")
    alkenone = PaleoProxy("http://linked.earth/ontology/proxy#alkenone", "alkenone")
    amoeba = PaleoProxy("http://linked.earth/ontology/proxy#amoeba", "amoeba")
    Ba_Al = PaleoProxy("http://linked.earth/ontology/proxy#Ba_Al", "Ba/Al")
    Ba_Ca = PaleoProxy("http://linked.earth/ontology/proxy#Ba_Ca", "Ba/Ca")
    biomarker = PaleoProxy("http://linked.earth/ontology/proxy#biomarker", "biomarker")
    BIT = PaleoProxy("http://linked.earth/ontology/proxy#BIT", "BIT")
    borehole = PaleoProxy("http://linked.earth/ontology/proxy#borehole", "borehole")
    BSi = PaleoProxy("http://linked.earth/ontology/proxy#BSi", "BSi")
    bubble_frequency = PaleoProxy("http://linked.earth/ontology/proxy#bubble_frequency", "bubble frequency")
    bulk_density = PaleoProxy("http://linked.earth/ontology/proxy#bulk_density", "bulk density")
    bulk_sediment = PaleoProxy("http://linked.earth/ontology/proxy#bulk_sediment", "bulk sediment")
    C_N = PaleoProxy("http://linked.earth/ontology/proxy#C_N", "C/N")
    Ca_K = PaleoProxy("http://linked.earth/ontology/proxy#Ca_K", "Ca/K")
    Ca_Ti = PaleoProxy("http://linked.earth/ontology/proxy#Ca_Ti", "Ca/Ti")
    CaCO3 = PaleoProxy("http://linked.earth/ontology/proxy#CaCO3", "CaCO3")
    calcification_rate = PaleoProxy("http://linked.earth/ontology/proxy#calcification_rate", "calcification rate")
    calcite = PaleoProxy("http://linked.earth/ontology/proxy#calcite", "calcite")
    carbonate = PaleoProxy("http://linked.earth/ontology/proxy#carbonate", "carbonate")
    cellulose = PaleoProxy("http://linked.earth/ontology/proxy#cellulose", "cellulose")
    charcoal = PaleoProxy("http://linked.earth/ontology/proxy#charcoal", "charcoal")
    chironomid = PaleoProxy("http://linked.earth/ontology/proxy#chironomid", "chironomid")
    chlorophyll = PaleoProxy("http://linked.earth/ontology/proxy#chlorophyll", "chlorophyll")
    chrysophyte_assemblage = PaleoProxy("http://linked.earth/ontology/proxy#chrysophyte_assemblage", "chrysophyte assemblage")
    cladoceran = PaleoProxy("http://linked.earth/ontology/proxy#cladoceran", "cladoceran")
    coccolithophore = PaleoProxy("http://linked.earth/ontology/proxy#coccolithophore", "coccolithophore")
    d13C = PaleoProxy("http://linked.earth/ontology/proxy#d13C", "d13C")
    d15N = PaleoProxy("http://linked.earth/ontology/proxy#d15N", "d15N")
    d15N_d40Ar = PaleoProxy("http://linked.earth/ontology/proxy#d15N_d40Ar", "d15N/d40Ar")
    d18O = PaleoProxy("http://linked.earth/ontology/proxy#d18O", "d18O")
    dD = PaleoProxy("http://linked.earth/ontology/proxy#dD", "dD")
    deuterium_excess = PaleoProxy("http://linked.earth/ontology/proxy#deuterium_excess", "deuterium excess")
    diatom = PaleoProxy("http://linked.earth/ontology/proxy#diatom", "diatom")
    dinocyst = PaleoProxy("http://linked.earth/ontology/proxy#dinocyst", "dinocyst")
    dry_bulk_density = PaleoProxy("http://linked.earth/ontology/proxy#dry_bulk_density", "dry bulk density")
    Eu_Zr = PaleoProxy("http://linked.earth/ontology/proxy#Eu_Zr", "Eu/Zr")
    Fe = PaleoProxy("http://linked.earth/ontology/proxy#Fe", "Fe")
    Fe_Al = PaleoProxy("http://linked.earth/ontology/proxy#Fe_Al", "Fe/Al")
    foraminifera = PaleoProxy("http://linked.earth/ontology/proxy#foraminifera", "foraminifera")
    GDGT = PaleoProxy("http://linked.earth/ontology/proxy#GDGT", "GDGT")
    grain_size = PaleoProxy("http://linked.earth/ontology/proxy#grain_size", "grain size")
    HBI = PaleoProxy("http://linked.earth/ontology/proxy#HBI", "HBI")
    historical = PaleoProxy("http://linked.earth/ontology/proxy#historical", "historical")
    humification = PaleoProxy("http://linked.earth/ontology/proxy#humification", "humification")
    ice_accumulation = PaleoProxy("http://linked.earth/ontology/proxy#ice_accumulation", "ice accumulation")
    ice_melt = PaleoProxy("http://linked.earth/ontology/proxy#ice_melt", "ice melt")
    inorganic_carbon = PaleoProxy("http://linked.earth/ontology/proxy#inorganic_carbon", "inorganic carbon")
    IP25 = PaleoProxy("http://linked.earth/ontology/proxy#IP25", "IP25")
    lake_level = PaleoProxy("http://linked.earth/ontology/proxy#lake_level", "lake level")
    latewood_cellulose = PaleoProxy("http://linked.earth/ontology/proxy#latewood_cellulose", "latewood cellulose")
    LDI = PaleoProxy("http://linked.earth/ontology/proxy#LDI", "LDI")
    macrofossils = PaleoProxy("http://linked.earth/ontology/proxy#macrofossils", "macrofossils")
    magnetic = PaleoProxy("http://linked.earth/ontology/proxy#magnetic", "magnetic")
    magnetic_susceptibility = PaleoProxy("http://linked.earth/ontology/proxy#magnetic_susceptibility", "magnetic susceptibility")
    mass_accumulation_rate = PaleoProxy("http://linked.earth/ontology/proxy#mass_accumulation_rate", "mass accumulation rate")
    maximum_latewood_density = PaleoProxy("http://linked.earth/ontology/proxy#maximum_latewood_density", "maximum latewood density")
    Mg = PaleoProxy("http://linked.earth/ontology/proxy#Mg", "Mg")
    Mg_Ca = PaleoProxy("http://linked.earth/ontology/proxy#Mg_Ca", "Mg/Ca")
    multiproxy = PaleoProxy("http://linked.earth/ontology/proxy#multiproxy", "multiproxy")
    Ti = PaleoProxy("http://linked.earth/ontology/proxy#Ti", "Ti")
    needs_to_be_changed = PaleoProxy("http://linked.earth/ontology/proxy#needs_to_be_changed", "needs to be changed")
    needsToBeChanged = PaleoProxy("http://linked.earth/ontology/proxy#needsToBeChanged", "needsToBeChanged")
    ostracod = PaleoProxy("http://linked.earth/ontology/proxy#ostracod", "ostracod")
    P_aqueous = PaleoProxy("http://linked.earth/ontology/proxy#P-aqueous", "P-aqueous")
    peat_ash = PaleoProxy("http://linked.earth/ontology/proxy#peat_ash", "peat ash")
    pH = PaleoProxy("http://linked.earth/ontology/proxy#pH", "pH")
    pollen = PaleoProxy("http://linked.earth/ontology/proxy#pollen", "pollen")
    radiolaria = PaleoProxy("http://linked.earth/ontology/proxy#radiolaria", "radiolaria")
    Rb = PaleoProxy("http://linked.earth/ontology/proxy#Rb", "Rb")
    Rb_Sr = PaleoProxy("http://linked.earth/ontology/proxy#Rb_Sr", "Rb/Sr")
    reflectance = PaleoProxy("http://linked.earth/ontology/proxy#reflectance", "reflectance")
    ring_width = PaleoProxy("http://linked.earth/ontology/proxy#ring_width", "ring width")
    Sr = PaleoProxy("http://linked.earth/ontology/proxy#Sr", "Sr")
    Sr_Ca = PaleoProxy("http://linked.earth/ontology/proxy#Sr_Ca", "Sr/Ca")
    stratigraphy = PaleoProxy("http://linked.earth/ontology/proxy#stratigraphy", "stratigraphy")
    sulfur = PaleoProxy("http://linked.earth/ontology/proxy#sulfur", "sulfur")
    TEX86 = PaleoProxy("http://linked.earth/ontology/proxy#TEX86", "TEX86")
    Ti_Al = PaleoProxy("http://linked.earth/ontology/proxy#Ti_Al", "Ti/Al")
    Ti_Ca = PaleoProxy("http://linked.earth/ontology/proxy#Ti_Ca", "Ti/Ca")
    TOC = PaleoProxy("http://linked.earth/ontology/proxy#TOC", "TOC")
    total_nitrogen = PaleoProxy("http://linked.earth/ontology/proxy#total_nitrogen", "total nitrogen")
    varve_thickness = PaleoProxy("http://linked.earth/ontology/proxy#varve_thickness", "varve thickness")