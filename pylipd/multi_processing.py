from pylipd.lipd_to_rdf import LipdToRDF
import multiprocessing as mp

def convert_to_rdf(lipdfile, rdffile):
    converter = LipdToRDF()    
    """Worker that converts one lipdfile to an rdffile"""
    try:
        converter.convert(lipdfile, rdffile)
    except Exception as e:
        print(f"ERROR: Could not convert LiPD file {lipdfile} to RDF")            
        raise e

def multi_convert_to_rdf(filemap, parallel=True):
    if parallel:
        """Create a pool to convert all lipdfiles to rdffiles"""
        pool = mp.Pool(mp.cpu_count())
        args = [(lipdfile, rdffile) for lipdfile, rdffile in filemap.items()]
        pool.starmap(convert_to_rdf, args, chunksize=1)
        pool.close()
    else:
        for lipdfile, rdffile in filemap.items():
            convert_to_rdf(lipdfile, rdffile)

def convert_to_pickle(lipdfile, tofile):
    converter = LipdToRDF()    
    """Worker that converts one lipdfile to an rdffile"""
    try:
        converter.convert(lipdfile, tofile, type="pickle")
    except Exception as e:
        print(f"ERROR: Could not convert LiPD file {lipdfile} to RDF")            
        raise e

def multi_convert_to_pickle(filemap, parallel=True):
    """Create a pool to convert all lipdfiles to picklefiles"""
    if parallel:
        pool = mp.Pool(mp.cpu_count())
        args = [(lipdfile, tofile) for lipdfile, tofile in filemap.items()]
        pool.starmap(convert_to_pickle, args, chunksize=1)
        pool.close()
    else:
        for lipdfile, tofile in filemap.items():
            convert_to_pickle(lipdfile, tofile)
