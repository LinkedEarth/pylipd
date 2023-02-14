"""
The LiPD class describes a `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ object. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of the LiPD data into an RDF graph containing terms from the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`
How to browse and query LiPD objects is described in a short example below, while `this notebook <https://nbviewer.jupyter.org/github/LinkedEarth/pylipd/blob/master/example_notebooks/pylipd_tutorial.ipynb>`_ demonstrates how to use PyLiPD to view and query LiPD datasets.
"""

import os
import pickle
import re
import os.path
import tempfile

from rdflib import ConjunctiveGraph, Namespace
from pylipd.multi_processing import multi_convert_to_pickle, multi_convert_to_rdf

from pylipd.rdf_to_lipd import RDFToLiPD
from pylipd.legacy_utils import LiPD_Legacy
from pylipd.utils import sanitizeId

from .globals.urls import NSURL, ONTONS


class LiPD:
    '''The LiPD class describes a `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ object. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of the LiPD data into an RDF graph containing terms from the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`
    How to browse and query LiPD objects is described in a short example below.

    Examples
    --------
    In this example, we read an online LiPD file and convert it into a time series object dictionary.

    .. ipython:: python
        :okwarning:
        :okexcept:

        from pylipd.lipd import LiPD

        lipd = LiPD()        
        lipd.load(["https://lipdverse.org/data/LCf20b99dfe8d78840ca60dfb1f832b9ec/1_0_1//Nunalleq.Ledger.2018.lpd"])
        
        ts_list = lipd.get_timeseries(lipd.get_all_dataset_ids())

        for dsid, tsos in ts_list.items():
            for tso in tsos:
                if 'paleoData_variableName' in tso:
                    print(dsid+': '+tso['paleoData_variableName']+': '+tso['archiveType'])
    '''
    def __init__(self):
        self.initialize_graph()
        self.remote = False

    def initialize_graph(self):
        self.graph = ConjunctiveGraph()
        self.graph.bind("le", Namespace(ONTONS))        
        #self.graph.bind("", Namespace(NS))

    def load_from_dir(self, dir_path, collection_id=None):
        '''Load LiPD files from a directory
        Note: This function creates multiple process to process lipd files in parallel, therefore it is important that this call be made under the "__main__" process

        Parameters
        ----------

        dir_path : str
            path to the directory containing lipd files

        collection_id : str
            (Optional) set a collection id for all lipd files in the directory

        Examples
        --------
        In this example, we load LiPD files from a directory.

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                lipd = LiPD()        
                lipd.load_from_dir("../examples/data")

                print(lipd.get_all_dataset_ids())
        '''
        if not os.path.isdir(dir_path):
            print(f"Directory {dir_path} does not exist")
            return

        lipdfiles = []
        for path in os.listdir(dir_path):
            file_path = os.path.join(dir_path, path)
            if os.path.isfile(file_path) and path.endswith(".lpd"):
                lipdfiles.append(file_path)
        self.load(lipdfiles, collection_id)


    # Allows loading http locations
    def load(self, lipdfiles, collection_id=None):
        '''Load LiPD files. 
        Note: This function creates multiple process to process lipd files in parallel, therefore it is important that this call be made under the "__main__" process

        Parameters
        ----------

        lipdfiles : array
            array of paths to lipd files (the paths could also be urls)

        collection_id : str
            (Optional) set a collection id for all lipd files in the directory

        Examples
        --------
        In this example, we load LiPD files for an array of paths.

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                lipd = LiPD() 
                lipd.load([
                    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                    "../examples/data/MD98_2181.Stott.2007.lpd",
                    "../examples/data/Ant-WAIS-Divide.Severinghaus.2012.lpd",
                    "https://lipdverse.org/data/LCf20b99dfe8d78840ca60dfb1f832b9ec/1_0_1/Nunalleq.Ledger.2018.lpd"                    
                ])            

                print(lipd.get_all_dataset_ids())
        '''        
        if type(lipdfiles) is not list:
            lipdfiles = [lipdfiles]
            
        filemap = {}
        for lipdfile in lipdfiles:
            if not os.path.isfile(lipdfile) and not lipdfile.startswith("http"):
                print(f"File {lipdfile} does not exist")
                continue

            picklefile = tempfile.NamedTemporaryFile().name
            filemap[lipdfile] = picklefile
        
        print(f"Loading {len(filemap.keys())} LiPD files" + (" from Collection: {collection_id}" if collection_id else ""))
        
        multi_convert_to_pickle(filemap, collection_id)
        print("Conversion to RDF done..")

        self.remote = False
        print("Loading RDF into graph")
        for lipdfile in lipdfiles:
            picklefile = filemap[lipdfile]
            if os.path.exists(picklefile):
                with open(picklefile, 'rb') as f:
                    subgraph = pickle.load(f)
                    self.graph.addN(subgraph.quads())
                os.remove(picklefile)
        print("Loaded..")


    def set_endpoint(self, endpoint):
        '''Sets a SparQL endpoint for a remote Knowledge Base (example: GraphDB)

        Parameters
        ----------

        endpoint : str
            URL for the SparQL endpoint 

        Examples
        --------
        
        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                # Fetch LiPD data from remote RDF Graph
                lipd_remote = LiPD()
                lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
                lipd_remote.load_remote_datasets(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
                print(lipd_remote.get_all_dataset_ids())

        '''
        self.remote = True
        self.endpoint = endpoint


    def convert_lipd_dir_to_rdf(self, lipd_dir, rdf_file, collection_id=None):
        '''Convert a directory containing LiPD files into a single RDF file (to be used for uploading to Knowledge Bases like GraphDB)

        Parameters
        ----------

        lipd_dir : str
            Path to the directory containing lipd files

        rdf_file : str
            Path to the output rdf file

        collection_id : str
            (Optional) set a collection id for all lipd files in the directory

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                # Fetch LiPD data from remote RDF Graph
                lipd = LiPD()

                lipd.convert_lipd_dir_to_rdf("../examples/data", "all-lipd.nq")
        '''

        filemap = {}
        for path in os.listdir(lipd_dir):
            fullpath = os.path.join(lipd_dir, path)
            tmp_rdf_file = tempfile.NamedTemporaryFile().name
            filemap[fullpath] = tmp_rdf_file
        
        print(f"Starting conversion of {len(filemap.keys())} LiPD files")

        multi_convert_to_rdf(filemap, collection_id)
        
        print("Conversion to RDF done..")

        print("Writing to main RDF file..")
        with open(rdf_file, "a") as fout:
            for lipdfile in filemap.keys():
                tmp_rdf_file = filemap[lipdfile]
                if os.path.exists(tmp_rdf_file):
                    fin = open(tmp_rdf_file, "r")
                    data = fin.read();
                    fin.close()
                    fout.write(data)
                    os.remove(tmp_rdf_file)
            fout.close()
        print("Written..")


    def query(self, query, result="sparql"):
        '''Once LiPD files or loaded into the graph (or remote endpoint set), one can make SparQL queries to the graph

        Parameters
        ----------

        query : str
            SparQL query

        result : str
            (Optional) Result return type

        Returns
        -------

        result : dict
            Dictionary of sparql variable and binding values
    
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                lipd = LiPD()
                lipd.load([
                    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                    "../examples/data/MD98_2181.Stott.2007.lpd"
                ])
                query = """PREFIX le: <http://linked.earth/ontology#>
                        select (count(distinct ?ds) as ?count) where { 
                            ?ds a le:Dataset .
                            ?ds le:hasUrl ?url
                        }"""
                result = lipd.query(query)
                print(result)
        '''

        if self.remote:
            matches = re.match(r"\s*SELECT\s+(.+)\s+WHERE\s+{(.+)}\s*", query, re.DOTALL)
            if matches:
                vars = matches.group(1)
                where = matches.group(2)
                query = f"SELECT {vars} WHERE {{ SERVICE <{self.endpoint}> {{ {where} }} }}"
        return self.graph.query(query, result=result)

    def load_remote_datasets(self, dsids):
        '''Loads remote datasets into cache if a remote endpoint is set

        Parameters
        ----------

        dsids : array
            array of dataset id strings

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                # Fetch LiPD data from remote RDF Graph
                lipd_remote = LiPD()
                lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
                lipd_remote.load_remote_datasets(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
                print(lipd_remote.get_all_dataset_ids())
        '''
        if not self.remote or not self.endpoint:
            raise Exception("No remote endpoint")

        if dsids == None or len(dsids) == 0:
            raise Exception("No dataset ids to cache")
        dsidstr = (' '.join('<' + NSURL + "/" + dsid + '>' for dsid in dsids))
        print("Caching datasets from remote endpoint..")
        qres = self.query(f"SELECT ?s ?p ?o ?g WHERE {{ GRAPH ?g {{ ?s ?p ?o }} VALUES ?g {{ {dsidstr} }} }}")

        # Reinitialize graph
        self.initialize_graph()
        for row in qres:
            self.graph.add((row.s, row.p, row.o, row.g))
        print("Done..")
        self.remote = False

    def get_timeseries(self, dsids):
        '''Get Legacy LiPD like Time Series Object (tso)

        Parameters
        ----------

        dsids : array
            array of dataset id strings

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                # Fetch LiPD data from remote RDF Graph
                lipd_remote = LiPD()
                lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
                ts_list = lipd_remote.get_timeseries(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
                for dsid, tsos in ts_list.items():
                    for tso in tsos:
                        if 'paleoData_variableName' in tso:
                            print(dsid+': '+tso['paleoData_variableName']+': '+tso['archiveType'])
        '''        
        if self.remote:
            # Cache datasets locally - to speed up queries
            self.load_remote_datasets(dsids)
            ts = self._get_timeseries(dsids)

            # Go back to remote
            self.initialize_graph()
            self.set_endpoint(self.endpoint)

            return ts
        else:
            ts = self._get_timeseries(dsids)
            return ts

    def _get_timeseries(self, dsids):
        timeseries = {}
        for dsid in dsids:
            converter = RDFToLiPD()
            d = converter.convert(dsid, self.graph)
            print("Extracting timeseries from dataset: " + dsid + " ...")
            if len(d.items()):
                tss = LiPD_Legacy().extract(d)
                timeseries[dsid] = tss
        return timeseries

    def get_lipd(self, dsid):
        '''Get LiPD json for a dataset

        Parameters
        ----------

        dsid : str
            dataset id

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            if __name__=="__main__":
                # Fetch LiPD data from remote RDF Graph
                lipd_remote = LiPD()
                lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
                dsid = "Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001"
                lipd_remote.load_remote_datasets([dsid])
                lipd_json = lipd_remote.get_lipd(dsid)
                print(lipd_json)
        '''           
        converter = RDFToLiPD()            
        return converter.convert(dsid, self.graph)

    def get_all_dataset_ids(self):
        query = f"""
            SELECT ?dsname WHERE {{ 
                ?ds a le:Dataset .
                ?ds le:name ?dsname
            }}
            """
        qres = self.query(query)
        return [sanitizeId(row.dsname) for row in qres]

    def search_datasets(variableName=[ ], archiveType=[ ], proxyObsType=[ ], infVarType = [ ], sensorGenus=[ ],
                    sensorSpecies=[ ], interpName =[ ], interpDetail =[ ], ageUnits = [ ],
                    ageBound = [ ], ageBoundType = [ ], recordLength = [ ], resolution = [ ],
                    lat = [ ], lon = [ ], alt = [ ], print_response = True, download_lipd = True,
                    download_folder = 'default'):
        pass


    def find_ensemble_table_for_variable(self, ensemble_table):
        pass