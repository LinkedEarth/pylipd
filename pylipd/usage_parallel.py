if __name__ == "__main__":
    from pylipd.lipd import LiPD

    local_lipd_dir = "/Users/varun/git/LiPD/PyLiPD/data/lpd"

    L = LiPD()

    # Convert LiPD files to RDF    
    L.convert_lipd_dir_to_rdf(
        local_lipd_dir,
        local_lipd_dir+".nq", 
        parallel=True,
        standardize=True,
        add_labels=False)
    exit()
    

    #L.load_from_dir(local_lipd_dir, parallel=True, cutoff=100)
    
    print(f"Total number of datasets: {len(L.get_all_dataset_names())}")

    print("Filtering by archive type and bounding box")
    
    #Lfiltered = L.filter_by_archive_type("marine").filter_by_geo_bbox(-50, -50, 50, 50)
    
    #print(f"Total number of filtered datasets: {len(Lfiltered.get_all_dataset_names())}")

    # Free up memory by deleting the original LiPD object
    #del L

    # Convert to LiPD Series
    print("Creating LiPD Series...")
    S = L.to_lipd_series(parallel=True)

    df = S.get_timeseries_essentials()
    print(df)

    #print("Filtering LiPD Series with variable name starting with 'd18O'")
    #S = S.filter_by_name("d18O")
    
    print("Printing all valid variables")
    print(S.get_all_variables())

    exit()
