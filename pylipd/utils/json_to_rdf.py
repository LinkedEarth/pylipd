from rdflib.graph import URIRef, Literal
from rdflib.namespace import XSD

from ..globals.urls import ONTONS

class JSONToRDF:
    def __init__(self, graph, graphurl):
        self.graph = graph
        self.graphurl = graphurl

    def _load_triple_into_graph(self, subject, propid, value):
        for val in value:
            valitem = None
            if val["@type"] == "uri":
                valitem = URIRef(val["@id"])
            elif val["@type"] == "literal":
                dtype = val["@datatype"]
                if dtype:
                    valitem = Literal(value, datatype=(XSD[dtype] if dtype in XSD else None))
                else:
                    valitem = Literal(value)
            if valitem:
                self.graph.add((
                    URIRef(subject),
                    URIRef(propid),
                    valitem,
                    URIRef(self.graphurl)
                ))

    def _clear_subgraph(self):
        for ctx in self.graph.contexts():
            id = str(ctx.identifier)
            if id == self.graphurl:
                self.graph.remove((None, None, None, id))    

    def load_data_in_graph(self, data):        
        # Clear the subgraph
        self._clear_subgraph()

        # Load data
        for subject in data:
            for propid in data[subject]:
                value = data[subject][propid]
                self._load_triple_into_graph(subject, ONTONS + propid, value)
