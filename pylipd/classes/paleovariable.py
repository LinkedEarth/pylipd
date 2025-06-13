
##############################
# Auto-generated. Do not Edit
##############################
from pylipd.globals.synonyms import SYNONYMS

class PaleoVariable:
    """Controlled-vocabulary class for `PaleoVariable` terms."""
    synonyms = SYNONYMS["VARIABLES"]["PaleoVariable"]

    def __init__(self, id, label):
        """Initialize a PaleoVariable term.

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
        """Create a PaleoVariable instance from a synonym string.

        Parameters
        ----------
        synonym : str
            A synonym or alternative name for the term.

        Returns
        -------
        PaleoVariable or None
            The PaleoVariable instance if found, None otherwise.
        """
        if synonym.lower() in PaleoVariable.synonyms:
            synobj = PaleoVariable.synonyms[synonym.lower()]
            return PaleoVariable(synobj['id'], synobj['label'])
        return None
        
class PaleoVariableConstants:
    ACL = PaleoVariable("http://linked.earth/ontology/paleo_variables#ACL", "ACL")
    AET_PET = PaleoVariable("http://linked.earth/ontology/paleo_variables#AET_PET", "AET/PET")
    ARM_IRM = PaleoVariable("http://linked.earth/ontology/paleo_variables#ARM_IRM", "ARM/IRM")
    ARSTAN = PaleoVariable("http://linked.earth/ontology/paleo_variables#ARSTAN", "ARSTAN")
    Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#Al", "Al")
    Al2O3 = PaleoVariable("http://linked.earth/ontology/paleo_variables#Al2O3", "Al2O3")
    As = PaleoVariable("http://linked.earth/ontology/paleo_variables#As", "As")
    BIT = PaleoVariable("http://linked.earth/ontology/paleo_variables#BIT", "BIT")
    BSi = PaleoVariable("http://linked.earth/ontology/paleo_variables#BSi", "BSi")
    Ba = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ba", "Ba")
    Ba_Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ba_Al", "Ba/Al")
    Ba_Ca = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ba_Ca", "Ba/Ca")
    Be = PaleoVariable("http://linked.earth/ontology/paleo_variables#Be", "Be")
    Br = PaleoVariable("http://linked.earth/ontology/paleo_variables#Br", "Br")
    C20n_alkenoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C20n-alkenoicAcid", "C20n-alkenoicAcid")
    C21n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C21n-alkanoicAcid", "C21n-alkanoicAcid")
    C22n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C22n-alkanoicAcid", "C22n-alkanoicAcid")
    C23n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C23n-alkanoicAcid", "C23n-alkanoicAcid")
    C24n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C24n-alkanoicAcid", "C24n-alkanoicAcid")
    C25_2n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C25_2n-alkanoicAcid", "C25_2n-alkanoicAcid")
    C25n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C25n-alkanoicAcid", "C25n-alkanoicAcid")
    C26n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C26n-alkanoicAcid", "C26n-alkanoicAcid")
    C27n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C27n-alkanoicAcid", "C27n-alkanoicAcid")
    C28n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C28n-alkanoicAcid", "C28n-alkanoicAcid")
    C29n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C29n-alkanoicAcid", "C29n-alkanoicAcid")
    C30n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C30n-alkanoicAcid", "C30n-alkanoicAcid")
    C31n_alkanoicAcid = PaleoVariable("http://linked.earth/ontology/paleo_variables#C31n-alkanoicAcid", "C31n-alkanoicAcid")
    C37Alkenone = PaleoVariable("http://linked.earth/ontology/paleo_variables#C37Alkenone", "C37Alkenone")
    C37_2Alkenone = PaleoVariable("http://linked.earth/ontology/paleo_variables#C37_2Alkenone", "C37:2Alkenone")
    C37_3aAlkenone = PaleoVariable("http://linked.earth/ontology/paleo_variables#C37_3aAlkenone", "C37:3aAlkenone")
    C37_3bAlkenone = PaleoVariable("http://linked.earth/ontology/paleo_variables#C37_3bAlkenone", "C37:3bAlkenone")
    C37_4Alkenone = PaleoVariable("http://linked.earth/ontology/paleo_variables#C37_4Alkenone", "C37:4Alkenone")
    CBT = PaleoVariable("http://linked.earth/ontology/paleo_variables#CBT", "CBT")
    CCA1 = PaleoVariable("http://linked.earth/ontology/paleo_variables#CCA1", "CCA1")
    CCA2 = PaleoVariable("http://linked.earth/ontology/paleo_variables#CCA2", "CCA2")
    CPI = PaleoVariable("http://linked.earth/ontology/paleo_variables#CPI", "CPI")
    C_N = PaleoVariable("http://linked.earth/ontology/paleo_variables#C_N", "C/N")
    Ca = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ca", "Ca")
    CaCO3 = PaleoVariable("http://linked.earth/ontology/paleo_variables#CaCO3", "CaCO3")
    CaO = PaleoVariable("http://linked.earth/ontology/paleo_variables#CaO", "CaO")
    Ca_K = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ca_K", "Ca/K")
    Ca_Sr = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ca_Sr", "Ca/Sr")
    Ca_Ti = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ca_Ti", "Ca/Ti")
    Ti_Ca = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ti_Ca", "Ti/Ca")
    Cd = PaleoVariable("http://linked.earth/ontology/paleo_variables#Cd", "Cd")
    Cd_Mn = PaleoVariable("http://linked.earth/ontology/paleo_variables#Cd_Mn", "Cd/Mn")
    Cl = PaleoVariable("http://linked.earth/ontology/paleo_variables#Cl", "Cl")
    Co = PaleoVariable("http://linked.earth/ontology/paleo_variables#Co", "Co")
    Cr = PaleoVariable("http://linked.earth/ontology/paleo_variables#Cr", "Cr")
    Cu = PaleoVariable("http://linked.earth/ontology/paleo_variables#Cu", "Cu")
    DWHI = PaleoVariable("http://linked.earth/ontology/paleo_variables#DWHI", "DWHI")
    Dd2H = PaleoVariable("http://linked.earth/ontology/paleo_variables#Dd2H", "Dd2H")
    EPS = PaleoVariable("http://linked.earth/ontology/paleo_variables#EPS", "EPS")
    ElNinoEvent = PaleoVariable("http://linked.earth/ontology/paleo_variables#ElNinoEvent", "ElNinoEvent")
    Eu_Zr = PaleoVariable("http://linked.earth/ontology/paleo_variables#Eu_Zr", "Eu/Zr")
    Fe = PaleoVariable("http://linked.earth/ontology/paleo_variables#Fe", "Fe")
    Fe2O3 = PaleoVariable("http://linked.earth/ontology/paleo_variables#Fe2O3", "Fe2O3")
    Fe_Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#Fe_Al", "Fe/Al")
    Fe_Ca = PaleoVariable("http://linked.earth/ontology/paleo_variables#Fe_Ca", "Fe/Ca")
    Fe_K = PaleoVariable("http://linked.earth/ontology/paleo_variables#Fe_K", "Fe/K")
    Fe_Mn = PaleoVariable("http://linked.earth/ontology/paleo_variables#Fe_Mn", "Fe/Mn")
    GDGT = PaleoVariable("http://linked.earth/ontology/paleo_variables#GDGT", "GDGT")
    GDGT_0_Cren = PaleoVariable("http://linked.earth/ontology/paleo_variables#GDGT-0_Cren", "GDGT-0/Cren")
    IP25 = PaleoVariable("http://linked.earth/ontology/paleo_variables#IP25", "IP25")
    IRM = PaleoVariable("http://linked.earth/ontology/paleo_variables#IRM", "IRM")
    ITCZ = PaleoVariable("http://linked.earth/ontology/paleo_variables#ITCZ", "ITCZ")
    JulianDay = PaleoVariable("http://linked.earth/ontology/paleo_variables#JulianDay", "JulianDay")
    K2O = PaleoVariable("http://linked.earth/ontology/paleo_variables#K2O", "K2O")
    K37 = PaleoVariable("http://linked.earth/ontology/paleo_variables#K37", "K37")
    K_Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#K_Al", "K/Al")
    LDI = PaleoVariable("http://linked.earth/ontology/paleo_variables#LDI", "LDI")
    LOI = PaleoVariable("http://linked.earth/ontology/paleo_variables#LOI", "LOI")
    La = PaleoVariable("http://linked.earth/ontology/paleo_variables#La", "La")
    MAR = PaleoVariable("http://linked.earth/ontology/paleo_variables#MAR", "MAR")
    MBT = PaleoVariable("http://linked.earth/ontology/paleo_variables#MBT", "MBT")
    MS = PaleoVariable("http://linked.earth/ontology/paleo_variables#MS", "MS")
    Si = PaleoVariable("http://linked.earth/ontology/paleo_variables#Si", "Si")
    MXD = PaleoVariable("http://linked.earth/ontology/paleo_variables#MXD", "MXD")
    Mg = PaleoVariable("http://linked.earth/ontology/paleo_variables#Mg", "Mg")
    MgO = PaleoVariable("http://linked.earth/ontology/paleo_variables#MgO", "MgO")
    Mg_Ca = PaleoVariable("http://linked.earth/ontology/paleo_variables#Mg_Ca", "Mg/Ca")
    Mn = PaleoVariable("http://linked.earth/ontology/paleo_variables#Mn", "Mn")
    MnO = PaleoVariable("http://linked.earth/ontology/paleo_variables#MnO", "MnO")
    Mn_Fe = PaleoVariable("http://linked.earth/ontology/paleo_variables#Mn_Fe", "Mn/Fe")
    Mn_Mo = PaleoVariable("http://linked.earth/ontology/paleo_variables#Mn_Mo", "Mn/Mo")
    Mo = PaleoVariable("http://linked.earth/ontology/paleo_variables#Mo", "Mo")
    NO3 = PaleoVariable("http://linked.earth/ontology/paleo_variables#NO3", "NO3")
    nitrate = PaleoVariable("http://linked.earth/ontology/paleo_variables#nitrate", "nitrate")
    N_C = PaleoVariable("http://linked.earth/ontology/paleo_variables#N_C", "N/C")
    Na2O = PaleoVariable("http://linked.earth/ontology/paleo_variables#Na2O", "Na2O")
    Ni = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ni", "Ni")
    PC1 = PaleoVariable("http://linked.earth/ontology/paleo_variables#PC1", "PC1")
    PC3 = PaleoVariable("http://linked.earth/ontology/paleo_variables#PC3", "PC3")
    PC2 = PaleoVariable("http://linked.earth/ontology/paleo_variables#PC2", "PC2")
    Paq = PaleoVariable("http://linked.earth/ontology/paleo_variables#Paq", "Paq")
    Pb = PaleoVariable("http://linked.earth/ontology/paleo_variables#Pb", "Pb")
    Picea_Artemisia = PaleoVariable("http://linked.earth/ontology/paleo_variables#Picea_Artemisia", "Picea/Artemisia")
    Picea_Pinus = PaleoVariable("http://linked.earth/ontology/paleo_variables#Picea_Pinus", "Picea/Pinus")
    Pinus_Artemisia = PaleoVariable("http://linked.earth/ontology/paleo_variables#Pinus_Artemisia", "Pinus/Artemisia")
    Poaceae_Ephedra = PaleoVariable("http://linked.earth/ontology/paleo_variables#Poaceae_Ephedra", "Poaceae/Ephedra")
    R570_R630 = PaleoVariable("http://linked.earth/ontology/paleo_variables#R570_R630", "R570/R630")
    R650_R700 = PaleoVariable("http://linked.earth/ontology/paleo_variables#R650_R700", "R650/R700")
    RABD660670 = PaleoVariable("http://linked.earth/ontology/paleo_variables#RABD660670", "RABD660670")
    RAN15 = PaleoVariable("http://linked.earth/ontology/paleo_variables#RAN15", "RAN15")
    RBAR = PaleoVariable("http://linked.earth/ontology/paleo_variables#RBAR", "RBAR")
    Rb = PaleoVariable("http://linked.earth/ontology/paleo_variables#Rb", "Rb")
    Rb87_Sr86 = PaleoVariable("http://linked.earth/ontology/paleo_variables#Rb87_Sr86", "Rb87/Sr86")
    SO4 = PaleoVariable("http://linked.earth/ontology/paleo_variables#SO4", "SO4")
    sulfate = PaleoVariable("http://linked.earth/ontology/paleo_variables#sulfate", "sulfate")
    salinity = PaleoVariable("http://linked.earth/ontology/paleo_variables#salinity", "salinity")
    Sc = PaleoVariable("http://linked.earth/ontology/paleo_variables#Sc", "Sc")
    Si_Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#Si_Al", "Si/Al")
    Si_Ti = PaleoVariable("http://linked.earth/ontology/paleo_variables#Si_Ti", "Si/Ti")
    Sr = PaleoVariable("http://linked.earth/ontology/paleo_variables#Sr", "Sr")
    Sr_Ca = PaleoVariable("http://linked.earth/ontology/paleo_variables#Sr_Ca", "Sr/Ca")
    TDS = PaleoVariable("http://linked.earth/ontology/paleo_variables#TDS", "TDS")
    TEX86 = PaleoVariable("http://linked.earth/ontology/paleo_variables#TEX86", "TEX86")
    TIC = PaleoVariable("http://linked.earth/ontology/paleo_variables#TIC", "TIC")
    TOC = PaleoVariable("http://linked.earth/ontology/paleo_variables#TOC", "TOC")
    organicCarbon = PaleoVariable("http://linked.earth/ontology/paleo_variables#organicCarbon", "organicCarbon")
    TOC_TN = PaleoVariable("http://linked.earth/ontology/paleo_variables#TOC_TN", "TOC/TN")
    Ti = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ti", "Ti")
    TiO2 = PaleoVariable("http://linked.earth/ontology/paleo_variables#TiO2", "TiO2")
    Ti_Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#Ti_Al", "Ti/Al")
    Uk37 = PaleoVariable("http://linked.earth/ontology/paleo_variables#Uk37", "Uk37")
    UK37 = PaleoVariable("http://linked.earth/ontology/paleo_variables#UK37", "UK37")
    Uk37_ = PaleoVariable("http://linked.earth/ontology/paleo_variables#Uk37_", "Uk37’")
    V = PaleoVariable("http://linked.earth/ontology/paleo_variables#V", "V")
    V_Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#V_Al", "V/Al")
    Y = PaleoVariable("http://linked.earth/ontology/paleo_variables#Y", "Y")
    Zn = PaleoVariable("http://linked.earth/ontology/paleo_variables#Zn", "Zn")
    Zr = PaleoVariable("http://linked.earth/ontology/paleo_variables#Zr", "Zr")
    Zr_Al = PaleoVariable("http://linked.earth/ontology/paleo_variables#Zr_Al", "Zr/Al")
    accumulation = PaleoVariable("http://linked.earth/ontology/paleo_variables#accumulation", "accumulation")
    age = PaleoVariable("http://linked.earth/ontology/paleo_variables#age", "age")
    age14C = PaleoVariable("http://linked.earth/ontology/paleo_variables#age14C", "age14C")
    ammonium = PaleoVariable("http://linked.earth/ontology/paleo_variables#ammonium", "ammonium")
    amps = PaleoVariable("http://linked.earth/ontology/paleo_variables#amps", "amps")
    aragonite = PaleoVariable("http://linked.earth/ontology/paleo_variables#aragonite", "aragonite")
    ash = PaleoVariable("http://linked.earth/ontology/paleo_variables#ash", "ash")
    boron = PaleoVariable("http://linked.earth/ontology/paleo_variables#boron", "boron")
    brGDGT_IIIa = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIIa", "brGDGT-IIIa")
    brGDGT_Id = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-Id", "brGDGT-Id")
    brGDGT_IIIa_ = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIIa_", "brGDGT-IIIa’")
    brGDGT_IIIb = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIIb", "brGDGT-IIIb")
    brGDGT_IIIb_ = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIIb_", "brGDGT-IIIb’")
    brGDGT_IIIc = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIIc", "brGDGT-IIIc")
    brGDGT_IIIc_ = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIIc_", "brGDGT-IIIc’")
    brGDGT_IIa = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIa", "brGDGT-IIa")
    brGDGT_IIa_ = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIa_", "brGDGT-IIa’")
    brGDGT_IIb = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIb", "brGDGT-IIb")
    brGDGT_IIb_ = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIb_", "brGDGT-IIb’")
    brGDGT_IIc = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIc", "brGDGT-IIc")
    brGDGT_IIc_ = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-IIc_", "brGDGT-IIc’")
    brGDGT_Ia = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-Ia", "brGDGT-Ia")
    brGDGT_Ib = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-Ib", "brGDGT-Ib")
    brGDGT_Ic = PaleoVariable("http://linked.earth/ontology/paleo_variables#brGDGT-Ic", "brGDGT-Ic")
    sampleID = PaleoVariable("http://linked.earth/ontology/paleo_variables#sampleID", "sampleID")
    bubbleNumberDensity = PaleoVariable("http://linked.earth/ontology/paleo_variables#bubbleNumberDensity", "bubbleNumberDensity")
    bulkDensity = PaleoVariable("http://linked.earth/ontology/paleo_variables#bulkDensity", "bulkDensity")
    calcificationRate = PaleoVariable("http://linked.earth/ontology/paleo_variables#calcificationRate", "calcificationRate")
    calcite = PaleoVariable("http://linked.earth/ontology/paleo_variables#calcite", "calcite")
    carbon = PaleoVariable("http://linked.earth/ontology/paleo_variables#carbon", "carbon")
    carbonate = PaleoVariable("http://linked.earth/ontology/paleo_variables#carbonate", "carbonate")
    charcoal = PaleoVariable("http://linked.earth/ontology/paleo_variables#charcoal", "charcoal")
    chloride = PaleoVariable("http://linked.earth/ontology/paleo_variables#chloride", "chloride")
    circulationIndex = PaleoVariable("http://linked.earth/ontology/paleo_variables#circulationIndex", "circulationIndex")
    clay = PaleoVariable("http://linked.earth/ontology/paleo_variables#clay", "clay")
    cluster = PaleoVariable("http://linked.earth/ontology/paleo_variables#cluster", "cluster")
    index = PaleoVariable("http://linked.earth/ontology/paleo_variables#index", "index")
    composite = PaleoVariable("http://linked.earth/ontology/paleo_variables#composite", "composite")
    concentration = PaleoVariable("http://linked.earth/ontology/paleo_variables#concentration", "concentration")
    core = PaleoVariable("http://linked.earth/ontology/paleo_variables#core", "core")
    correction = PaleoVariable("http://linked.earth/ontology/paleo_variables#correction", "correction")
    correlationCoefficient = PaleoVariable("http://linked.earth/ontology/paleo_variables#correlationCoefficient", "correlationCoefficient")
    sampleCount = PaleoVariable("http://linked.earth/ontology/paleo_variables#sampleCount", "sampleCount")
    count = PaleoVariable("http://linked.earth/ontology/paleo_variables#count", "count")
    d13C = PaleoVariable("http://linked.earth/ontology/paleo_variables#d13C", "d13C")
    d15N = PaleoVariable("http://linked.earth/ontology/paleo_variables#d15N", "d15N")
    d18O = PaleoVariable("http://linked.earth/ontology/paleo_variables#d18O", "d18O")
    d2H = PaleoVariable("http://linked.earth/ontology/paleo_variables#d2H", "d2H")
    d2HUncertaintyHigh80 = PaleoVariable("http://linked.earth/ontology/paleo_variables#d2HUncertaintyHigh80", "d2HUncertaintyHigh80")
    d2HUncertaintyLow80 = PaleoVariable("http://linked.earth/ontology/paleo_variables#d2HUncertaintyLow80", "d2HUncertaintyLow80")
    deleteMe = PaleoVariable("http://linked.earth/ontology/paleo_variables#deleteMe", "deleteMe")
    needsToBeChanged = PaleoVariable("http://linked.earth/ontology/paleo_variables#needsToBeChanged", "needsToBeChanged")
    deltaRelativeHumidity = PaleoVariable("http://linked.earth/ontology/paleo_variables#deltaRelativeHumidity", "deltaRelativeHumidity")
    deltaTemperature = PaleoVariable("http://linked.earth/ontology/paleo_variables#deltaTemperature", "deltaTemperature")
    density = PaleoVariable("http://linked.earth/ontology/paleo_variables#density", "density")
    depth = PaleoVariable("http://linked.earth/ontology/paleo_variables#depth", "depth")
    depthBottom = PaleoVariable("http://linked.earth/ontology/paleo_variables#depthBottom", "depthBottom")
    depthTop = PaleoVariable("http://linked.earth/ontology/paleo_variables#depthTop", "depthTop")
    deuteriumExcess = PaleoVariable("http://linked.earth/ontology/paleo_variables#deuteriumExcess", "deuteriumExcess")
    diatom = PaleoVariable("http://linked.earth/ontology/paleo_variables#diatom", "diatom")
    diatomCount = PaleoVariable("http://linked.earth/ontology/paleo_variables#diatomCount", "diatomCount")
    dinocyst = PaleoVariable("http://linked.earth/ontology/paleo_variables#dinocyst", "dinocyst")
    dolomite = PaleoVariable("http://linked.earth/ontology/paleo_variables#dolomite", "dolomite")
    dryBulkDensity = PaleoVariable("http://linked.earth/ontology/paleo_variables#dryBulkDensity", "dryBulkDensity")
    duration = PaleoVariable("http://linked.earth/ontology/paleo_variables#duration", "duration")
    dust = PaleoVariable("http://linked.earth/ontology/paleo_variables#dust", "dust")
    effectivePrecipitation = PaleoVariable("http://linked.earth/ontology/paleo_variables#effectivePrecipitation", "effectivePrecipitation")
    elevation = PaleoVariable("http://linked.earth/ontology/paleo_variables#elevation", "elevation")
    zscore = PaleoVariable("http://linked.earth/ontology/paleo_variables#zscore", "zscore")
    epsilonC28C22 = PaleoVariable("http://linked.earth/ontology/paleo_variables#epsilonC28C22", "epsilonC28C22")
    epsilonC28C24 = PaleoVariable("http://linked.earth/ontology/paleo_variables#epsilonC28C24", "epsilonC28C24")
    epsilonC29C23 = PaleoVariable("http://linked.earth/ontology/paleo_variables#epsilonC29C23", "epsilonC29C23")
    equilibriumLineAltitude = PaleoVariable("http://linked.earth/ontology/paleo_variables#equilibriumLineAltitude", "equilibriumLineAltitude")
    event = PaleoVariable("http://linked.earth/ontology/paleo_variables#event", "event")
    eventLayer = PaleoVariable("http://linked.earth/ontology/paleo_variables#eventLayer", "eventLayer")
    facies = PaleoVariable("http://linked.earth/ontology/paleo_variables#facies", "facies")
    feldspar = PaleoVariable("http://linked.earth/ontology/paleo_variables#feldspar", "feldspar")
    flood = PaleoVariable("http://linked.earth/ontology/paleo_variables#flood", "flood")
    fluorine = PaleoVariable("http://linked.earth/ontology/paleo_variables#fluorine", "fluorine")
    foraminifera = PaleoVariable("http://linked.earth/ontology/paleo_variables#foraminifera", "foraminifera")
    gamma = PaleoVariable("http://linked.earth/ontology/paleo_variables#gamma", "gamma")
    glacierCoverage = PaleoVariable("http://linked.earth/ontology/paleo_variables#glacierCoverage", "glacierCoverage")
    globigerinoidesRuber = PaleoVariable("http://linked.earth/ontology/paleo_variables#globigerinoidesRuber", "globigerinoidesRuber")
    grainSize = PaleoVariable("http://linked.earth/ontology/paleo_variables#grainSize", "grainSize")
    lithics = PaleoVariable("http://linked.earth/ontology/paleo_variables#lithics", "lithics")
    grayscale = PaleoVariable("http://linked.earth/ontology/paleo_variables#grayscale", "grayscale")
    growing_degree_days = PaleoVariable("http://linked.earth/ontology/paleo_variables#growing_degree_days", "growing degree days")
    growthRate = PaleoVariable("http://linked.earth/ontology/paleo_variables#growthRate", "growthRate")
    hasGap = PaleoVariable("http://linked.earth/ontology/paleo_variables#hasGap", "hasGap")
    hasHiatus = PaleoVariable("http://linked.earth/ontology/paleo_variables#hasHiatus", "hasHiatus")
    hole = PaleoVariable("http://linked.earth/ontology/paleo_variables#hole", "hole")
    humidificationIndex = PaleoVariable("http://linked.earth/ontology/paleo_variables#humidificationIndex", "humidificationIndex")
    iceMelt = PaleoVariable("http://linked.earth/ontology/paleo_variables#iceMelt", "iceMelt")
    iceRaftedDebris = PaleoVariable("http://linked.earth/ontology/paleo_variables#iceRaftedDebris", "iceRaftedDebris")
    inc_coh = PaleoVariable("http://linked.earth/ontology/paleo_variables#inc_coh", "inc/coh")
    isReliable = PaleoVariable("http://linked.earth/ontology/paleo_variables#isReliable", "isReliable")
    lakeArea = PaleoVariable("http://linked.earth/ontology/paleo_variables#lakeArea", "lakeArea")
    lakeLevel = PaleoVariable("http://linked.earth/ontology/paleo_variables#lakeLevel", "lakeLevel")
    lakeTrend = PaleoVariable("http://linked.earth/ontology/paleo_variables#lakeTrend", "lakeTrend")
    lakeVolume = PaleoVariable("http://linked.earth/ontology/paleo_variables#lakeVolume", "lakeVolume")
    landscapeCover = PaleoVariable("http://linked.earth/ontology/paleo_variables#landscapeCover", "landscapeCover")
    percent = PaleoVariable("http://linked.earth/ontology/paleo_variables#percent", "percent")
    latitude = PaleoVariable("http://linked.earth/ontology/paleo_variables#latitude", "latitude")
    layerThickness = PaleoVariable("http://linked.earth/ontology/paleo_variables#layerThickness", "layerThickness")
    longitude = PaleoVariable("http://linked.earth/ontology/paleo_variables#longitude", "longitude")
    material = PaleoVariable("http://linked.earth/ontology/paleo_variables#material", "material")
    mineralogy = PaleoVariable("http://linked.earth/ontology/paleo_variables#mineralogy", "mineralogy")
    sulfur = PaleoVariable("http://linked.earth/ontology/paleo_variables#sulfur", "sulfur")
    needsToBeSplitIntoMultipleColumns = PaleoVariable("http://linked.earth/ontology/paleo_variables#needsToBeSplitIntoMultipleColumns", "needsToBeSplitIntoMultipleColumns")
    nitrogen = PaleoVariable("http://linked.earth/ontology/paleo_variables#nitrogen", "nitrogen")
    notes = PaleoVariable("http://linked.earth/ontology/paleo_variables#notes", "notes")
    organicMatter = PaleoVariable("http://linked.earth/ontology/paleo_variables#organicMatter", "organicMatter")
    organicNitrogen = PaleoVariable("http://linked.earth/ontology/paleo_variables#organicNitrogen", "organicNitrogen")
    oxygen = PaleoVariable("http://linked.earth/ontology/paleo_variables#oxygen", "oxygen")
    pH = PaleoVariable("http://linked.earth/ontology/paleo_variables#pH", "pH")
    peat = PaleoVariable("http://linked.earth/ontology/paleo_variables#peat", "peat")
    phosphorus = PaleoVariable("http://linked.earth/ontology/paleo_variables#phosphorus", "phosphorus")
    potassium = PaleoVariable("http://linked.earth/ontology/paleo_variables#potassium", "potassium")
    precipitation = PaleoVariable("http://linked.earth/ontology/paleo_variables#precipitation", "precipitation")
    productivity = PaleoVariable("http://linked.earth/ontology/paleo_variables#productivity", "productivity")
    pyrite = PaleoVariable("http://linked.earth/ontology/paleo_variables#pyrite", "pyrite")
    quartz = PaleoVariable("http://linked.earth/ontology/paleo_variables#quartz", "quartz")
    reflectance = PaleoVariable("http://linked.earth/ontology/paleo_variables#reflectance", "reflectance")
    relativeHumidity = PaleoVariable("http://linked.earth/ontology/paleo_variables#relativeHumidity", "relativeHumidity")
    residualChronology = PaleoVariable("http://linked.earth/ontology/paleo_variables#residualChronology", "residualChronology")
    ringWidth = PaleoVariable("http://linked.earth/ontology/paleo_variables#ringWidth", "ringWidth")
    sand = PaleoVariable("http://linked.earth/ontology/paleo_variables#sand", "sand")
    seaIce = PaleoVariable("http://linked.earth/ontology/paleo_variables#seaIce", "seaIce")
    section = PaleoVariable("http://linked.earth/ontology/paleo_variables#section", "section")
    sedimentDry = PaleoVariable("http://linked.earth/ontology/paleo_variables#sedimentDry", "sedimentDry")
    sedimentationRate = PaleoVariable("http://linked.earth/ontology/paleo_variables#sedimentationRate", "sedimentationRate")
    segmentLength = PaleoVariable("http://linked.earth/ontology/paleo_variables#segmentLength", "segmentLength")
    sequence = PaleoVariable("http://linked.earth/ontology/paleo_variables#sequence", "sequence")
    silt = PaleoVariable("http://linked.earth/ontology/paleo_variables#silt", "silt")
    site = PaleoVariable("http://linked.earth/ontology/paleo_variables#site", "site")
    siteCount = PaleoVariable("http://linked.earth/ontology/paleo_variables#siteCount", "siteCount")
    sodium = PaleoVariable("http://linked.earth/ontology/paleo_variables#sodium", "sodium")
    solarIrradiance = PaleoVariable("http://linked.earth/ontology/paleo_variables#solarIrradiance", "solarIrradiance")
    streamflow = PaleoVariable("http://linked.earth/ontology/paleo_variables#streamflow", "streamflow")
    temperature = PaleoVariable("http://linked.earth/ontology/paleo_variables#temperature", "temperature")
    thickness = PaleoVariable("http://linked.earth/ontology/paleo_variables#thickness", "thickness")
    totalCarbon = PaleoVariable("http://linked.earth/ontology/paleo_variables#totalCarbon", "totalCarbon")
    totalNitrogen = PaleoVariable("http://linked.earth/ontology/paleo_variables#totalNitrogen", "totalNitrogen")
    totalPollen = PaleoVariable("http://linked.earth/ontology/paleo_variables#totalPollen", "totalPollen")
    treeCover = PaleoVariable("http://linked.earth/ontology/paleo_variables#treeCover", "treeCover")
    uncertainty = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertainty", "uncertainty")
    uncertainty1s = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertainty1s", "uncertainty1s")
    uncertainty2s = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertainty2s", "uncertainty2s")
    uncertaintyHigh = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyHigh", "uncertaintyHigh")
    uncertaintyHigh1s = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyHigh1s", "uncertaintyHigh1s")
    uncertaintyLow95 = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyLow95", "uncertaintyLow95")
    uncertaintyHigh50 = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyHigh50", "uncertaintyHigh50")
    uncertaintyHigh90 = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyHigh90", "uncertaintyHigh90")
    uncertaintyHigh95 = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyHigh95", "uncertaintyHigh95")
    uncertaintyLow = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyLow", "uncertaintyLow")
    uncertaintyLow1s = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyLow1s", "uncertaintyLow1s")
    uncertaintyLow90 = PaleoVariable("http://linked.earth/ontology/paleo_variables#uncertaintyLow90", "uncertaintyLow90")
    upwelling = PaleoVariable("http://linked.earth/ontology/paleo_variables#upwelling", "upwelling")
    uranium = PaleoVariable("http://linked.earth/ontology/paleo_variables#uranium", "uranium")
    varveThickness = PaleoVariable("http://linked.earth/ontology/paleo_variables#varveThickness", "varveThickness")
    volume = PaleoVariable("http://linked.earth/ontology/paleo_variables#volume", "volume")
    waterContent = PaleoVariable("http://linked.earth/ontology/paleo_variables#waterContent", "waterContent")
    waterTableDepth = PaleoVariable("http://linked.earth/ontology/paleo_variables#waterTableDepth", "waterTableDepth")
    wetBulkDensity = PaleoVariable("http://linked.earth/ontology/paleo_variables#wetBulkDensity", "wetBulkDensity")
    year = PaleoVariable("http://linked.earth/ontology/paleo_variables#year", "year")