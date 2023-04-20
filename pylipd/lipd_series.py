from rdflib import ConjunctiveGraph, Namespace, URIRef
from tqdm import tqdm
from pylipd.globals.queries import QUERY_FILTER_VARIABLE_NAME, QUERY_VARIABLE

from pylipd.globals.urls import ONTONS
from pylipd.multi_processing import multi_load_lipd_series
from pylipd.rdf_graph import RDFGraph
from pylipd.utils import sanitizeId


class LiPDSeries(RDFGraph):
    '''The LiPD Series class describes a collection of `LiPD (Linked Paleo Data) <https://cp.copernicus.org/articles/12/1093/2016/cp-12-1093-2016.html>`_ 
    variables. It contains an `RDF <https://www.w3.org/RDF/>`_ Graph which is serialization of  LiPD variables into an RDF graph containing terms from 
    the `LiPD Ontology <http://linked.earth/Ontology/release/core/1.2.0/index-en.html>`. Each LiPD Variable is also associated with the LiPD itself
    so it can be deserialized into the original LiPD format.
    How to browse and query the LiPD variables is described in a short example below.

    Examples
    --------
    In this example, we read an online LiPD file and convert it into a time series object dictionary.

    .. ipython:: python
        :okwarning:
        :okexcept:

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

        '''        
        return self.query(QUERY_VARIABLE)[1]


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

        '''
        query = QUERY_FILTER_VARIABLE_NAME
        query = query.replace("[name]", name)

        qres, qres_df = self.query(query)
        varuris = [str(row.uri) for row in qres]
        dsuris = [*set([str(row.dsuri) for row in qres])]

        print(len(dsuris))

        rdfgraph = self.get(varuris)
        S = LiPDSeries(rdfgraph.graph)
        S.lipds = {k: self.lipds[k].copy() for k in dsuris}
        return S