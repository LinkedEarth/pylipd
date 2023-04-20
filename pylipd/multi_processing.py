from tqdm import tqdm
from pylipd.globals.queries import QUERY_ALL_VARIABLES_GRAPH
from pylipd.lipd_to_rdf import LipdToRDF
import multiprocessing as mp
import copy

def convert_to_rdf(lipdfile, rdffile):
    converter = LipdToRDF()    
    """Worker that converts one lipdfile to an rdffile"""
    try:
        converter.convert(lipdfile)
        converter.serialize(rdffile)
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


def convert_lipd_to_graph(lipdfile):
    """Worker that converts one lipdfile to an RDF graph"""
    try:
        converter = LipdToRDF()
        converter.convert(lipdfile)
        return converter.graph
    except Exception as e:
        print(f"ERROR: Could not convert LiPD file {lipdfile} to RDF")            
        raise e


def multi_load_lipd(graph, lipdfiles, parallel=True):
    """Load all lipdfiles to the RDF graph"""
    if parallel:            
        with mp.Pool(mp.cpu_count()) as pool:
            for subgraph in tqdm(pool.imap_unordered(convert_lipd_to_graph, lipdfiles, chunksize=1), total=len(lipdfiles)):
                graph.addN(subgraph.quads())
                del subgraph
            pool.close()
            pool.join()

    else:
        for i in tqdm(range(0, len(lipdfiles))):
            lipdfile = lipdfiles[i]
            subgraph = convert_lipd_to_graph(lipdfile)
            graph.addN(subgraph.quads())
            del subgraph
    return graph

    
def extract_variables_graph(arg):
    ctxid, subgraph = arg
    query = QUERY_ALL_VARIABLES_GRAPH
    subgraph.update(query)
    subgraph.remove((None, None, None, ctxid))
    return (ctxid, subgraph)


def multi_load_lipd_series(graph, single_dataset_lipds, parallel=True):
    """Load all lipd variables to the RDF graph"""

    args = []
    for ctxid, lipd in single_dataset_lipds.items():
        args.append((ctxid, lipd.graph))

    print("- Extracting variable subgraphs")
    if parallel:
        with mp.Pool(mp.cpu_count()) as pool:
            for (ctxid, subgraph) in tqdm(pool.imap_unordered(extract_variables_graph, args, chunksize=1), total=len(args)):
                # TODO: Add triples to store the dsname & tablename that the variable belongs to
                graph.addN(subgraph.quads())
            pool.close()
            pool.join()

    else:
        for i in tqdm(range(0, len(args))):
            ctxid, subgraph = args[i]
            ctxid, subgraph = extract_variables_graph(args[i])
            graph.addN(subgraph.quads())
    return graph

