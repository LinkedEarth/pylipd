"""
The LiPD class describes a `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ object. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of the LiPD data into an RDF graph containing terms from the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`
How to browse and query LiPD objects is described in a short example below, while `this notebook <https://nbviewer.jupyter.org/github/LinkedEarth/pylipd/blob/master/example_notebooks/pylipd_tutorial.ipynb>`_ demonstrates how to use PyLiPD to view and query LiPD datasets.
"""

import os
import re
import os.path
import tempfile
import pandas as pd
import random
import string
import io

from rdflib import ConjunctiveGraph, URIRef
from tqdm import tqdm
from pylipd.globals.queries import QUERY_ALL_VARIABLES_GRAPH, QUERY_BIBLIO, QUERY_DSID, QUERY_DSNAME, QUERY_ENSEMBLE_TABLE, QUERY_ENSEMBLE_TABLE_SHORT, QUERY_FILTER_ARCHIVE_TYPE, QUERY_FILTER_GEO, QUERY_VARIABLE, QUERY_VARIABLE_GRAPH
from pylipd.lipd_series import LiPDSeries
from pylipd.multi_processing import multi_convert_to_rdf, multi_load_lipd
from pylipd.rdf_graph import RDFGraph

from pylipd.rdf_to_lipd import RDFToLiPD
from pylipd.legacy_utils import LiPD_Legacy
from pylipd.utils import sanitizeId

#import bibtexparser
#from bibtexparser.bibdatabase import BibDatabase
from doi2bib import crossref
from pybtex.database import BibliographyData, Entry

from .globals.urls import NSURL

class LiPD(RDFGraph):
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
        super().__init__(graph)

    
    def load_from_dir(self, dir_path, parallel=False, cutoff=None):
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
        if cutoff:
            lipdfiles = lipdfiles[0:cutoff]
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
            
        numfiles = len(lipdfiles)
        print(f"Loading {numfiles} LiPD files")
        self.graph = multi_load_lipd(self.graph, lipdfiles, parallel)
        print("Loaded..")


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

    def get_lipd(self, dsname):
        '''Get LiPD json for a dataset

        Parameters
        ----------

        dsname : str
            dataset id

        Returns
        -------

        lipdjson : dict
            LiPD json

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
        return converter.convert_to_json(dsname)

    def create_lipd(self, dsname, lipdfile):
        '''Create LiPD file for a dataset

        Parameters
        ----------

        dsname : str
            dataset id

        lipdfile: str
            path to LiPD file

        Returns
        -------

        lipdjson : dict
            LiPD json

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
    

    def get(self, dsnames):
        '''Gets dataset(s) from the graph and returns the popped LiPD object
        Parameters
        ----------
        dsnames : str or list of str
            dataset name(s) to get.
        
        Returns
        -------

        pylipd.lipd.LiPD
            LiPD object with the retrieved dataset(s)

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
            ds = lipd.get(all_datasets[0])
            print("Got dataset: " + str(ds.get_all_dataset_names()))       
        '''
        dsnames = [dsnames] if type(dsnames) is not list else dsnames
        dsids = [(f"{NSURL}/{dsname}" if not dsname.startswith(NSURL) else dsname) for dsname in dsnames]

        ds = super().get(dsids)
        return LiPD(ds.graph)

    def pop(self, dsnames):
        '''Pops dataset(s) from the graph and returns the popped LiPD object
        
        Parameters
        ----------
        dsnames : str or list of str
            dataset name(s) to be popped.
        
        Returns
        -------

        pylipd.lipd.LiPD
            LiPD object with the popped dataset(s)

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

        dsnames = [dsnames] if type(dsnames) is not list else dsnames
        dsids = [(f"{NSURL}/{dsname}" if not dsname.startswith(NSURL) else dsname) for dsname in dsnames]
        popped = super().pop(dsids)
        return LiPD(popped.graph)

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
        
        dsnames = [dsnames] if type(dsnames) is not list else dsnames
        dsids = [(f"{NSURL}/{dsname}" if not dsname.startswith(NSURL) else dsname) for dsname in dsnames]

        super().remove(dsids)


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


    def get_ensemble_tables(self, dsname = None, ensembleVarName = None, ensembleDepthVarName = 'depth'):
        '''Gets ensemble tables from the LiPD graph

        Parameters
        ----------

        dsname : str
            The name of the dataset if you wish to analyse one at a time (Set to ".*" to match all datasets with a common root)
        ensembleVarName : None or str
            ensemble variable name. Default is None, which searches for names that contain "year" or "age" (Set to ".*" to match all ensemble variable names)
        ensembleDepthVarName : str
            ensemble depth variable name. Default is 'depth' (Set to ".*" to match all ensemble depth variable names)

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
                ensembleVarName="age",
                ensembleDepthVarName="depth"
            )
            print("Ensemble tables:")
            print(ens_df)
        '''
        
        if dsname is None:
            dsname = ''
        
        if ensembleVarName is None:
            query = QUERY_ENSEMBLE_TABLE_SHORT
            query = query.replace("[dsname]", dsname)
            query = query.replace("[ensembleDepthVarName]", ensembleDepthVarName)
        
        else:
       
            query = QUERY_ENSEMBLE_TABLE
            query = query.replace("[dsname]", dsname)
            query = query.replace("[ensembleVarName]", ensembleVarName)
            query = query.replace("[ensembleDepthVarName]", ensembleDepthVarName)

        qres, qres_df = self.query(query)
        return qres_df


    def get_all_variables(self):
        '''
        Returns a list of all variables in the graph
        
        Returns
        -------

        pandas.DataFrame
            A dataframe of all variables in the graph with columns uri, varid, varname

        '''
        return self.query(QUERY_VARIABLE)[1]


    def to_lipd_series(self, parallel=False):
        '''
        Converts the LiPD object to a LiPDSeries object

        Parameters
        ----------
        parallel : bool
            Whether to use parallel processing to load the data. Default is False

        Returns
        -------
        pylipd.lipd.LiPDSeries
            A LiPDSeries object

        '''
        S = LiPDSeries()    
        S.load(self, parallel)
        return S


    # bbox = left,bottom,right,top
    # bbox = min Longitude , min Latitude , max Longitude , max Latitude 
    def filter_by_geo_bbox(self, lonMin, latMin, lonMax, latMax):
        '''
        Filters datasets to return a new LiPD object that only keeps datasets that fall within the bounding box

        Parameters
        ----------
        lonMin : float
            Minimum longitude

        latMin : float
            Minimum latitude
        
        lonMax : float
            Maximum longitude

        latMax : float
            Maximum latitude

        Returns
        -------

        pylipd.lipd.LiPD
            A new LiPD object that only contains datasets that fall within the bounding box

        '''
        query = QUERY_FILTER_GEO
        query = query.replace("[lonMin]", str(lonMin))
        query = query.replace("[latMin]", str(latMin))
        query = query.replace("[lonMax]", str(lonMax))               
        query = query.replace("[latMax]", str(latMax))
        qres, qres_df = self.query(query)
        dsnames = [sanitizeId(row.dsname) for row in qres]
        return self.get(dsnames)


    def filter_by_archive_type(self, archiveType):
        '''
        Filters datasets to return a new LiPD object that only keeps datasets that have the specified archive type

        Parameters
        ----------

        archiveType : str
            The archive type to filter by

        Returns
        -------
        
        pylipd.lipd.LiPD
            A new LiPD object that only contains datasets that have the specified archive type (regex)

        '''
        query = QUERY_FILTER_ARCHIVE_TYPE
        query = query.replace("[archiveType]", archiveType)
        qres, qres_df = self.query(query)
        dsnames = [sanitizeId(row.dsname) for row in qres]
        return self.get(dsnames)
