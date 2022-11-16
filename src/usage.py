from lipd import LiPD

####################
# TODO:
# - Edit local LiPD & update endpoint
####################

if __name__=="__main__":
    lipd = LiPD()

    lipd_dir = "/Users/varun/git/LiPD/PyLiPD/data/lpd"

    '''
    # Convert LiPD files to RDF    
    lipd.convert_lipd_dir_to_rdf(
        lipd_dir,
        lipd_dir+".nq")
    

    # Load LiPD files into local RDF graph
    print("========== LOCAL API =========")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Temp12k1_1_0/", "Temp12k1_1_0")
    #lipd.load_local_from_dir(lipd_dir)

    # Convert one LiPD file to RDF
    convert_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd/MD98_2181.Stott.2007.lpd",
        "/Users/varun/git/LiPD/PyLiPD/data/MD98_2181.Stott.2007.nq"
    )
    '''

    # Load Datasets (from Local and Remote)

    dsids = ["MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012", "Asi-TDAXJP.PAGES2k.2013"]


    lipdfiles = [lipd_dir + "/" + dsid + ".lpd" for dsid in dsids]
    lipd.load_local(lipdfiles)
    #lipd.load_local_from_dir(lipd_dir)
    
    # Fetch LiPD data from remote RDF Graph
    #lipd.load_remote("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")

    ts_list = lipd.convert_to_timeseries(dsids)
    for item in ts_list:
        print(item['dataSetName']+': '+item['paleoData_variableName'])

    #datasets = lipd.get_datasets(data_only=False)
    #print("Fetched..")
    #for ds in datasets:
    #    print(ds['id'])
        #print(json.dumps(ds, indent=3))

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