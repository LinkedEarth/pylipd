from lipd import LiPD, convert_to_rdf
import json
import os

####################
# TODO:
# - Add ensemble table to the LiPD to RDF conversion
# - Reload the graph to the endpoint
####################

if __name__=="__main__":
    lipd = LiPD()

    
    # Convert LiPD files to RDF
    lipd.convert_lipd_dir_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd", 
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.nq")
    
    # Load LiPD files into local RDF graph
    print("========== LOCAL API =========")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Temp12k1_1_0/", "Temp12k1_1_0")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Pages2k2_1_2/", "Pages2k2_1_2")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/wNAm1_0_0/", "wNAm1_0_0")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/iso2k1_0_1/", "iso2k1_0_1")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/PalMod1_0_1/", "PalMod1_0_1")
    
    '''
    convert_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd/MD98_2181.Stott.2007.lpd",
        "/Users/varun/git/LiPD/PyLiPD/data/MD98_2181.Stott.2007.nq"
    )
    lipdfiles = [
        #"https://github.com/LinkedEarth/Pyleoclim_util/blob/master/example_data/MD982176.Stott.2004.lpd?raw=true",
        "/Users/varun/git/LiPD/PyLiPD/data/lpd/Asi-TDAXJP.PAGES2k.2013.lpd",
        #"/Users/varun/git/LiPD/PyLiPD/data/lpd/MD98_2181.Stott.2007.lpd"
        #"/Users/varun/git/LiPD/PyLiPD/data/lpd/geoChronR-examples/Kurupa.Boldt.2015.lpd"
    ]
    lipd.load_local(lipdfiles)

    print("Fetching Datasets..")
    datasets = lipd.get_datasets(data_only=False)
    print("Fetched..")
    for ds in datasets:
        #print(ds['id'])
        print(json.dumps(ds, indent=3))
    
    '''
    
    # Fetch LiPD data from remote RDF Graph
    #print("========== REMOTE API =========")
    #lipd.load_remote("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse")
    #ds = lipd.get_dataset("http://linked.earth/lipd/Pages2k2_1_2#Ant-WAIS-Divide.Severinghaus.2012", data_only=True)
    #print(ds)

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