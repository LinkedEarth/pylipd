import tempfile
from lipd_to_rdf import LipdToRDF
import tempfile
from rdflib import Graph, Namespace
from globals import NS, ONTONS
import os

class LiPD(object):
    def __init__(self, lipdfiles):
        self.converter = LipdToRDF()
        self.graph = Graph(bind_namespaces="rdflib")
        self.graph.bind("le", Namespace(ONTONS))
        self.graph.bind("", Namespace(NS))

        for lipdfile in lipdfiles:
            rdffile = tempfile.NamedTemporaryFile().name
            try:
                self.converter.convert(lipdfile, rdffile)
            except Exception as e:
                print("ERROR: Could not convert LiPD file to RDF")            
                raise(e)
            self.graph.parse(rdffile)
            os.remove(rdffile)

    def query(self, query):
        qres = self.graph.query(query)
        return qres

    def local_name(self, url):
        return str(url).split("#")[-1]

    def get_all_properties(self, id):
        qres = self.graph.query(f"SELECT ?p ?o WHERE {{ <{id}> ?p ?o }}")
        result = {}
        for row in qres:
            if self.local_name(row.p) not in result:
                result[self.local_name(row.p)] = []
            result[self.local_name(row.p)].append(self.local_name(row.o))
        return result

    def get_dataset_property_object_properties(self, dsid, propid):
        qres = self.graph.query(f"SELECT ?o WHERE {{ <{dsid}> le:{propid} ?o }}")
        return [ self.get_all_properties(row.o) for row in qres ]

    def get_dataset(self, dsid):
        ds = self.get_all_properties(dsid)
        ds["id"] = str(dsid)
        ds["includesPaleoData"] = self.get_paleo_data(dsid)
        ds["includesChronData"] = self.get_chron_data(dsid)
        ds["collectedFrom"] = self.get_dataset_property_object_properties(dsid, "collectedFrom")
        ds["publishedIn"] = self.get_dataset_property_object_properties(dsid, "publishedIn")
        return ds

    def get_datasets(self):
        qres = self.graph.query("SELECT ?s WHERE { ?s a le:Dataset }")
        return [self.get_dataset(row.s) for row in qres]

    def get_variables(self, dsid):
        qres = self.graph.query(f"SELECT ?o WHERE {{ <{dsid}> le:includesVariable ?o }}")
        vars = []
        for row in qres:
            var = self.get_all_properties(row.o)
            var["id"] = self.local_name(row.o)
            vars.append(var)
        return vars

    def get_data_table(self, dataid):
        qres = self.graph.query(f"SELECT ?o WHERE {{ <{dataid}> le:foundInMeasurementTable ?o }}")
        return [ { 
            "id": self.local_name(row.o), 
            "includesVariable": self.get_variables(row.o) 
        } for row in qres ]

    def get_paleo_data(self, dsid):
        qres = self.graph.query(f"SELECT ?o WHERE {{ <{dsid}> le:includesPaleoData ?o }}")
        return [ { "foundInMeasurementTable": self.get_data_table(row.o) } for row in qres ]

    def get_chron_data(self, dsid):
        qres = self.graph.query(f"SELECT ?o WHERE {{ <{dsid}> le:includesChronData ?o }}")
        return [ { "foundInMeasurementTable": self.get_data_table(row.o) } for row in qres ]
