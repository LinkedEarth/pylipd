from lipd import LiPD
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
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/PalMod1_0_1/", 
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/PalMod1_0_1.nt",
        "PalMod1_0_1")
    lipd.convert_lipd_dir_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Temp12k1_1_0/", 
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Temp12k1_1_0.nt",
        "Temp12k1_1_0")
    lipd.convert_lipd_dir_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Pages2k2_1_2/", 
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Pages2k2_1_2.nt",
        "Pages2k2_1_2")
    lipd.convert_lipd_dir_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/wNAm1_0_0/", 
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/wNAm1_0_0.nt",
        "wNAm1_0_0")
    lipd.convert_lipd_dir_to_rdf(
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/iso2k1_0_1/", 
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/iso2k1_0_1.nt",
        "iso2k1_0_1")


    '''
    # Load LiPD files into local RDF graph
    print("========== LOCAL API =========")
    lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Temp12k1_1_0/", "Temp12k1_1_0")
    lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Pages2k2_1_2/", "Pages2k2_1_2")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/wNAm1_0_0/", "wNAm1_0_0")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/iso2k1_0_1/", "iso2k1_0_1")
    #lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd.new/PalMod1_0_1/", "PalMod1_0_1")
    '''
    
    '''
    lipdfiles = [
        #"https://github.com/LinkedEarth/Pyleoclim_util/blob/master/example_data/MD982176.Stott.2004.lpd?raw=true",
        "/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Pages2k2_1_2/Ant-WAIS-Divide.Severinghaus.2012.lpd" 
        #"/Users/varun/git/LiPD/PyLiPD/data/lpd.new/Temp12k1_1_0/MD98_2181.Stott.2007.lpd",
        #"/Users/varun/git/LiPD/PyLiPD/data/lpd/geoChronR-examples/Kurupa.Boldt.2015.lpd"
    ]
    lipd.load_local(lipdfiles, collection_id="Pages2k2_1_2")
    '''

    '''
    print("Fetching Datasets..")
    datasets = lipd.get_datasets(data_only=False)
    print("Fetched..")
    for ds in datasets:
        print(ds)
    '''

    '''
    # Fetch LiPD data from remote RDF Graph
    print("========== REMOTE API =========")
    lipd.load_remote("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse")
    ds = lipd.get_dataset("http://linked.earth/lipd/Pages2k2_1_2#Ant-WAIS-Divide.Severinghaus.2012", data_only=True)
    print(ds)
    '''