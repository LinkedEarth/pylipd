from lipd import LiPD

####################
# TODO:
# - Edit local LiPD & update endpoint
####################

if __name__=="__main__":
    lipd = LiPD()

    local_lipd_dir = "/Users/varun/git/LiPD/PyLiPD/data/lpd"
    remote_lipd_endpoint = "https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2"

    '''
    # Convert LiPD files to RDF    
    lipd.convert_lipd_dir_to_rdf(
        local_lipd_dir,
        local_lipd_dir+".nq")
    
    # Convert one LiPD file to RDF
    convert_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd/MD98_2181.Stott.2007.lpd",
        "/Users/varun/git/LiPD/PyLiPD/data/MD98_2181.Stott.2007.nq"
    )
    '''

    # Load Datasets (from Local and Remote)
    dsids = ["MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012", "Asi-TDAXJP.PAGES2k.2013"]

    # Load from local
    lipdfiles = [local_lipd_dir + "/" + dsid + ".lpd" for dsid in dsids]
    lipd.load(lipdfiles)
    #lipd.load_from_dir(local_lipd_dir)
    
    # Fetch LiPD data from remote RDF Graph
    #lipd.set_endpoint(remote_lipd_endpoint)
    #lipd.load_remote_datasets(dsids=dsids)

    # Convert to TSO object (as before)
    ts_list = lipd.convert_to_timeseries(dsids)
    for item in ts_list:
        print(item['dataSetName']+': '+item['paleoData_variableName'])

    '''
    datasets = lipd.get_datasets(dsids=dsids)
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