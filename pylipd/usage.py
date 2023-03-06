from pylipd.lipd import LiPD
from pylipd.multi_processing import convert_to_rdf

####################
# TODO:
# - Edit local LiPD & update endpoint
####################

if __name__=="__main__":
    local_lipd_dir = "/Users/varun/git/LiPD/PyLiPD/data/lpd"
    remote_lipd_endpoint = "https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2"

    lipd = LiPD()

    '''
    # Convert LiPD files to RDF    
    lipd.convert_lipd_dir_to_rdf(
        local_lipd_dir,
        local_lipd_dir+".nq")
    
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

    L = LiPD()
    #L.load(local_lipd_dir+"/"+"ODP1671017E.lpd")
    #L.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")    
    L.load([local_lipd_dir + "/" + dsname + ".lpd" for dsname in ["MD98_2181.Stott.2007","NAm-SmithersSkiArea.Schweingruber.1996", 
                            "NAm-CeaderBreaks.Briffa.1996", "ODP1671017E", 
                            "SPC14.Kahle.2021", "RC12-10.Poore.2003", 
                            "MD02-2553.Poore.2009", "AD9117.Guinta.2001",
                            "SchellingsBog.Barron.2004", "Hidden.Tang.1999"]])
    #bibtex = L.get_bibtex()
    #print(bibtex)
    #exit()

    # Load from local
    lipd = LiPD()
    lipdfiles = [local_lipd_dir + "/" + dsname + ".lpd" for dsname in dsnames]
    #print(lipdfiles)
    
    lipd.load(lipdfiles)
    #lipd.load_from_dir(local_lipd_dir)
    print(lipd.get_all_dataset_names())
    print(lipd.get_all_dataset_ids())

    #lipd.load(["/Users/varun/Downloads/Arc-LakeNataujärvi.Ojala.2005.lpd"])
    #print(lipd.get_all_dataset_names())
    
    for dsname in lipd.get_all_dataset_names():
        json = lipd.get_lipd(dsname)
        print(json['pub'])

    ts_list = lipd.get_timeseries(lipd.get_all_dataset_names())
    for dsname, tsos in ts_list.items():
        for tso in tsos:
            if 'paleoData_variableName' in tso:
                print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])

    exit()
    
    # Fetch LiPD data from remote RDF Graph
    lipd.set_endpoint(remote_lipd_endpoint)
    lipd.load_remote_datasets(remote_dsnames)

    # Convert to TSO object (as before)
    ts_list_remote = lipd.get_timeseries(lipd.get_all_dataset_names())
    for dsname, tsos in ts_list_remote.items():
        for tso in tsos:
            print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])

    print(lipd.get_all_dataset_names())
    poplipd = lipd.pop(remote_dsnames[0])
    print("After popping..")
    print(lipd.get_all_dataset_names())
    print("Popped..")
    print(poplipd.get_all_dataset_names())
    
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