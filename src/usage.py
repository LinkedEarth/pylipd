from lipd import LiPD
import os

if __name__=="__main__":
    print("========== LOCAL API =========")
    lipdfiles = []
    dir_path = "/Users/varun/git/LiPD/PyLiPD/data/lpd/globalHolocene1_0_0/"
    for path in os.listdir(dir_path):
        fullpath = os.path.join(dir_path, path)
        lipdfiles.append(fullpath)

    #lipdfiles = [
    #    "/Users/varun/git/LiPD/PyLiPD/data/lpd/Temp12k1_0_2/RiviereFeuilles2.Larouche.1981.lpd", 
    #    "/Users/varun/git/LiPD/PyLiPD/data/lpd/Temp12k1_0_2/MD98_2181.Stott.2007.lpd",
    #    "/Users/varun/git/LiPD/PyLiPD/data/lpd/geoChronR-examples/Kurupa.Boldt.2015.lpd"
    #]

    lipd = LiPD()
    print(f"Loading {len(lipdfiles)} Files..")
    lipd.load_local(lipdfiles)

    print("Fetching Datasets..")
    datasets = lipd.get_datasets()
    print("Fetched..")
    for ds in datasets:
        print(ds['id'])


    '''
    print("========== REMOTE API =========")
    lipd_remote = LiPD()
    lipd_remote.load_remote("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse")
    ds = lipd_remote.get_dataset("http://linked.earth/lipd/Temp12k1_0_2#117_723A.Godad.2011", data_only=True)
    print(ds)
    '''