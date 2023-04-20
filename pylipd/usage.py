from pylipd.lipd import LiPD
import json
from pylipd.lipd_series import LiPDSeries
from pylipd.multi_processing import convert_to_rdf

####################
# TODO:
# - Edit local LiPD & update endpoint
####################


local_lipd_dir = "/Users/varun/git/LiPD/PyLiPD/data/lpd.latest"
remote_lipd_endpoint = "https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2"

'''
lipd = LiPD()
# Convert LiPD files to RDF    
lipd.convert_lipd_dir_to_rdf(
    local_lipd_dir,
    local_lipd_dir+".nq", 
    parallel=False)

exit()
'''

'''
# Convert one LiPD file to RDF
convert_to_rdf(
    "/Users/varun/git/LiPD/PyLiPD/data/lpd/CO03COPM.lpd",
    "/Users/varun/git/LiPD/PyLiPD/data/MD98_2181.Stott.2007.nq"
)
exit()
'''

'''    
data = ['https://lipdverse.org/data/TjhHrDv0LQ4aazHolZkR/1_0_0//Ocn-WEqPacific.Stott.2007.lpd']
lipd.load(data)

ts_list = lipd.get_timeseries(lipd.get_all_dataset_names())
for dsname, tsos in ts_list.items():
    for tso in tsos:
        if 'paleoData_variableName' in tso:
            print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])    

'''

# Load Datasets (from Local and Remote)
dsnames = ["MD98_2181.Stott.2007"]
remote_dsnames = ["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001"]

'''
L = LiPD()

#L.load(local_lipd_dir+"/"+"ODP1671017E.lpd")
#L.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")    
L.load([local_lipd_dir + "/" + dsname + ".lpd" for dsname in ["MD98_2181.Stott.2007","NAm-SmithersSkiArea.Schweingruber.1996", 
                        "NAm-CeaderBreaks.Briffa.1996", "ODP1671017E", 
                        "SPC14.Kahle.2021", "RC12-10.Poore.2003", 
                        "MD02-2553.Poore.2009", "AD9117.Guinta.2001", "SP10BEIN",
                        "SchellingsBog.Barron.2004", "Hidden.Tang.1999"]])
#bibtex = L.get_bibtex()
#print(bibtex)
#exit()

S = LiPDSeries()
S.load(L)

print(S)

exit()
'''

# Load from local
lipd = LiPD()
data_path = local_lipd_dir + '/Ocn-Palmyra.Nurhati.2011.lpd'
lipd.load(data_path)
print(lipd.get_all_dataset_names())

#lipdfiles = [local_lipd_dir + "/" + dsname + ".lpd" for dsname in dsnames]
#print(lipdfiles)

#lipd.load(lipdfiles)
lipd.load_from_dir("examples/data")
print(lipd.get_all_dataset_names())

lat = -77.08
lon = 38.91
radius = 50

(result, result_df) = lipd.query("""
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT ?what
WHERE {
  ?ds wgs84:lat ?lat .
  ?ds wgs84:lon ?lon .
  
  FILTER(geof:sfWithin(?geometry,
     "POLYGON((-77.089005 38.913574,-77.029953 38.913574,-77.029953 38.886321,-77.089005 38.886321,-77.089005 38.913574))"^^geo:wktLiteral))
}
""")

#print(lipd.get_all_dataset_ids())
ens_df = lipd.get_ensemble_tables(
    ensembleVarName="age",
    ensembleDepthVarName="depth"
)
print(ens_df)


#lipd.load(["/Users/varun/Downloads/Arc-LakeNataujärvi.Ojala.2005.lpd"])
#print(lipd.get_all_dataset_names())

ts_list = lipd.get_timeseries(lipd.get_all_dataset_names())
for dsname, tsos in ts_list.items():
    for tso in tsos:
        if 'paleoData_variableName' in tso:
            print(dsname+': '+str(tso['paleoData_variableName'])+': '+tso['archiveType'])


# Fetch LiPD data from remote RDF Graph
#lipd.set_endpoint(remote_lipd_endpoint)
#lipd.load_remote_datasets(remote_dsnames)

# Convert to TSO object (as before)
'''
ts_list_remote = lipd.get_timeseries(lipd.get_all_dataset_names())
for dsname, tsos in ts_list_remote.items():
    for tso in tsos:
        print(dsname+': '+str(tso['paleoData_variableName'])+': '+tso['archiveType'])
'''

print("Popping ...")
poplipd = lipd.pop(lipd.get_all_dataset_names())
print(lipd.get_all_dataset_names())
print(poplipd.get_all_dataset_names())

print("Creating separate lipd file for popped")
dsname = poplipd.get_all_dataset_names()[0]
lipdfile = f"{dsname}.lpd"
poplipd.create_lipd(dsname, lipdfile)

print("Loading .. created lipd file: "+lipdfile)
lpd2 = LiPD()
lpd2.load([lipdfile])
ts_list_remote = lpd2.get_timeseries(lpd2.get_all_dataset_names())
for dsname, tsos in ts_list_remote.items():
    for tso in tsos:
        print(dsname+': '+str(tso['paleoData_variableName'])+': '+tso['archiveType'])

ens_df2 = lpd2.get_ensemble_tables(
    ensembleVarName="age",
    ensembleDepthVarName="depth"
)
print(ens_df2)

print("After popping..")
print(lipd.get_all_dataset_names())
ts_list_remote = lipd.get_timeseries(lipd.get_all_dataset_names())
for dsname, tsos in ts_list_remote.items():
    for tso in tsos:
        print(dsname+': '+str(tso['paleoData_variableName'])+': '+tso['archiveType'])

print("Popped..")
print(poplipd.get_all_dataset_names())

print("Merging back..")
mergelipd = lipd.merge(poplipd)
print(mergelipd.get_all_dataset_names())

ts_list_remote = mergelipd.get_timeseries(mergelipd.get_all_dataset_names())
for dsname, tsos in ts_list_remote.items():
    for tso in tsos:
        print(dsname+': '+str(tso['paleoData_variableName'])+': '+tso['archiveType'])

'''
print(lipd.get_all_dataset_names())    
datasets = lipd.get_datasets(dsnames=dsnames)
print("Fetched..")
for ds in datasets:
    print(ds['id'])
    #print(json.dumps(ds, indent=3))
'''

# Usage
# - Just look at https://pyleoclim-util.readthedocs.io/en/master/core/api.html#lipdseries-pyleoclim-lipdseries
# - Implementing Series, MultipleSeries, EnsemebleSeries, Lipd, LipdSeries
# - Pyleoclim
#     - Given: Variable name, optional Dataset IDs
#       - Return time series data for the  matching variables (optional fuzzy match)
#     - Given: Proxy, optional Dataset IDs
#       - Return time series data for the  variables with matching proxies (optional fuzzy match)

#   - Time Series Data consists of:
#       - Variable value, Variable name, Variable unit, Time axis name (age/year), Time axis unit, Time axis values, Lat, Long, Dataset ID

#   - Lat, Long, Elevation
#   - Get the ensemble table given a dataset ID & age Year
# - Own metadata