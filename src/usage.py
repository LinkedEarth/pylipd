from lipd import LiPD

lipdfiles = [
    "/Users/varun/git/LiPD/PyLiPD/data/lpd/Temp12k1_0_2/RiviereFeuilles2.Larouche.1981.lpd", 
    "/Users/varun/git/LiPD/PyLiPD/data/lpd/Temp12k1_0_2/MD98_2181.Stott.2007.lpd",
    "/Users/varun/git/LiPD/PyLiPD/data/lpd/geoChronR-examples/Kurupa.Boldt.2015.lpd"
]
lipd = LiPD(lipdfiles)
datasets = lipd.get_datasets()
for ds in datasets:
    print("\n======= Dataset ========")
    print(ds)
