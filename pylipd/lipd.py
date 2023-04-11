"""
The LiPD class describes a `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ object. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of the LiPD data into an RDF graph containing terms from the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`
How to browse and query LiPD objects is described in a short example below, while `this notebook <https://nbviewer.jupyter.org/github/LinkedEarth/pylipd/blob/master/example_notebooks/pylipd_tutorial.ipynb>`_ demonstrates how to use PyLiPD to view and query LiPD datasets.
"""

import math
import os
import pickle
import re
import copy
import os.path
import tempfile
import pandas as pd
import random
import string
import io

from rdflib import ConjunctiveGraph, Namespace, URIRef
from pylipd.globals.queries import QUERY_BIBLIO, QUERY_DSID, QUERY_DSNAME, QUERY_ENSEMBLE_TABLE
from pylipd.multi_processing import multi_convert_to_pickle, multi_convert_to_rdf

from pylipd.rdf_to_lipd import RDFToLiPD
from pylipd.legacy_utils import LiPD_Legacy
from pylipd.utils import sanitizeId, sparql_results_to_df

#import bibtexparser
#from bibtexparser.bibdatabase import BibDatabase
from doi2bib import crossref
from pybtex.database import BibliographyData, Entry

from .globals.urls import NSURL, ONTONS

from copy import deepcopy


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
        
        ts_list = lipd.get_timeseries(lipd.get_all_dataset_names())

        for dsname, tsos in ts_list.items():
            for tso in tsos:
                if 'paleoData_variableName' in tso:
                    print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])
    '''
    def __init__(self, graph=None):
        if graph is None:
            self._initialize_graph()
        else:
            self.graph = graph

    def _initialize_graph(self):
        self.graph = ConjunctiveGraph()
        self.graph.bind("le", Namespace(ONTONS))        
        #self.graph.bind("", Namespace(NS))

    def copy(self):
        '''
        Makes a copy of the object

        Returns
        -------
        pylipd.LiPD
            a copy of the original object

        '''
        
        return deepcopy(self)

    def merge(self, lipd):
        '''
        Merges the current LiPD object with another LiPD object

        Parameters
        ----------
        lipd : pylipd.LiPD
            LiPD object to merge with

        Returns
        -------
        pylipd.LiPD
            merged LiPD object

        '''

        merged = self.copy()
        merged.graph.addN(lipd.graph.quads())
        return merged
    
    def load_from_dir(self, dir_path, parallel=False):
        '''Load LiPD files from a directory
        Note: This function creates multiple process to process lipd files in parallel, therefore it is important that this call be made under the "__main__" process

        Parameters
        ----------

        dir_path : str
            path to the directory containing lipd files

        parallel: bool
            (Optional) set to True to process lipd files in parallel. You *must* run this function under the "__main__" process for this to work

        Examples
        --------
        In this example, we load LiPD files from a directory.

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            lipd = LiPD()        
            lipd.load_from_dir("../examples/data")

            print(lipd.get_all_dataset_names())
        '''
        if not os.path.isdir(dir_path):
            print(f"Directory {dir_path} does not exist")
            return

        lipdfiles = []
        for path in os.listdir(dir_path):
            file_path = os.path.join(dir_path, path)
            if os.path.isfile(file_path) and path.endswith(".lpd"):
                lipdfiles.append(file_path)
        self.load(lipdfiles, parallel)


    # Allows loading http locations
    def load(self, lipdfiles, parallel=False):
        '''Load LiPD files. 
        Note: This function creates multiple process to process lipd files in parallel, therefore it is important that this call be made under the "__main__" process

        Parameters
        ----------

        lipdfiles : list of str
            array of paths to lipd files (the paths could also be urls)

        parallel: bool
            (Optional) set to True to process lipd files in parallel. You *must* run this function under the "__main__" process for this to work


        Examples
        --------
        In this example, we load LiPD files for an array of paths.

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            lipd = LiPD() 
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd",
                "../examples/data/Ant-WAIS-Divide.Severinghaus.2012.lpd",
                "https://lipdverse.org/data/LCf20b99dfe8d78840ca60dfb1f832b9ec/1_0_1/Nunalleq.Ledger.2018.lpd"                    
            ])            

            print(lipd.get_all_dataset_names())
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
        
        print(f"Loading {len(filemap.keys())} LiPD files")
        
        multi_convert_to_pickle(filemap, parallel)
        print("Conversion to RDF done..")

        print("Loading RDF into graph")
        for lipdfile in lipdfiles:
            picklefile = filemap[lipdfile]
            if os.path.exists(picklefile):
                with open(picklefile, 'rb') as f:
                    subgraph = pickle.load(f)
                    self.graph.addN(subgraph.quads())
                os.remove(picklefile)
        print("Loaded..")


    def clear(self):
        '''Clears the graph'''
        self._initialize_graph()


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

            # Fetch LiPD data from remote RDF Graph
            lipd_remote = LiPD()
            lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
            lipd_remote.load_remote_datasets(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
            print(lipd_remote.get_all_dataset_names())

        '''
        self.endpoint = endpoint


    def convert_lipd_dir_to_rdf(self, lipd_dir, rdf_file, parallel=False):
        '''Convert a directory containing LiPD files into a single RDF file (to be used for uploading to Knowledge Bases like GraphDB)

        Parameters
        ----------

        lipd_dir : str
            Path to the directory containing lipd files

        rdf_file : str
            Path to the output rdf file


        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

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

        multi_convert_to_rdf(filemap, parallel)
        
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


    def query(self, query, remote=False, result="sparql"):
        '''Once LiPD files or loaded into the graph (or remote endpoint set), one can make SparQL queries to the graph

        Parameters
        ----------

        query : str
            SparQL query

        remote: bool
            (Optional) If set to True, the query will be made to the remote endpoint (if set)

        result : str
            (Optional) Result return type

        Returns
        -------

        result : dict
            Dictionary of sparql variable and binding values
        
        result_df : pandas.Dataframe
            Return the dictionary above as a pandas.Dataframe
    
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

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
            result, result_df = lipd.query(query)
            result_df
        '''

        if remote and self.endpoint:
            print("Making remote query to endpoint: " + self.endpoint)
            matches = re.match(r"(.*)\s*SELECT\s+(.+)\s+WHERE\s+{(.+)}\s*(.*)", query, re.DOTALL | re.IGNORECASE)
            if matches:
                prefix = matches.group(1)
                vars = matches.group(2)
                where = matches.group(3)
                suffix = matches.group(4)
                query = f"{prefix} SELECT {vars} WHERE {{ SERVICE <{self.endpoint}> {{ {where} }} }} {suffix}"   
        
        result = self.graph.query(query)
        result_df = sparql_results_to_df(result)
        
        return result, result_df 

    # def whatArchive(self):
        
    #     archive_query = """PREFIX le: <http://linked.earth/ontology#>
    #             select ?archiveType (count(distinct ?archiveType) as ?count) where { 
    #                 ?ds a le:Dataset .
    #                 ?ds le:hasUrl ?url
    #             }"""

    def load_remote_datasets(self, dsnames):
        '''Loads remote datasets into cache if a remote endpoint is set

        Parameters
        ----------

        dsnames : array
            array of dataset names

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd_remote = LiPD()
            lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
            lipd_remote.load_remote_datasets(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
            print(lipd_remote.get_all_dataset_names())
        '''
        if not self.endpoint:
            raise Exception("No remote endpoint")
        
        if type(dsnames) is not list:
            dsnames = [dsnames]
            
        if dsnames == None or len(dsnames) == 0:
            raise Exception("No dataset names to cache")
        dsnamestr = (' '.join('<' + NSURL + "/" + dsname + '>' for dsname in dsnames))
        print("Caching datasets from remote endpoint..")
        qres, qres_df = self.query(f"SELECT ?s ?p ?o ?g WHERE {{ GRAPH ?g {{ ?s ?p ?o }} VALUES ?g {{ {dsnamestr} }} }}", remote=True)

        # Reinitialize graph
        # self._initialize_graph()
        for row in qres:
            self.graph.add((row.s, row.p, row.o, row.g))
        print("Done..")


    def update_remote_datasets(self, dsnames):
        '''Updates local LiPD Graph for datasets to remote endpoint'''
        if not self.endpoint:
            raise Exception("No remote endpoint")
        # TODO: Implement this


    def get_bibtex(self, remote = True, save = True, path = 'mybiblio.bib', verbose = False):
        '''Get BibTeX for loaded datasets
        
        Parameters
        ----------
        remote : bool 
            (Optional) If set to True, will return the bibliography by checking against the DOI
        
        save : bool
            (Optional) Whether to save the bibliography to a file
            
        path : str
            (Optional) Path where to save the file
        
        verbose : bool
            (Optional) Whether to print out on the console. Note that this option will turn on automatically if saving to a file fails. 

        Returns
        -------
        bibs : list
            List of BiBTex entry
        
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            print(lipd.get_bibtex())
        '''

        def establish_type(pub_type):
            
            if pub_type:
                pub_type = re.sub('-', '', pub_type).lower()
            else:
                pub_type = 'misc'
            
            if re.match(r".*article.*", pub_type) or re.match(r".*shortcommunication.*", pub_type):
                pub_type = 'article'
            elif re.match(r".*chapter.*", pub_type) or re.match(r".*book.*", pub_type):
                pub_type = 'chapter'
            elif re.match(r".*report.*", pub_type):
                pub_type = 'report'
            else:
                pub_type = 'misc'
            
            return pub_type

        def make_bib(row):
            pub_type = establish_type(row['type'])
            
            # Create a unique citation ID if not given
            row = row.fillna("")
            if row['citeKey'] is None:
                characters = string.ascii_letters + string.digits
                citation_key = ''.join(random.choice(characters) for i in range(8))
            else:
                citation_key = row['citeKey']
            
            entries = [] #start creating the list
            
            if row['authors']:
                entries.append(('author', str(row['authors'])))
            if row['doi']:
                entries.append(('doi',str(row['doi'])))
            if row['year']:
                entries.append(('year',str(row['year'])))
            if row['pubyear']:
                entries.append(('year',str(row['pubyear'])))
            if row['title']:
                if pub_type == 'article' or pub_type == 'misc':
                    entries.append(('title',str(row['title'])))
                elif pub_type == 'chapter' or pub_type == 'report':
                    entries.append(('chapter', str(row['title'])))
            if row['journal']:
                if pub_type == 'article':
                    entries.append(('journal', str(row['journal'])))
                if pub_type == 'book':
                    entries.append(('title', str(row['journal'])))
            if row['volume']:
                entries.append(('volume', str(row['volume'])))
            if row['issue']:
                entries.append(('issue', str(row['issue'])))
            if row['pages']:
                entries.append(('pages', str(row['pages'])))
            if row['publisher']:
                entries.append(('publisher', str(row['publisher'])))
            if row['report']:
                entries.append(('title', str(row['report'])))
            if row['edition']:
                entries.append(('edition', str(row['edition'])))
            if row['institution']:
                entries.append(('institution',str(row['institution'])))
            if row['url']:
                entries.append(('url',str(row['url'])))
            if row['url2']:
                entries.append(('url',str(row['url2'])))
            
            if pub_type == 'article':
                bib = BibliographyData({citation_key:Entry('article',entries)})
            elif pub_type == 'chapter' or pub_type == 'report':
                bib = BibliographyData({citation_key:Entry('inbook',entries)})
            elif pub_type == 'misc':
                bib = BibliographyData({citation_key:Entry('misc',entries)})
            
            return bib  
        
        result, df = self.query(QUERY_BIBLIO)
        
        bibs = []

        for idx,row in df.iterrows():
            if remote == True:
                try: 
                    f = (crossref.get_bib(row['doi']))
                    if f[0]==True:
                        bibs.append(f[1])
                    else:
                        print("Cannot find a matching record for the provided DOI, creating the entry manually")
                        bibs.append(make_bib(row).to_string('bibtex'))
                except:
                    print("Cannot parse the provided DOI, creating the entry manually")
                    bibs.append(make_bib(row).to_string('bibtex'))
            
        if save == True:   
            try:
                with io.open(path, 'w', encoding="utf-8") as bibfile:
                    for bib in bibs:
                        bibfile.write("{}\n".format(bib))

            except TypeError:
                print("Can't save in output file\n")
                verbose = True
        
        if verbose == True:
            print(bibs)
        
        return bibs, df       

    def get_timeseries(self, dsnames, to_dataframe=False):
        '''Get Legacy LiPD like Time Series Object (tso)

        Parameters
        ----------

        dsnames : list
            array of dataset id or name strings
        
        to_dataframe : bool {True; False}
            Whether to return a dataframe along the dictionary. Default is False
        
        Returns
        -------
        
        ts : dict
            A dictionary containing Time Series Object
            
        df : Pandas.DataFrame
            If to_dataframe is set to True, returns a queriable Pandas DataFrame

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd_remote = LiPD()
            lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
            ts_list = lipd_remote.get_timeseries(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
            for dsname, tsos in ts_list.items():
                for tso in tsos:
                    if 'paleoData_variableName' in tso:
                        print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])
        '''
        ts = self._get_timeseries(dsnames)
        if to_dataframe == False:
            return ts
        elif to_dataframe == True:
            dict_list =[]

            for item in ts.keys():
                for dictionary in ts[item]:
                    dict_list.append(dictionary)

            df = pd.DataFrame.from_dict(dict_list, orient='columns')
            
            return ts, df

    def _get_timeseries(self, dsnames):
        timeseries = {}
        for dsname in dsnames:
            converter = RDFToLiPD(self.graph)
            d = converter.convert_to_json(dsname)
            print("Extracting timeseries from dataset: " + dsname + " ...")
            if len(d.items()):
                tss = LiPD_Legacy().extract(d)
                timeseries[dsname] = tss
        return timeseries

    def get_lipd(self, dsname, lipdfile):
        '''Get LiPD json for a dataset

        Parameters
        ----------

        dsname : str
            dataset id

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
            ])
            lipd_json = lipd.get_lipd(lipd.get_all_dataset_names()[0])
            print(lipd_json)
        '''           
        converter = RDFToLiPD(self.graph)
        return converter.convert_to_json(dsname, lipdfile)

    def create_lipd(self, dsname, lipdfile):
        '''Create LiPD file for a dataset

        Parameters
        ----------

        dsname : str
            dataset id

        lipdfile: str
            path to LiPD file

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
            ])
            dsname = lipd.get_all_dataset_names()[0]
            lipd.create_lipd(dsname, "test.lpd")
        '''           
        converter = RDFToLiPD(self.graph)
        return converter.convert(dsname, lipdfile)
    
    def pop(self, dsnames):
        '''Pops dataset(s) from the graph and returns the popped LiPD object

        Parameters
        ----------

        dsnames : str or list of str
            dataset name(s) to be popped.


        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            all_datasets = lipd.get_all_dataset_names()
            print("Loaded datasets: " + str(all_datasets))
            popped = lipd.pop(all_datasets[0])
            print("Loaded datasets after pop: " + str(lipd.get_all_dataset_names()))
            print("Popped dataset: " + str(popped.get_all_dataset_names()))       
        '''

        popped = LiPD()

        if type(dsnames) is not list:
            dsnames = [dsnames]
        
        graphurls=[]
        for dsname in dsnames:
            graphurls.append(NSURL + "/" + dsname)

        # Match subgraphs
        for ctx in self.graph.contexts():
            id = str(ctx.identifier)
            if id in graphurls:
                subgraph = copy.deepcopy(self.graph.get_context(id))
                for triple in subgraph.triples((None, None, None)):
                    popped.graph.add((
                        triple[0],
                        triple[1],
                        triple[2],
                        URIRef(id)))

                self.graph.remove((None, None, None, id))
        
        return popped

    def remove(self, dsnames):
        '''Removes dataset(s) from the graph

        Parameters
        ----------

        dsnames : str or list of str
            dataset name(s) to be removed

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            all_datasets = lipd.get_all_dataset_names()
            print("Loaded datasets: " + str(all_datasets))
            lipd.remove(all_datasets[0])
            print("Loaded datasets after remove: " + str(lipd.get_all_dataset_names()))
        '''
        
        if type(dsnames) is not list:
            dsnames = [dsnames]
        
        graphurls=[]
        for dsname in dsnames:
            graphurls.append(NSURL + "/" + dsname)

        # Match subgraphs
        for ctx in self.graph.contexts():
            id = str(ctx.identifier)
            if id in graphurls:
                self.graph.remove((None, None, None, id))       


    def get_rdf(self):
        '''Returns RDF serialization of the current Graph
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            nquads = lipd.get_rdf()
            print(nquads[:10000])
            print("...")
        '''
        
        return self.graph.serialize(format='nquads')


    def get_all_dataset_names(self):
        '''Get all Dataset Names
        
        Returns
        -------
        
        dsnames : list
        
        A list of datasetnames
        
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            print(lipd.get_all_dataset_names())
        '''        
        qres, qres_df = self.query(QUERY_DSNAME)
        return [sanitizeId(row.dsname) for row in qres]

    def get_all_dataset_ids(self):
        '''Get all Dataset ids
        
        Returns
        -------
        
        dsids : list
        
        A list of datasetnames
        
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            print(lipd.get_all_dataset_ids())
        '''
        qres, qres_df = self.query(QUERY_DSID)
        return [sanitizeId(row.dsid) for row in qres]
    

    def search_datasets(variableName=[ ], archiveType=[ ], proxy=[ ], resolution = [ ],
                    ageUnits = [ ], ageBound = [ ], ageBoundType = [ ], 
                    lat = [ ], lon = [ ], alt = [ ], 
                    print_response = True, download_lipd = True,
                    download_folder = 'default'):
        pass


    def get_ensemble_tables(self, archiveType, varName, timeVarName, depthVarName, ensembleVarName, ensembleDepthVarName):
        '''Gets ensemble tables from the LiPD graph

        Parameters
        ----------

        archiveType : str
            archive type (Set to ".*" to match all archive types)
        varName : str
            variable name (Set to ".*" to match all variable names)
        timeVarName : str
            time variable name (Set to ".*" to match all time variable names)
        depthVarName : str
            depth variable name (Set to ".*" to match all depth variable names)
        ensembleVarName : str
            ensemble variable name (Set to ".*" to match all ensemble variable names)
        ensembleDepthVarName : str
            ensemble depth variable name (Set to ".*" to match all ensemble depth variable names)

        Returns
        -------

        ensemble_tables : dataframe
            A dataframe containing the ensemble tables


        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.lipd import LiPD

            lipd = LiPD()
            lipd.load([
                "../examples/data/ODP846.Lawrence.2006.lpd"
            ])
            all_datasets = lipd.get_all_dataset_names()
            print("Loaded datasets: " + str(all_datasets))

            ens_df = lipd.get_ensemble_tables(
                archiveType=".*",
                varName="c37",
                timeVarName="age",
                depthVarName="depth",
                ensembleVarName="age",
                ensembleDepthVarName="depth"
            )
            print("Ensemble tables:")
            print(ens_df)
        '''
       
        query = QUERY_ENSEMBLE_TABLE
        query = query.replace("[archiveType]", archiveType)
        query = query.replace("[varName]", varName)
        query = query.replace("[timeVarName]", timeVarName)
        query = query.replace("[depthVarName]", depthVarName)
        query = query.replace("[ensembleVarName]", ensembleVarName)
        query = query.replace("[ensembleDepthVarName]", ensembleDepthVarName)

        qres, qres_df = self.query(query)
        return qres_df

