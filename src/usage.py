from lipd import LiPD
import os

####################
# TODO:
# - Add ensemble table to the LiPD to RDF conversion
# - Reload the graph to the endpoint
####################

if __name__=="__main__":
    print("========== LOCAL API =========")
    
    lipd = LiPD()

    '''
    lipd.load_local_from_dir("/Users/varun/git/LiPD/PyLiPD/data/lpd/Temp12k1_0_2/")

    lipdfiles = [
        "/Users/varun/git/LiPD/PyLiPD/data/lpd/PalMod1_0_1/ODP846.lpd" 
        #"/Users/varun/git/LiPD/PyLiPD/data/lpd/Temp12k1_0_2/MD98_2181.Stott.2007.lpd",
        #"/Users/varun/git/LiPD/PyLiPD/data/lpd/geoChronR-examples/Kurupa.Boldt.2015.lpd"
    ]
    #lipd.load_local(lipdfiles)

    print("Fetching Datasets..")
    datasets = lipd.get_datasets()
    print("Fetched..")
    for ds in datasets:
        print(ds['id'])
    '''

    print("========== REMOTE API =========")
    lipd.load_remote("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse")
    ds = lipd.get_dataset("http://linked.earth/lipd/PalMod1_0_1#ODP846", data_only=True)
    print(ds)