from tqdm import tqdm
from .globals.queries import QUERY_FILTER_VARIABLE_NAME, QUERY_VARIABLE, QUERY_DISTINCT_VARIABLE, QUERY_VARIABLE_ESSENTIALS, QUERY_DISTINCT_PROXY, QUERY_FILTER_VARIABLE_PROXY, QUERY_FILTER_VARIABLE_RESOLUTION, QUERY_LiPDSERIES_PROPERTIES
from .utils.multi_processing import multi_load_lipd_series
from .utils.rdf_graph import RDFGraph

import numpy as np
import json

class LiPDSeries(RDFGraph):
    '''The LiPD Series class describes a collection of `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ 
    variables. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of  LiPD variables into an RDF graph containing terms from 
    the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`. Each LiPD Variable is also associated with the LiPD itself
    so it can be deserialized into the original LiPD format.
    How to browse and query the LiPD variables is described in a short example below.

    Examples
    --------
    In this example, we read an online LiPD file and convert it into a time series object dictionary.

    .. jupyter-execute::

        from pylipd.lipd_series import LiPDSeries

        lipd = LiPD()
        lipd.load(["https://lipdverse.org/data/LCf20b99dfe8d78840ca60dfb1f832b9ec/1_0_1//Nunalleq.Ledger.2018.lpd"])
        lipd_series = lipd.to_lipd_series()
    '''
    def __init__(self, graph=None):
        super().__init__(graph)
        self.lipds = {}


    def load(self, lipd, parallel=False):
        '''Extract Variables from the LiPD object.

        Parameters
        ----------
        lipd : LiPD
            A LiPD object
        
               
        Examples
        --------
        .. jupyter-execute::

            from pylipd.lipd_series import LiPDSeries

            lipd = LiPD()
            lipd.load(["https://lipdverse.org/data/LCf20b99dfe8d78840ca60dfb1f832b9ec/1_0_1//Nunalleq.Ledger.2018.lpd"])
            lipd_series = lipd.to_lipd_series()
        '''

        print(f"Creating LiPD Series...")

        # Update graph (Create contexts for each variable)
        print("- Extracting dataset subgraphs")
        total = len(lipd.get_all_dataset_names())
        for ctx in tqdm(lipd.graph.contexts(), total=total):
            ctxid = str(ctx.identifier)
            self.lipds[ctxid] = lipd.get(ctxid)
                    
        multi_load_lipd_series(self.graph, self.lipds, parallel)
        
        print("Done..")


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

            from pylipd.utils.dataset import load_dir

            lipd = load_dir()
            S = lipd.to_lipd_series()
            df = S.get_all_variables()
            
            print(df)
        
        
        '''        
        return self.query(QUERY_VARIABLE)[1]
    
    def get_all_variable_names(self):
        
        """
        Get a list of all possible distinct variableNames. Useful for filtering and querying. 

        Returns
        -------
        list
            A list of unique variableName 
        
        Examples
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir
            lipd = load_dir('Pages2k')
            S = lipd.to_lipd_series()
            varName = S.get_all_variable_names()
            print(varName)
        """

        return self.query(QUERY_DISTINCT_VARIABLE)[1].iloc[:,0].values.tolist()
    
    def get_all_proxy(self):
        
        """
        Get a list of all possible proxy. Useful for filtering and querying. 

        Returns
        -------
        list
            A list of unique proxies
        
        Examples
        --------
        
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir
            lipd = load_dir('Pages2k')
            S = lipd.to_lipd_series()
            proxyName = S.get_all_proxy()
            print(proxyName)
        """
        
        return self.query(QUERY_DISTINCT_PROXY)[1].iloc[:,0].values.tolist()

    def get_timeseries_essentials(self):
        '''This function returns information about each variable: `dataSetName`, `archiveType`, `name`, `values`, `units`, `TSID`, `proxy`.

        Returns
        -------
        qres_df : pandas.DataFrame
            A dataframe containing the information in each column
        
        Examples
        --------
        
        .. jupyter-execute::

            from pylipd.utils.dataset import load_dir

            lipd = load_dir()
            S = lipd.to_lipd_series()
            df = S.get_timeseries_essentials()
            
            print(df)

        '''
        
    
        query = QUERY_VARIABLE_ESSENTIALS
        qres, qres_df = self.query(query)
        
        #fix the dataframe
        for _,row in qres_df.iterrows():
            string = row['dataSetName'].split('/')[-1]
            row['dataSetName'] = string
        
        qres_df['values']=qres_df['values'].apply(lambda row : np.array(json.loads(row)))

        return qres_df
    
    def get_variable_properties(self):
        """
        Get a list of all the properties name associated with the dataset. Useful to write custom queries

        Returns
        -------
        clean_list : list
            A list of unique variable properties
        
        Examples
        --------
        
        .. jupyter-execute::

            from pylipd.utils.dataset import load_dir

            lipd = load_dir()
            S = lipd.to_lipd_series()
            l = S.get_variable_properties()
            
            print(l)


        """
        
        query_list = self.query(QUERY_LiPDSERIES_PROPERTIES)[1].iloc[:,0].values.tolist()
        clean_list = [item.split("#")[-1] for item in query_list]
        
        return clean_list
    

    def filter_by_name(self, name):
        '''
        Filters series to return a new LiPDSeries that only keeps variables that have the specified name (regex)

        Parameters
        ----------

        name : str
            The variable name to filter by

        Returns
        -------
        
        pylipd.lipd_series.LiPDSeries
            A new LiPDSeries object that only contains variables that have the specified name (regex)
        
        Examples
        --------
        
        .. jupyter-execute::

            from pylipd.utils.dataset import load_datasets
            lipd = load_datasets('ODP846.Lawrence.2006.lpd')
            S = lipd.to_lipd_series()
            sst = S.filter_by_name('sst')
            
            print(sst.get_all_variable_names())

        '''
        query = QUERY_FILTER_VARIABLE_NAME
        query = query.replace("[name]", name)

        qres, qres_df = self.query(query)
        varuris = [str(row.uri) for row in qres]
        dsuris = [*set([str(row.dsuri) for row in qres])]

        #print(len(dsuris))

        rdfgraph = self.get(varuris)
        S = LiPDSeries(rdfgraph.graph)
        S.lipds = {k: self.lipds[k].copy() for k in dsuris}
        return S

    def filter_by_proxy(self, proxy):
        '''
        Filters series to return a new LiPDSeries that only keeps variables that have the specified proxy (regex)
    
        Parameters
        ----------
    
        proxy : str
            The name of the proxy to filter by
    
        Returns
        -------
        
        pylipd.lipd_series.LiPDSeries
            A new LiPDSeries object that only contains variables that have the specified name (regex)
        
        Examples
        --------
        
        .. jupyter-execute::
    
            from pylipd.utils.dataset import load_dir
            lipd = load_dir('Pages2k')
            S = lipd.to_lipd_series()
            S_filtered = S.filter_by_proxy('ring width')
            print(S_filtered.get_all_proxy())
    
        '''
        query = QUERY_FILTER_VARIABLE_PROXY
        query = query.replace("[proxy]", proxy)
    
        qres, qres_df = self.query(query)
        varuris = [str(row.uri) for row in qres]
        dsuris = [*set([str(row.dsuri) for row in qres])]
    
        rdfgraph = self.get(varuris)
        S = LiPDSeries(rdfgraph.graph)
        S.lipds = {k: self.lipds[k].copy() for k in dsuris}
        return S
    
    def filter_by_resolution(self, threshold, stats='Mean'):
        '''
        Filters series to return a new LiPDSeries that only keeps variables that have a resolution less than the specified threshold. 

        Parameters
        ----------
        threshold : float
            The maximum resolution to keep
        stats : str, optional
            Whether to use 'Mean', 'Median', 'Min' or 'Max' resolution. The default is 'Mean'.

        Raises
        ------
        ValueError
            Make sure that the stats is of ['Mean','Median', 'Min', 'Max'].

        Returns
        -------
        S : pylipd.lipd_series.LiPDSeries
            A new LiPDSeries object that only contains the filtered variables
        
        Examples
        --------
        
        .. jupyter-execute::
    
            from pylipd.utils.dataset import load_dir
            lipd = load_dir('Pages2k')
            S = lipd.to_lipd_series()
            S_filtered = S.filter_by_resolution(10)

        '''
        
        stats = stats.capitalize() #make sure that the first letter is capitalized
        stats_allowed = ['Mean','Median', 'Min', 'Max'] #possible values
        if stats not in stats_allowed:
            raise ValueError("Stats must be ['Mean','Median', 'Min', 'Max']")
        
        threshold = float(threshold) # make sure this is a float or can be coerced in one
        
        query = QUERY_FILTER_VARIABLE_RESOLUTION
        query = query.replace("[value]", str(threshold))
        query = query.replace("[stat]", stats)

        qres,q_df = self.query(query)
        
        varuris = [str(row.uri) for row in qres]
        dsuris = [*set([str(row.dsuri) for row in qres])]
    
        rdfgraph = self.get(varuris)
        S = LiPDSeries(rdfgraph.graph)
        S.lipds = {k: self.lipds[k].copy() for k in dsuris}
        return S