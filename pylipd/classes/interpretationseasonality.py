
##############################
# Auto-generated. Do not Edit
##############################
from pylipd.globals.synonyms import SYNONYMS

class InterpretationSeasonality:
    """Controlled-vocabulary class for `InterpretationSeasonality` terms."""
    synonyms = SYNONYMS["INTERPRETATION"]["InterpretationSeasonality"]

    def __init__(self, id, label):
        """Initialize a InterpretationSeasonality term.

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
        """Create a InterpretationSeasonality instance from a synonym string.

        Parameters
        ----------
        synonym : str
            A synonym or alternative name for the term.

        Returns
        -------
        InterpretationSeasonality or None
            The InterpretationSeasonality instance if found, None otherwise.
        """
        if synonym.lower() in InterpretationSeasonality.synonyms:
            synobj = InterpretationSeasonality.synonyms[synonym.lower()]
            return InterpretationSeasonality(synobj['id'], synobj['label'])
        return None
        
class InterpretationSeasonalityConstants:
    Annual = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Annual", "Annual")
    Winter = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Winter", "Winter")
    Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr", "Apr")
    Oct_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-May", "Oct-May")
    Apr_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Aug", "Apr-Aug")
    Apr_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Dec", "Apr-Dec")
    Apr_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Feb", "Apr-Feb")
    Apr_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Jan", "Apr-Jan")
    Apr_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Jul", "Apr-Jul")
    Apr_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Jun", "Apr-Jun")
    Apr_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Mar", "Apr-Mar")
    Apr_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-May", "Apr-May")
    Apr_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Nov", "Apr-Nov")
    Apr_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Oct", "Apr-Oct")
    Apr_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Apr-Sep", "Apr-Sep")
    Summer = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Summer", "Summer")
    Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug", "Aug")
    Aug_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Apr", "Aug-Apr")
    Aug_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Dec", "Aug-Dec")
    Aug_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Feb", "Aug-Feb")
    Aug_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Jan", "Aug-Jan")
    Aug_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Jul", "Aug-Jul")
    Aug_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Jun", "Aug-Jun")
    Aug_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Mar", "Aug-Mar")
    Aug_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-May", "Aug-May")
    Aug_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Nov", "Aug-Nov")
    Aug_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Oct", "Aug-Oct")
    Aug_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Aug-Sep", "Aug-Sep")
    Growing_Season = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Growing_Season", "Growing Season")
    Coldest_Month = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Coldest_Month", "Coldest Month")
    Dec_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Apr", "Dec-Apr")
    Dec_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Aug", "Dec-Aug")
    Dec_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Feb", "Dec-Feb")
    Dec_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Jan", "Dec-Jan")
    Dec_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Jul", "Dec-Jul")
    Dec_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Jun", "Dec-Jun")
    Dec_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Mar", "Dec-Mar")
    Dec_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-May", "Dec-May")
    Dec_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Oct", "Dec-Oct")
    Dec_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Dec-Sep", "Dec-Sep")
    Fall = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Fall", "Fall")
    Feb_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Aug", "Feb-Aug")
    Feb_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Apr", "Feb-Apr")
    Feb_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Dec", "Feb-Dec")
    Feb_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Jul", "Feb-Jul")
    Feb_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Jun", "Feb-Jun")
    Feb_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Mar", "Feb-Mar")
    Feb_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-May", "Feb-May")
    Feb_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Nov", "Feb-Nov")
    Feb_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Oct", "Feb-Oct")
    Feb_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Feb-Sep", "Feb-Sep")
    Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan", "Jan")
    Jan_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Apr", "Jan-Apr")
    Jan_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Aug", "Jan-Aug")
    Jan_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Feb", "Jan-Feb")
    Jan_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Jul", "Jan-Jul")
    Jan_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Jun", "Jan-Jun")
    Jan_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Mar", "Jan-Mar")
    Jan_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-May", "Jan-May")
    Jan_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Nov", "Jan-Nov")
    Jan_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Oct", "Jan-Oct")
    Jan_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jan-Sep", "Jan-Sep")
    Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul", "Jul")
    May_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Sep", "May-Sep")
    Jul_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Apr", "Jul-Apr")
    Jul_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Aug", "Jul-Aug")
    Jul_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Dec", "Jul-Dec")
    Jul_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Feb", "Jul-Feb")
    Jul_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Jan", "Jul-Jan")
    Jul_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Jun", "Jul-Jun")
    Jul_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Mar", "Jul-Mar")
    Jul_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-May", "Jul-May")
    Jul_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Nov", "Jul-Nov")
    Jul_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Oct", "Jul-Oct")
    Jul_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jul-Sep", "Jul-Sep")
    Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun", "Jun")
    Jun_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Apr", "Jun-Apr")
    Jun_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Aug", "Jun-Aug")
    Jun_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Sep", "Jun-Sep")
    Jun_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Dec", "Jun-Dec")
    Jun_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Feb", "Jun-Feb")
    Jun_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Jan", "Jun-Jan")
    Jun_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Jul", "Jun-Jul")
    Jun_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Mar", "Jun-Mar")
    Jun_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Nov", "Jun-Nov")
    Jun_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Jun-Oct", "Jun-Oct")
    Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar", "Mar")
    Mar_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Apr", "Mar-Apr")
    Mar_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Aug", "Mar-Aug")
    Mar_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Dec", "Mar-Dec")
    Mar_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Jan", "Mar-Jan")
    Mar_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Jul", "Mar-Jul")
    Mar_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Jun", "Mar-Jun")
    Mar_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-May", "Mar-May")
    Mar_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Nov", "Mar-Nov")
    Mar_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Oct", "Mar-Oct")
    Mar_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Mar-Sep", "Mar-Sep")
    May_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Apr", "May-Apr")
    May_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Aug", "May-Aug")
    May_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Dec", "May-Dec")
    May_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Oct", "May-Oct")
    May_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Feb", "May-Feb")
    May_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Jan", "May-Jan")
    May_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Jul", "May-Jul")
    May_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Jun", "May-Jun")
    May_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Mar", "May-Mar")
    May_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#May-Nov", "May-Nov")
    needsToBeChanged = InterpretationSeasonality("http://linked.earth/ontology/interpretation#needsToBeChanged", "needsToBeChanged")
    Nov_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Apr", "Nov-Apr")
    Nov_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Aug", "Nov-Aug")
    Nov_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Dec", "Nov-Dec")
    Nov_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Feb", "Nov-Feb")
    Nov_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Jan", "Nov-Jan")
    Nov_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Jul", "Nov-Jul")
    Nov_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Jun", "Nov-Jun")
    Nov_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Mar", "Nov-Mar")
    Nov_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-May", "Nov-May")
    Nov_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Oct", "Nov-Oct")
    Nov_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Nov-Sep", "Nov-Sep")
    Oct_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Apr", "Oct-Apr")
    Oct_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Aug", "Oct-Aug")
    Oct_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Dec", "Oct-Dec")
    Oct_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Feb", "Oct-Feb")
    Oct_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Jan", "Oct-Jan")
    Oct_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Jul", "Oct-Jul")
    Oct_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Jun", "Oct-Jun")
    Oct_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Mar", "Oct-Mar")
    Oct_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Nov", "Oct-Nov")
    Oct_Sep = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Oct-Sep", "Oct-Sep")
    Sep_Apr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Apr", "Sep-Apr")
    Sep_Aug = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Aug", "Sep-Aug")
    Sep_Dec = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Dec", "Sep-Dec")
    Sep_Feb = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Feb", "Sep-Feb")
    Sep_Jan = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Jan", "Sep-Jan")
    Sep_Jul = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Jul", "Sep-Jul")
    Sep_Jun = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Jun", "Sep-Jun")
    Sep_Mar = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Mar", "Sep-Mar")
    Sep_May = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-May", "Sep-May")
    Sep_Nov = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Nov", "Sep-Nov")
    Sep_Oct = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Sep-Oct", "Sep-Oct")
    Spr_Sum = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Spr-Sum", "Spr-Sum")
    Spring = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Spring", "Spring")
    subannual = InterpretationSeasonality("http://linked.earth/ontology/interpretation#subannual", "subannual")
    Warmest_Month = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Warmest_Month", "Warmest Month")
    Wet_Season = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Wet_Season", "Wet Season")
    Win_Spr = InterpretationSeasonality("http://linked.earth/ontology/interpretation#Win-Spr", "Win-Spr")