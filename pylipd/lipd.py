"""
The LiPD class describes a `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ object. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of the LiPD data into an RDF graph containing terms from the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`
How to browse and query LiPD objects is described in a short example below, while `this notebook <https://nbviewer.jupyter.org/github/LinkedEarth/pylipd/blob/master/example_notebooks/pylipd_tutorial.ipynb>`_ demonstrates how to use PyLiPD to view and query LiPD datasets.
"""

import ast
import os
import re
import os.path
import tempfile
import pandas as pd
import random
import string
import io
import numpy as np
import json
import uuid

from pylipd.classes.dataset import Dataset

from pylipd.utils.json_to_rdf import JSONToRDF
from pylipd.utils.rdf_to_json import RDFToJSON

from .globals.queries import QUERY_FILTER_TIME, QUERY_BIBLIO, QUERY_DSID, QUERY_DSNAME, QUERY_ENSEMBLE_TABLE, QUERY_ENSEMBLE_TABLE_SHORT, QUERY_FILTER_ARCHIVE_TYPE, QUERY_FILTER_GEO, QUERY_VARIABLE, QUERY_VARIABLE_GRAPH, QUERY_UNIQUE_ARCHIVE_TYPE, QUERY_TIMESERIES_ESSENTIALS_CHRON, QUERY_TIMESERIES_ESSENTIALS_PALEO, QUERY_DISTINCT_VARIABLE, QUERY_DATASET_PROPERTIES, QUERY_VARIABLE_PROPERTIES, QUERY_MODEL_PROPERTIES, QUERY_LOCATION, QUERY_FILTER_DATASET_NAME, QUERY_FILTER_COMPILATION, QUERY_COMPILATION_NAME

from .lipd_series import LiPDSeries
from .utils.multi_processing import multi_convert_to_rdf, multi_load_lipd
from .utils.rdf_graph import RDFGraph

from .utils.rdf_to_lipd import RDFToLiPD
from .utils.legacy_utils import LiPD_Legacy
from .utils.utils import sanitizeId

#import bibtexparser
#from bibtexparser.bibdatabase import BibDatabase
from doi2bib import crossref
from pybtex.database import BibliographyData, Entry

from .globals.urls import NSURL, DEFAULT_GRAPH_URI

class LiPD(RDFGraph):
    '''The LiPD class describes a `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ object. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of the LiPD data into an RDF graph containing terms from the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`
    How to browse and query LiPD objects is described in a short example below.

    Examples
    --------
    In this example, we read an online LiPD file and convert it into a time series object dictionary.

    .. jupyter-execute::
        
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

    
    def load_from_dir(self, dir_path, parallel=False, cutoff=None, standardize=True, add_labels=True):
        '''Load LiPD files from a directory
       
        Parameters
        ----------

        dir_path : str
            path to the directory containing lipd files

        parallel: bool
            (Optional) set to True to process lipd files in parallel. You *must* run this function under the "__main__" process for this to work
        
        cutoff : int
            (Optional) the maximum number of files to load at once.
            
        Examples
        --------
        In this example, we load LiPD files from a directory.

        .. jupyter-execute::
            
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
        self.load(lipdfiles, parallel, standardize, add_labels)


    # Allows loading http locations
    def load(self, lipdfiles, parallel=False, standardize=True, add_labels=True):
        '''Load LiPD files. 
        

        Parameters
        ----------

        lipdfiles : list of str
            array of paths to lipd files (the paths could also be urls)

        parallel: bool
            (Optional) set to True to process lipd files in parallel. You *must* run this function under the "__main__" process for this to work


        Examples
        --------
        In this example, we load LiPD files for an array of paths.

        .. jupyter-execute::

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
        self.graph = multi_load_lipd(self.graph, lipdfiles, parallel, standardize, add_labels)
        print("Loaded..")
    
    #def load_from_lipdverse(self, datasetID, version=None):
        


    def convert_lipd_dir_to_rdf(self, lipd_dir, rdf_file, parallel=False, standardize=True, add_labels=False):
        '''Convert a directory containing LiPD files into a single RDF file (to be used for uploading to Knowledge Bases like GraphDB)

        Parameters
        ----------

        lipd_dir : str
            Path to the directory containing lipd files

        rdf_file : str
            Path to the output rdf file

        '''

        filemap = {}
        for path in os.listdir(lipd_dir):
            fullpath = os.path.join(lipd_dir, path)
            tmp_rdf_file = tempfile.NamedTemporaryFile().name
            filemap[fullpath] = tmp_rdf_file
        
        print(f"Converting {len(filemap.keys())} LiPD files to RDF..")

        multi_convert_to_rdf(filemap, parallel, standardize, add_labels)
        
        print("Conversion to RDF done..")

        print("Writing to main RDF file..")
        with open(rdf_file, "w") as fout:
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


    def load_remote_datasets(self, dsnames, load_default_graph=True):
        '''Loads remote datasets into cache if a remote endpoint is set

        Parameters
        ----------

        dsnames : array
            array of dataset names

        Examples
        --------

        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd_remote = LiPD()
            lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic")
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

        if load_default_graph:
            dsnamestr += f" <{DEFAULT_GRAPH_URI}>"
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
        
        df : pandas.DataFrame
            Bibliography information in a Pandas DataFrame
        
        Examples
        --------    
        
        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            print(lipd.get_bibtex(save=False))
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
                        print(f"Cannot find a matching record for the provided DOI ({row['doi']}), creating the entry manually")
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

    def get_timeseries(self, dsnames, to_dataframe=False, mode="paleo", time="age"):
        '''Get Legacy LiPD like Time Series Object (tso)
        
        This function is meant to provide legacy support to the older version of the LiPD utilities, which retruns a dictionary ot timeseries objects. The function also supports returning to a pandas.DataFrame, essentially flattening all the information. This is useful to explore all possible properties but can be slow for large number of datasets or if you only require some standard information. In this case, use `get_timeseries_essentials`. 

        Parameters
        ----------

        dsnames : list
            array of dataset id or name strings
        
        to_dataframe : bool {True; False}
            Whether to return a dataframe along the dictionary. Default is False
        
        mode: 'paleo' or 'chron'
            Whether to return information from the PaleoData or ChronData objects
        
        time: 'age' or 'year'
            Whether the time is expressed as year or age
        
        Returns
        -------
        
        ts : dict
            A dictionary containing Time Series Object
            
        df : Pandas.DataFrame
            If to_dataframe is set to True, returns a queriable Pandas DataFrame

        Examples
        --------
        
        To only return a list of timeseries objects

        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Fetch LiPD data from remote RDF Graph
            lipd_remote = LiPD()
            lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic")
            ts_list = lipd_remote.get_timeseries(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
            for dsname, tsos in ts_list.items():
                for tso in tsos:
                    if 'paleoData_variableName' in tso:
                        print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])
        
        
        To return a dataframe in addition to the list of timeseries objects
        
        
        .. jupyter-execute::
            
            from pylipd.lipd import LiPD
            
            lipd_remote = LiPD()
            lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic")
            ts_list, df = lipd_remote.get_timeseries(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"], to_dataframe = True)
            df.head()
        
        See also
        --------
        
        pylipd.lipd.LiPD.get_timeseries_essentials
        
        '''
        
        if type(dsnames)==str:
            dsnames=[dsnames]
        
        ts = self._get_timeseries(dsnames, mode=mode, time=time)
        if to_dataframe == False:
            return ts
        elif to_dataframe == True:
            dict_list =[]

            for item in ts.keys():
                for dictionary in ts[item]:
                    dict_list.append(dictionary)

            df = pd.DataFrame.from_dict(dict_list, orient='columns')
            
            return ts, df

    def _get_timeseries(self, dsnames, mode="paleo", time="age"):
        timeseries = {}
        for dsname in dsnames:
            converter = RDFToLiPD(self.graph)
            d = converter.convert_to_json(dsname)
            print("Extracting timeseries from dataset: " + dsname + " ...")
            if len(d.items()):
                tss = LiPD_Legacy().extract(d, mode=mode, time=time)
                timeseries[dsname] = tss
        return timeseries
    
    def get_timeseries_essentials(self, dsnames=None, mode='paleo'):
        ''' Returns specific properties for timeseries: 'dataSetName', 'archiveType', 'geo_meanLat', 'geo_meanLon',
               'geo_meanElev', 'paleoData_variableName', 'paleoData_values',
               'paleoData_units', 'paleoData_proxy' (paleo only), 'paleoData_proxyGeneral' (paleo only),
               'time_variableName', 'time_values', 'time_units', 'depth_variableName',
               'depth_values', 'depth_units'
        

        Parameters
        ----------
        dsnames : list
            array of dataset id or name strings        
        mode : paleo, chron
            Whether to retrun the information stored in the PaleoMeasurementTable or the ChronMeasurementTable. The default is 'paleo'.

        Raises
        ------
        ValueError
            Need to select either 'chron' or 'paleo'

        Returns
        -------
        qres_df : pandas.DataFrame
            A pandas dataframe returning the properties in columns for each series stored in a row of the dataframe

        Example
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_datasets
            lipd = load_datasets('ODP846.Lawrence.2006.lpd')
            df_paleo = lipd.get_timeseries_essentials(mode='paleo')
            print(df_paleo)
        
        To return the information stored in the ChronTable:
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_datasets
            lipd = load_datasets('ODP846.Lawrence.2006.lpd')  
            df_chron = lipd.get_timeseries_essentials(mode='chron')
            print(df_chron)
    
        '''
        
        if dsnames is None:
            dsnames= ''
        if type(dsnames)==str:
            dsnames=[dsnames]            
        
        qres_df = None
        for dsname in dsnames:
            if mode == 'paleo':
                query = QUERY_TIMESERIES_ESSENTIALS_PALEO
                query = query.replace("[dsname]", dsname)
            elif mode == 'chron':
                query = QUERY_TIMESERIES_ESSENTIALS_CHRON
                query = query.replace("[dsname]", dsname)
            else:
                raise ValueError("The mode should be either 'paleo' or 'chron'")
        
            qres, qtmp_df = self.query(query)
            
            try:
                qtmp_df['paleoData_values']=qtmp_df['paleoData_values'].apply(lambda row : np.array(json.loads(row)))
            except:
                qtmp_df['chronData_values']=qtmp_df['chronData_values'].apply(lambda row : np.array(json.loads(row)))
            
            
            qtmp_df['time_values']=qtmp_df['time_values'].apply(lambda x : np.array(json.loads(x)) if x is not None else None)
            qtmp_df['depth_values']=qtmp_df['depth_values'].apply(lambda x : np.array(json.loads(x)) if x is not None else None)
            if qres_df is None:
                qres_df = qtmp_df
            else:
                qres_df = pd.concat([qres_df, qtmp_df], ignore_index=True)
        
        
        return qres_df
            

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

        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Load a local LiPD file
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

        .. jupyter-execute::


            from pylipd.lipd import LiPD

            # Load a local file
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
        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Load LiPD files from a local directory
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
        .. jupyter-execute::


            from pylipd.lipd import LiPD

            # Load local files
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
        .. jupyter-execute::


            from pylipd.lipd import LiPD
            
            # Load local files
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

        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Load local files
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

        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Load local files
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            print(lipd.get_all_dataset_ids())
        '''
        qres, qres_df = self.query(QUERY_DSID)
        return [sanitizeId(row.dsid) for row in qres]
    
    def get_all_archiveTypes(self):
        '''
        Returns a list of all the unique archiveTypes present in the LiPD object

        Returns
        -------
        list
            A list of archiveTypes
            
        Examples
        --------
        
        .. jupyter-execute::

            from pylipd.lipd import LiPD

            # Load Local files
            lipd = LiPD()
            lipd.load([
                "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
                "../examples/data/MD98_2181.Stott.2007.lpd"
            ])
            print(lipd.get_all_archiveTypes())

        '''
        
        qres, qres_df = self.query(QUERY_UNIQUE_ARCHIVE_TYPE)
        return [str(row.archiveType) for row in qres]
        
    def get_all_locations(self, dsname = None):
        '''Return geographical coordinates for all the datasets.       

        Parameters
        ----------
        dsname : str, optional
            The name of the dataset for which to return the timeseries information. The default is None.

        Returns
        -------
        df : pandas.DataFrame
            A pandas dataframe returning the latitude, longitude and elevation for each dataset
        
        Examples
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir
            lipd = load_dir('Pages2k')
            df = lipd.get_all_locations()
            print(df)

        '''
        
        if dsname is None:
            dsname= ''
        
        query = QUERY_LOCATION
        query = query.replace("[dsname]", dsname)
            
                
        return self.query(query)[1]
    
    def get_all_compilation_names(self):
        '''Return the names of the compilation present in the LiPD object     

        Returns
        -------
        l : list
            A list returning the names of the available compilations.
        
        Examples
        --------
        
        .. jupyter-execute::
        
            from pylipd.utils.dataset import load_dir
            
            lipd = load_dir('Temp12k')
            df = lipd.get_all_compilation_names()
            print(df)

        '''
        
        qres, qres_df = self.query(QUERY_COMPILATION_NAME)
        return [sanitizeId(row.compilationName) for row in qres]


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

        .. jupyter-execute::

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

        nan_replace = re.compile(re.escape('NaN'), re.IGNORECASE)

        qres_df['ensembleDepthValues']=qres_df['ensembleDepthValues'].apply(lambda row : np.array(json.loads(row)))
        qres_df['ensembleVariableValues']=qres_df['ensembleVariableValues'].apply(lambda row : np.array(ast.literal_eval(nan_replace.sub('None', row))))
        
        return qres_df


    def get_all_variables(self):
        '''
        Returns a list of all variables in the graph
        
        Returns
        -------

        pandas.DataFrame
            A dataframe of all variables in the graph with columns uri, varid, varname
            
        Examples
        --------
        
        .. jupyter-execute::

            from pylipd.lipd import LiPD

            lipd = LiPD()
            lipd.load([
                "../examples/data/ODP846.Lawrence.2006.lpd"
            ])
            
            df = lipd.get_all_variables()
            print(df)

        '''
        return self.query(QUERY_VARIABLE)[1]

    def get_all_variable_names(self):
        """
        Get a list of all possible distinct variableNames. Useful for filtering and qeurying. 

        Returns
        -------
        list
            A list of unique variableName 
        
        Examples
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir
            lipd = load_dir('Pages2k')
            varName = lipd.get_all_variable_names()
            print(varName)
        

        """
        
        return self.query(QUERY_DISTINCT_VARIABLE)[1].iloc[:,0].values.tolist()
    
    def get_dataset_properties(self):
        """Get a list of unique properties attached to a dataset. 
        
        Note: Some properties will return another object (e.g., 'publishedIn' will give you a Publication object with its own properties)
        Note: Not all datasets will have the same available properties (i.e., not filled in by a user)
        

        Returns
        -------
        clean_list : list
            A list of avialable properties that can queried

        Examples
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir
            lipd = load_dir(name='Pages2k')
            dataset_properties = lipd.get_dataset_properties()
            print(dataset_properties)
        """
        
        query_list = self.query(QUERY_DATASET_PROPERTIES)[1].iloc[:,0].values.tolist()
        clean_list = [item.split("#")[-1] for item in query_list]
        
        return clean_list
    
    def get_variable_properties(self):
        '''Get a list of variable properties that can be used for querying
        

        Returns
        -------
        list
            A list of unique variable properties
        
        Examples
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir
            lipd = load_dir(name='Pages2k')
            variable_properties = lipd.get_variable_properties()
            print(variable_properties)

        '''
        
        query_list = self.query(QUERY_VARIABLE_PROPERTIES)[1].iloc[:,0].values.tolist()
        clean_list = [item.split("#")[-1] for item in query_list]
        
        return clean_list
    
    def get_model_properties(self):
        '''Get all the properties associated with a model
        

        Returns
        -------
        List
            A list of unique properties attached to models
        
        Examples
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_datasets
            lipd = load_datasets(names='ODP846')
            model_properties = lipd.get_model_properties()
            print(model_properties)


        '''
        
        query_list = self.query(QUERY_MODEL_PROPERTIES)[1].iloc[:,0].values.tolist()
        clean_list = [item.split("#")[-1] for item in query_list]
        
        return clean_list

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
            
        Examples
        --------
        
        .. jupyter-execute::

            from pylipd.lipd import LiPD

            lipd = LiPD()
            lipd.load([
                "../examples/data/ODP846.Lawrence.2006.lpd"
            ])
            
            S = lipd.to_lipd_series()
        
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
        
        Examples
        --------
        
        pyLipd ships with existing datasets that can be loaded directly through the package. Let's load the Pages2k sample datasets using this method.
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir

            lipd = load_dir()
            Lfiltered = lipd.filter_by_geo_bbox(0,25,50,50)
            Lfiltered.get_all_dataset_names()           
        
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
        
        Examples
        --------
        
        pyLipd ships with existing datasets that can be loaded directly through the package. Let's load the Pages2k sample datasets using this method.
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir

            lipd = load_dir('Pages2k')
            Lfiltered = lipd.filter_by_archive_type('marine')
            Lfiltered.get_all_archiveTypes()
        
        If searching for multiple archiveTypes, you can construct the name as follows:
        
        .. jupyter-execute::

            from pylipd.utils.dataset import load_dir

            lipd = load_dir('Pages2k')
            Lfiltered = lipd.filter_by_archive_type('marine|coral')
            Lfiltered.get_all_archiveTypes()
        
        '''
        
        query = QUERY_FILTER_ARCHIVE_TYPE
        query = query.replace("[archiveType]", archiveType)
        qres, qres_df = self.query(query)
        dsnames = [sanitizeId(row.dsname) for row in qres]
        return self.get(dsnames)

    
    def filter_by_datasetName(self, datasetName):
        '''
        Filters datasets to return a new LiPD object that only keeps datasets that have the specified names

        Parameters
        ----------

        datasetName : str 
            The datasetNames to filter by

        Returns
        -------
        
        pylipd.lipd.LiPD
            A new LiPD object that only contains datasets that have the specified archive type (regex)
        
        Examples
        --------
        
        pyLipd ships with existing datasets that can be loaded directly through the package. Let's load the Pages2k sample datasets using this method.
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir

            lipd = load_dir('Pages2k')
            Lfiltered = lipd.filter_by_datasetName('Ocn-RedSea.Felis.2000')
            Lfiltered.get_all_dataset_names()
        
        If searching for multiple dataset names, you can construct the name as follows:
        
        .. jupyter-execute::
        
            from pylipd.utils.dataset import load_dir

            lipd = load_dir('Pages2k')
            dsnames = ['Ocn-RedSea.Felis.2000','Ant-WAIS-Divide.Severinghaus.2012']
            dsquery = '|'.join(dsnames)
            Lfiltered = lipd.filter_by_datasetName(dsquery)
            Lfiltered.get_all_dataset_names()
            
        '''
        
        query = QUERY_FILTER_DATASET_NAME
        query = query.replace("[datasetName]", datasetName)
        qres, qres_df = self.query(query)
        dsnames = [sanitizeId(row.dsname) for row in qres]
        return self.get(dsnames)
    
    def filter_by_compilationName(self, compilationName):
        '''
        Filters datasets to return a new LiPD object that only keeps datasets that have the specific compilation

        Parameters
        ----------

        compilationName : str 
            The name of the compilation to filter by

        Returns
        -------
        
        pylipd.lipd.LiPD
            A new LiPD object that only contains datasets that have the specified archive type (regex)
        
        Examples
        --------
        
        pyLipd ships with existing datasets that can be loaded directly through the package. Let's load the Pages2k sample datasets using this method.
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import available_dataset_names, load_datasets

            dsList = available_dataset_names()
            D = load_datasets(dsList)
            Dfiltered = D.filter_by_compilationName('Temp12k')
            Dfiltered.get_all_dataset_names()
        
        '''
        
        query = QUERY_FILTER_COMPILATION
        query = query.replace("[compilationName]", compilationName)
        qres, qres_df = self.query(query)
        dsnames = [sanitizeId(row.dataSetName) for row in qres]
        return self.get(dsnames)
        
    
    def filter_by_time(self,timeBound, timeBoundType = 'any', recordLength = None):
        """
        Filter the records according to a specified time interval and the length of the record within that interval. Note that this function assumes that all records use the same time representation. 
        
        If you are unsure about the time representation, you may need to use `.get_timeseries_essentials`. 

        Parameters
        ----------
        timeBound : list
            Minimum and Maximum age value to search for.
        timeBoundType : str, optional
            The type of querying to perform. Possible values include: "any", "entire", and "entirely".
            - any: Overlap any portions of matching datasets (default)
            - entirely: are entirely overlapped by matching datasets
            - entire: overlap entire matching datasets but dataset can be shorter than the bounds
            The default is 'any'.
        recordLength : float, optional
            The minimum length the record needs to have while matching the ageBound criteria. The default is None.

        Raises
        ------
        ValueError
            timeBoundType must take the values in ["any", "entire", and "entirely"]

        Returns
        -------
        pylipd.lipd.LiPD
            A new LiPD object that only contains datasets that have the specified time interval
            
        Examples
        --------
        pyLipd ships with existing datasets that can be loaded directly through the package. Let's load the Pages2k sample datasets using this method.
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir

            lipd = load_dir('Pages2k')
            Lfiltered = lipd.filter_by_time(timeBound=[0,1800])
            Lfiltered.get_all_dataset_names()

        """
        
        if timeBound and timeBound[0]>timeBound[1]:
                timeBound = [timeBound[1],timeBound[0]]

        timeBoundType=timeBoundType.lower()

        query = QUERY_FILTER_TIME
        __, df = self.query(query)
        if recordLength is None:
            if timeBoundType == 'entirely':
                filter_df = df[(df['minage'] <= timeBound[0]) & (df['maxage'] >= timeBound[1])]
            elif timeBoundType == 'entire':
                filter_df = df[(df['minage'] >= timeBound[0]) & (df['maxage'] <= timeBound[1])]
            elif timeBoundType == 'any':
                filter_df = df[(df['minage'] <= timeBound[1])]
            else:
                raise ValueError("timeBoundType must be in ['any', 'entirely','entire']")
        else:
            if timeBoundType == 'entirely':
                filter_df = df[(df['minage'] <= timeBound[0]) & (df['maxage'] >= timeBound[1]) & (np.abs(df['maxage']-df['minage'])>=recordLength)]
            elif timeBoundType == 'entire':
                filter_df = df[(df['minage'] >= timeBound[0]) & (df['maxage'] <= timeBound[1]) & (np.abs(df['maxage']-df['minage'])>=recordLength)]
            elif timeBoundType == 'any':
                filter_df = df[(df['minage'] <= timeBound[1]) & (np.abs(df['minage']-timeBound[1])>=recordLength)]
            else:
                raise ValueError("timeBoundType must be in ['any', 'entirely','entire']")
            
        dsnames = list(filter_df['dsname'])
        return self.get(dsnames)
    
    
    def get_datasets(self) -> 'list[Dataset]':
        '''
        Return datasets as instances of the Dataset class

        Parameters
        ----------

        Returns
        -------
        
        list of pylipd.classes.Dataset
            A list of Dataset objects
        
        Examples
        --------
        
        pyLipd ships with existing datasets that can be loaded directly through the package. Let's load the Pages2k sample datasets using this method.
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir

            lipd = load_dir('Pages2k')
            lipd.get_datasets()
        
        '''        
        datasets: list[Dataset] = []
        for dsname in self.get_all_dataset_names():
            dsuri = NSURL + "/" + dsname
            r2j = RDFToJSON(dsuri, self.graph)
            data = json.loads(r2j.to_json())
            ds = Dataset.from_data(dsuri, data)
            datasets.append(ds)
        return datasets
    

    def _generate_unique_id(self, prefix='PYD'):
        # Generate a random UUID
        random_uuid = uuid.uuid4()  # Generates a random UUID.
        
        # Convert UUID format to the specific format we need
        # UUID is usually in the form '1e2a2846-2048-480b-9ec6-674daef472bd' so we slice and insert accordingly
        id_str = str(random_uuid)
        formatted_id = f"{prefix}-{id_str[:5]}-{id_str[9:13]}-{id_str[14:18]}-{id_str[19:23]}-{id_str[24:28]}"
        
        return formatted_id

    def _fix_missing_ids(self, ds: Dataset):
        # Assign variable ids if not present
        # Assign datatable csv file name if not present
        pd_counter = 0
        for pd in ds.getPaleoData():
            table_counter = 0
            for table in pd.getMeasurementTables():
                if not table.getFileName():
                    table.setFileName(f"paleo{pd_counter}measurement{table_counter}.csv")
                for v in table.getVariables():
                    if not v.getVariableId():
                        v.setVariableId(self._generate_unique_id(prefix='TS'))
                table_counter += 1
            pd_counter += 1

        chron_counter = 0
        for chron in ds.getChronData():
            table_counter = 0
            for table in chron.getMeasurementTables():
                if not table.getFileName():
                    table.setFileName(f"chron{chron_counter}measurement{table_counter}.csv")
                for v in table.getVariables():
                    if not v.getVariableId():
                        v.setVariableId(self._generate_unique_id(prefix='TS'))
                table_counter += 1

            model_counter = 0
            for model in chron.getModeledBy():
                table_counter = 0
                for table in model.getEnsembleTables():
                    if not table.getFileName():
                        table.setFileName(f"chron{chron_counter}model{model_counter}ensemble{table_counter}.csv")
                    for v in table.getVariables():
                        if not v.getVariableId():
                            v.setVariableId(self._generate_unique_id(prefix='TS'))
                    table_counter += 1
                model_counter += 1
            chron_counter += 1        


    def load_datasets(self, datasets: 'list[Dataset]'):
        '''
        Loads instances of Dataset class into the LiPD graph

        Parameters
        ----------
        list of pylipd.classes.Dataset
            A list of Dataset objects

        Examples
        --------
        
        pyLipd ships with existing datasets that can be loaded directly through the package. Let's load the Pages2k sample datasets using this method.
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir

            lipd = load_dir('Pages2k')
            dses = lipd.get_datasets()

            # Modify the datasets if needed, then write them to the same, or another LiPD object

            lipd2 = LiPD()
            lipd2.load_datasets(dses)
        
        '''
        for ds in datasets:
            self._fix_missing_ids(ds)
            dsuri = ds.id
            j2r = JSONToRDF(self.graph, dsuri)
            j2r.load_data_in_graph(ds.to_data())
