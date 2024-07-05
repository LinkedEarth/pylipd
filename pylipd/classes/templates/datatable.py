import pandas as pd
import json

### START TEMPLATE FUNCTION ###
# Special Functions manually added for DataTable class
def getDataFrame(self, use_standard_names=False) -> pd.DataFrame:
    cols = []
    for v in self.variables:
        colname = v.getName()
        if use_standard_names and v.getStandardVariable() is not None:
            colname = v.getStandardVariable().getLabel()
        cols.append(colname)
    
    df = pd.DataFrame(columns=cols)
    for v in self.variables:
        colname = v.getName()
        if use_standard_names and v.getStandardVariable() is not None:
            colname = v.getStandardVariable().getLabel()
        df[colname] = json.loads(v.getValues())
    
    # Create metadata as a dictionary and add to dataframe attr
    df.attrs = {}
    for v in self.variables:
        colname = v.getName()
        if use_standard_names and v.getStandardVariable() is not None:
            colname = v.getStandardVariable().getLabel()
        df.attrs[colname] = v.to_json()
        del df.attrs[colname]["hasValues"]

    return df
### END TEMPLATE FUNCTION ###


### START TEMPLATE FUNCTION ###
def setDataFrame(self, df: pd.DataFrame):
    # Need to delete all existing variables
    # Create new set of variable objects using the metadata
    pass
### END TEMPLATE FUNCTION ###