"""
The RDF Graph class contains an `RDF <https://www.w3.org/RDF/>`_ Graph using the RDFLib library, and allows querying over it using SPARQL. 
It also allows querying over a remote endpoint.
"""

from copy import deepcopy
import re
from rdflib import ConjunctiveGraph, Namespace, URIRef

from pylipd.globals.urls import ONTONS
from pylipd.utils import sparql_results_to_df

class RDFGraph:
    '''
    The RDF Graph class contains an `RDF <https://www.w3.org/RDF/>`_ Graph using the RDFLib library, and allows querying over it
    
    Examples
    --------
    
    .. ipython:: python
        :okwarning:
        :okexcept:

        from pylipd.rdf_graph import RDFGraph

        # Load RDF file into graph
        rdf = RDFGraph()
        rdf.load(["../examples/rdf/graph.ttl"])
        (result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")
        result_df    

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
    
    def load(self, files, graphid=None):
        '''Loads a RDF file into the graph

        Parameters
        ----------

        rdf_file : str
            Path to the RDF file

        Examples
        --------
        
        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.rdf_graph import RDFGraph

            # Load RDF file into graph
            rdf = RDFGraph()
            rdf.load(["../examples/rdf/graph.ttl"])
            (result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")
            result_df
        '''

        for file in files:
            self.graph.parse(file, publicID=graphid)


    def clear(self):
        '''Clears the graph'''
        self._initialize_graph()


    def copy(self):
        '''
        Makes a copy of the object

        Returns
        -------
        pylipd.rdf_graph.RDFGraph
            a copy of the original object

        '''
        
        return deepcopy(self)

    def merge(self, rdf):
        '''
        Merges the current LiPD object with another LiPD object

        Parameters
        ----------
        rdf : pylipd.rdf_graph.RDFGraph
            RDFGraph object to merge with

        Returns
        -------
        pylipd.rdf_graph.RDFGraph
            merged RDFGraph object

        '''

        merged = self.copy()
        merged.graph.addN(rdf.graph.quads())
        return merged
    
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

            from pylipd.rdf_graph import RDFGraph

            # Fetch LiPD data from remote RDF Graph
            rdf = RDFGraph()
            rdf.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
            (result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")

        '''
        self.endpoint = endpoint


    def query(self, query, remote=False, result="sparql"):
        '''Once data is loaded into the graph (or remote endpoint set), one can make SparQL queries to the graph

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

            from pylipd.rdf_graph import RDFGraph

            rdf = RDFGraph()
            rdf.load(["../examples/rdf/graph.ttl"])
            query = """PREFIX le: <http://linked.earth/ontology#>
                    select ?s ?p ?o where { 
                        ?s ?p ?o 
                    } LIMIT 10 """
            result, result_df = rdf.query(query)
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
    
    def remove(self, ids):
        '''Removes ids(s) from the graph

        Parameters
        ----------

        ids : str or list of str
            graph id(s) to be removed

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.rdf_graph import RDFGraph

            # Remove RDF graph data for given id(s)
            rdf = RDFGraph()
            rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
            rdf.remove("http://example.org/graph")
        '''
        
        if type(ids) is not list:
            ids = [ids]

        # Match subgraphs
        for ctx in self.graph.contexts():
            id = str(ctx.identifier)
            if id in ids:
                self.graph.remove((None, None, None, id))       


    def get(self, ids):
        '''Get id(s) from the graph and returns the LiPD object

        Parameters
        ----------

        ids : str or list of str
            graph id(s) to get.

        Returns
        -------

        pylipd.rdf_graph.RDFGraph
            RDFGraph object with the retrieved graph(s)

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.rdf_graph import RDFGraph

            # Fetch RDF graph data for given id(s)
            rdf = RDFGraph()
            rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
            rdf.get("http://example.org/graph")  
        '''

        graphds = RDFGraph()

        if type(ids) is not list:
            ids = [ids]

        # Match subgraphs
        for ctx in self.graph.contexts():
            id = str(ctx.identifier)
            if id in ids:
                for triple in self.graph.triples((None, None, None, id)):
                    graphds.graph.add((
                        triple[0],
                        triple[1],
                        triple[2],
                        URIRef(id)))
        return graphds
    

    def pop(self, ids):
        '''Pops graph(s) from the combined graph and returns the popped RDF Graph

        Parameters
        ----------

        ids : str or list of str
            rdf id(s) to be popped.

        Returns
        -------

        pylipd.rdf_graph.RDFGraph
            RDFGraph object with the popped graph(s)

        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.rdf_graph import RDFGraph

            # Pop RDF graph data for given id(s)
            rdf = RDFGraph()
            rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
            popped = rdf.pop("http://example.org/graph")      
        '''

        popped = self.get(ids)
        self.remove(ids)
        
        return popped
    

    def get_all_graph_ids(self):
        '''Get all Graph ids
        
        Returns
        -------
        
        ids : list
        
        A list of graph ids
        
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.rdf_graph import RDFGraph

            # Fetch RDF Graph Data
            rdf = RDFGraph()
            rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
            print(rdf.get_all_graph_ids())
        '''        
        ids = [str(ctx.identifier) for ctx in self.graph.contexts()]
        return ids
    

    def serialize(self):
        '''Returns RDF quad serialization of the current combined Graph
        Examples
        --------

        .. ipython:: python
            :okwarning:
            :okexcept:

            from pylipd.rdf_graph import RDFGraph

            # Fetch RDF data
            rdf = RDFGraph()
            rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
            nquads = rdf.serialize()
            print(nquads[:10000])
            print("...")
        '''
        
        return self.graph.serialize(format='nquads')