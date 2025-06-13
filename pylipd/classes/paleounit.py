
##############################
# Auto-generated. Do not Edit
##############################
from pylipd.globals.synonyms import SYNONYMS

class PaleoUnit:
    """Controlled-vocabulary class for `PaleoUnit` terms."""
    synonyms = SYNONYMS["UNITS"]["PaleoUnit"]

    def __init__(self, id, label):
        """Initialize a PaleoUnit term.

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
        """Create a PaleoUnit instance from a synonym string.

        Parameters
        ----------
        synonym : str
            A synonym or alternative name for the term.

        Returns
        -------
        PaleoUnit or None
            The PaleoUnit instance if found, None otherwise.
        """
        if synonym.lower() in PaleoUnit.synonyms:
            synobj = PaleoUnit.synonyms[synonym.lower()]
            return PaleoUnit(synobj['id'], synobj['label'])
        return None
        
class PaleoUnitConstants:
    atomic_ratio = PaleoUnit("http://linked.earth/ontology/paleo_units#atomic_ratio", "atomic ratio")
    cgs = PaleoUnit("http://linked.earth/ontology/paleo_units#cgs", "cgs")
    cm = PaleoUnit("http://linked.earth/ontology/paleo_units#cm", "cm")
    cm_kyr = PaleoUnit("http://linked.earth/ontology/paleo_units#cm_kyr", "cm/kyr")
    cm_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#cm_yr", "cm/yr")
    cm3 = PaleoUnit("http://linked.earth/ontology/paleo_units#cm3", "cm3")
    count = PaleoUnit("http://linked.earth/ontology/paleo_units#count", "count")
    count_century = PaleoUnit("http://linked.earth/ontology/paleo_units#count_century", "count/century")
    count_cm2 = PaleoUnit("http://linked.earth/ontology/paleo_units#count_cm2", "count/cm2")
    count_cm2_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#count_cm2_yr", "count/cm2/yr")
    count_cm3 = PaleoUnit("http://linked.earth/ontology/paleo_units#count_cm3", "count/cm3")
    count_g = PaleoUnit("http://linked.earth/ontology/paleo_units#count_g", "count/g")
    count_kyr = PaleoUnit("http://linked.earth/ontology/paleo_units#count_kyr", "count/kyr")
    count_mL = PaleoUnit("http://linked.earth/ontology/paleo_units#count_mL", "count/mL")
    count_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#count_yr", "count/yr")
    cps = PaleoUnit("http://linked.earth/ontology/paleo_units#cps", "cps")
    day = PaleoUnit("http://linked.earth/ontology/paleo_units#day", "day")
    degC = PaleoUnit("http://linked.earth/ontology/paleo_units#degC", "degC")
    degree = PaleoUnit("http://linked.earth/ontology/paleo_units#degree", "degree")
    fraction = PaleoUnit("http://linked.earth/ontology/paleo_units#fraction", "fraction")
    g = PaleoUnit("http://linked.earth/ontology/paleo_units#g", "g")
    g_cm_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#g_cm_yr", "g/cm/yr")
    g_cm2 = PaleoUnit("http://linked.earth/ontology/paleo_units#g_cm2", "g/cm2")
    g_cm2_kyr = PaleoUnit("http://linked.earth/ontology/paleo_units#g_cm2_kyr", "g/cm2/kyr")
    g_cm2_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#g_cm2_yr", "g/cm2/yr")
    g_cm3 = PaleoUnit("http://linked.earth/ontology/paleo_units#g_cm3", "g/cm3")
    g_L = PaleoUnit("http://linked.earth/ontology/paleo_units#g_L", "g/L")
    g_m2 = PaleoUnit("http://linked.earth/ontology/paleo_units#g_m2", "g/m2")
    g_m2_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#g_m2_yr", "g/m2/yr")
    grayscale = PaleoUnit("http://linked.earth/ontology/paleo_units#grayscale", "grayscale")
    kg_m2_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#kg_m2_yr", "kg/m2/yr")
    kg_m3 = PaleoUnit("http://linked.earth/ontology/paleo_units#kg_m3", "kg/m3")
    km2 = PaleoUnit("http://linked.earth/ontology/paleo_units#km2", "km2")
    km3 = PaleoUnit("http://linked.earth/ontology/paleo_units#km3", "km3")
    log_mg_L_ = PaleoUnit("http://linked.earth/ontology/paleo_units#log_mg_L_", "log(mg/L)")
    m = PaleoUnit("http://linked.earth/ontology/paleo_units#m", "m")
    m3_kg = PaleoUnit("http://linked.earth/ontology/paleo_units#m3_kg", "m3/kg")
    mg = PaleoUnit("http://linked.earth/ontology/paleo_units#mg", "mg")
    mg_cm2_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#mg_cm2_yr", "mg/cm2/yr")
    mg_g = PaleoUnit("http://linked.earth/ontology/paleo_units#mg_g", "mg/g")
    mg_kg = PaleoUnit("http://linked.earth/ontology/paleo_units#mg_kg", "mg/kg")
    mg_L = PaleoUnit("http://linked.earth/ontology/paleo_units#mg_L", "mg/L")
    mm = PaleoUnit("http://linked.earth/ontology/paleo_units#mm", "mm")
    mm_day = PaleoUnit("http://linked.earth/ontology/paleo_units#mm_day", "mm/day")
    mm_season = PaleoUnit("http://linked.earth/ontology/paleo_units#mm_season", "mm/season")
    mm_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#mm_yr", "mm/yr")
    mmol_mol = PaleoUnit("http://linked.earth/ontology/paleo_units#mmol_mol", "mmol/mol")
    months_year = PaleoUnit("http://linked.earth/ontology/paleo_units#months_year", "months/year")
    needsToBeChanged = PaleoUnit("http://linked.earth/ontology/paleo_units#needsToBeChanged", "needsToBeChanged")
    ng = PaleoUnit("http://linked.earth/ontology/paleo_units#ng", "ng")
    ng_g = PaleoUnit("http://linked.earth/ontology/paleo_units#ng_g", "ng/g")
    peak_area = PaleoUnit("http://linked.earth/ontology/paleo_units#peak_area", "peak area")
    percent = PaleoUnit("http://linked.earth/ontology/paleo_units#percent", "percent")
    permil = PaleoUnit("http://linked.earth/ontology/paleo_units#permil", "permil")
    pH = PaleoUnit("http://linked.earth/ontology/paleo_units#pH", "pH")
    ppb = PaleoUnit("http://linked.earth/ontology/paleo_units#ppb", "ppb")
    ppm = PaleoUnit("http://linked.earth/ontology/paleo_units#ppm", "ppm")
    practical_salinity_unit = PaleoUnit("http://linked.earth/ontology/paleo_units#practical_salinity_unit", "practical salinity unit")
    ratio = PaleoUnit("http://linked.earth/ontology/paleo_units#ratio", "ratio")
    SI = PaleoUnit("http://linked.earth/ontology/paleo_units#SI", "SI")
    ug_cm2_yr = PaleoUnit("http://linked.earth/ontology/paleo_units#ug_cm2_yr", "ug/cm2/yr")
    ug_g = PaleoUnit("http://linked.earth/ontology/paleo_units#ug_g", "ug/g")
    um = PaleoUnit("http://linked.earth/ontology/paleo_units#um", "um")
    umol_mol = PaleoUnit("http://linked.earth/ontology/paleo_units#umol_mol", "umol/mol")
    unitless = PaleoUnit("http://linked.earth/ontology/paleo_units#unitless", "unitless")
    yr_14C_BP = PaleoUnit("http://linked.earth/ontology/paleo_units#yr_14C_BP", "yr 14C BP")
    yr_AD = PaleoUnit("http://linked.earth/ontology/paleo_units#yr_AD", "yr AD")
    yr_b2k = PaleoUnit("http://linked.earth/ontology/paleo_units#yr_b2k", "yr b2k")
    yr_BP = PaleoUnit("http://linked.earth/ontology/paleo_units#yr_BP", "yr BP")
    yr_ka = PaleoUnit("http://linked.earth/ontology/paleo_units#yr_ka", "yr ka")
    z_score = PaleoUnit("http://linked.earth/ontology/paleo_units#z_score", "z score")