from rdflib.graph import ConjunctiveGraph, URIRef
import json

class RDFToJSON:
    """
    The RDFToFacts class helps in converting an RDF Graph to Plain JSON
    It uses the SCHEMA dictionary (from globals/schema.py) to do the conversion
    """    
    def __init__(self, id, graph: ConjunctiveGraph):
        self.graph = graph
        self.allfacts = {}
        self._get_indexed_facts(id)
    
    def _get_prop_values_from_query_result_p_o(self, qres):
        result = {}
        for row in qres:
            pname = self._local_name(row.p)
            if pname not in result:
                result[pname] = []
            value = {}
            if isinstance(row.o, URIRef):
                value["@type"] = "uri"
                value["@id"] = str(row.o)
            else:
                value["@type"] = "literal"
                value["@value"] = row.o.value
                value["@datatype"] = row.o.datatype
            result[pname].append(value)
        return result

    def _get_facts(self, id):
        query = f"SELECT ?p ?o WHERE {{ <{id}> ?p ?o }}"
        qres = self.graph.query(query)
        return self._get_prop_values_from_query_result_p_o(qres)

    def _local_name(self, url):
        return str(url).split("#")[-1]
    
    def _get_indexed_facts(self, id):
        if id in self.allfacts:
            return

        facts = self._get_facts(id)
        self.allfacts[id] = facts

        for pname, pfacts in facts.items():
            for pfact in pfacts:
                if pfact["@type"] == "uri":
                    if pname != "type":
                        self._get_indexed_facts(pfact["@id"])

    def to_json(self):
        return json.dumps(self.allfacts, default=str, indent=3)