from rdflib import RDF, RDFS
from rdflib.graph import URIRef, Literal
from rdflib.namespace import XSD

from ..globals.urls import ONTONS

class JSONToRDF:
    def __init__(self, graph, graphurl):
        self.graph = graph
        self.graphurl = graphurl

    def _load_triple_into_graph(self, subject, prop, value):
        for val in value:
            valitem = None
            if val["@type"] == "uri":
                valitem = URIRef(val["@id"])
            elif val["@type"] == "literal":
                dtype:str = val["@datatype"]
                if dtype:
                    if type(val["@value"]) == str:
                        dtype="http://www.w3.org/2001/XMLSchema#string"
                    valitem = Literal(val["@value"], datatype=URIRef(dtype))
                else:
                    valitem = Literal(val["@value"])
            if valitem:
                self.graph.add((
                    URIRef(subject),
                    prop,
                    valitem,
                    URIRef(self.graphurl)
                ))

    def _clear_subgraph(self):
        for ctx in self.graph.contexts():
            id = str(ctx.identifier)
            if id == self.graphurl:
                self.graph.remove((None, None, None, URIRef(self.graphurl)))    

    def load_data_in_graph(self, data):        
        # Clear the subgraph
        self._clear_subgraph()

        # Load data
        for subject in data:
            for propid in data[subject]:
                value = data[subject][propid]
                prop = URIRef(ONTONS + propid)
                if propid == "type":
                    prop = RDF.type
                if propid == "label":
                    prop = RDFS.label
                self._load_triple_into_graph(subject, prop, value)
