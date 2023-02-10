from pylipd.lipd_to_rdf import LipdToRDF
import multiprocessing as mp

def convert_to_rdf(lipdfile, rdffile, collection_id=None):
    converter = LipdToRDF(collection_id)    
    """Worker that converts one lipdfile to an rdffile"""
    try:
        converter.convert(lipdfile, rdffile)
    except Exception as e:
        print(f"ERROR: Could not convert LiPD file {lipdfile} to RDF")            
        raise e

def multi_convert_to_rdf(filemap, collection_id=None):
    """Create a pool to convert all lipdfiles to rdffiles"""
    pool = mp.Pool(mp.cpu_count())
    args = [(lipdfile, rdffile, collection_id) for lipdfile, rdffile in filemap.items()]
    pool.starmap(convert_to_rdf, args, chunksize=1)
    pool.close()


def convert_to_pickle(lipdfile, tofile, collection_id=None):
    converter = LipdToRDF(collection_id)    
    """Worker that converts one lipdfile to an rdffile"""
    try:
        converter.convert(lipdfile, tofile, type="pickle")
    except Exception as e:
        print(f"ERROR: Could not convert LiPD file {lipdfile} to RDF")            
        raise e

def multi_convert_to_pickle(filemap, collection_id=None):
    """Create a pool to convert all lipdfiles to picklefiles"""
    pool = mp.Pool(mp.cpu_count())
    args = [(lipdfile, tofile, collection_id) for lipdfile, tofile in filemap.items()]
    pool.starmap(convert_to_pickle, args, chunksize=1)
    pool.close()
