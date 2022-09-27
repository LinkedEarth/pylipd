import os
import re
import json
import tempfile
import multiprocessing as mp
from rdflib import Graph, Namespace

from utils import ucfirst, lcfirst
from lipd_to_rdf import LipdToRDF
from globals.namespaces import NS, ONTONS

def convert_to_rdf(lipdfile, rdffile):
    converter = LipdToRDF()    
    """Worker that converts one lipdfile to an rdffile"""
    try:
        converter.convert(lipdfile, rdffile)
    except Exception as e:
        print(f"ERROR: Could not convert LiPD file {lipdfile} to RDF")            
        raise(e)

def multi_convert_to_rdf(filemap):
    """Create a pool to convert all lipdfiles to rdffiles"""
    pool = mp.Pool(mp.cpu_count())
    args = [(lipdfile, rdffile) for lipdfile, rdffile in filemap.items()]
    pool.starmap(convert_to_rdf, args, chunksize=1)
    pool.close()


class LiPD(object):
    def __init__(self):
        self.graph = Graph(bind_namespaces="rdflib")
        self.graph.bind("le", Namespace(ONTONS))
        self.graph.bind("", Namespace(NS))


    def load_local_from_dir(self, dir_path):
        lipdfiles = []
        for path in os.listdir(dir_path):
            fullpath = os.path.join(dir_path, path)
            lipdfiles.append(fullpath)
        self.load_local(lipdfiles)


    #####################################
    # TODO: Allow loading http locations
    #####################################
    def load_local(self, lipdfiles):
        filemap = {}
        for lipdfile in lipdfiles:
            rdffile = tempfile.NamedTemporaryFile().name
            filemap[lipdfile] = rdffile
        print(f"Starting conversion of {len(filemap.keys())} LiPD files")
        multi_convert_to_rdf(filemap)
        print("Conversion to RDF done..")

        self.remote = False
        print("Loading RDF into graph")
        for lipdfile in lipdfiles:
            rdffile = filemap[lipdfile]
            if os.path.exists(rdffile):
                self.graph.parse(rdffile)
                os.remove(rdffile)
        print("Loaded..")


    def load_remote(self, endpoint):
        self.remote = True
        self.endpoint = endpoint


    def query(self, query):
        if self.remote:
            matches = re.match(r"\s*SELECT\s+(.+)\s+WHERE\s+{(.+)}\s*", query, re.DOTALL)
            if matches:
                vars = matches.group(1)
                where = matches.group(2)
                query = f"SELECT {vars} WHERE {{ SERVICE <{self.endpoint}> {{ {where} }} }}"
                print(query)
        return self.graph.query(query)


    def local_name(self, url):
        return str(url).split("#")[-1]


    def _get_prop_values_from_query_result_p_o(self, qres):
        result = {}
        for row in qres:
            if self.local_name(row.p) not in result:
                result[self.local_name(row.p)] = []
            result[self.local_name(row.p)].append(self.local_name(row.o))
        return result


    def get_all_properties(self, id):
        qres = self.query(f"SELECT ?p ?o WHERE {{ <{id}> ?p ?o }}")
        return self._get_prop_values_from_query_result_p_o(qres)


    def get_dataset_property_object_properties(self, dsid, propid):
        qres = self.query(f"SELECT ?s ?p ?o WHERE {{ <{dsid}> le:{propid} ?s . ?s ?p ?o }}")
        
        object_rows = {}
        # Group rows by object
        for row in qres:
            objid = str(row.s)
            if objid not in object_rows:
                object_rows[objid] = []
            object_rows[objid].append(row)
        return [{
            "id": self.local_name(objid),
            "properties": self._get_prop_values_from_query_result_p_o(object_rows[objid])
        } for objid in object_rows]


    def get_dataset(self, dsid, data_only=True):
        ds = self.get_all_properties(dsid)
        ds["id"] = str(dsid)
        ds["includesPaleoData"] = self.get_paleo_data(dsid)
        ds["includesChronData"] = self.get_chron_data(dsid)
        if not data_only:
            ds["collectedFrom"] = self.get_dataset_property_object_properties(dsid, "collectedFrom")
            ds["publishedIn"] = self.get_dataset_property_object_properties(dsid, "publishedIn")
        return ds


    def get_datasets(self):
        qres = self.query("SELECT ?s WHERE { ?s a le:Dataset }")
        return [self.get_dataset(row.s) for row in qres]


    def get_table_variables(self, tableid):
        qres = self.query(f"SELECT ?v ?p ?o WHERE {{ <{tableid}> le:includesVariable ?v . ?v ?p ?o }}")
        vars = []

        var_rows = {}
        # Group rows by variable
        for row in qres:
            varid = str(row.v)
            if varid not in var_rows:
                var_rows[varid] = []
            var_rows[varid].append(row)
        
        # Get property values from rows for variable
        for varid in var_rows:
            var = self._get_prop_values_from_query_result_p_o(var_rows[varid])
            var["id"] = self.local_name(varid)
            if "hasValues" in var:
                try:
                    var["hasValues"] = json.loads(var["hasValues"][0])
                except:
                    pass
            vars.append(var)
        return vars


    def get_data_table(self, dataid):
        qres = self.query(f"SELECT ?o WHERE {{ <{dataid}> le:foundInMeasurementTable ?o }}")
        return [ { 
            "id": self.local_name(row.o), 
            "includesVariable": self.get_table_variables(row.o) 
        } for row in qres ]

    
    def get_data(self, dsid, type="Paleo"):
        lctype = lcfirst(type)
        uctype = ucfirst(type)
        qres = self.query(f""" 
            SELECT ?o ?t ?m ?met ?mst ?mdt WHERE {{ 
                <{dsid}> le:includes{uctype}Data ?o . 
                ?o le:foundInMeasurementTable ?t . 
                OPTIONAL {{ 
                    ?o le:{lctype}ModeledBy ?m . 
                    OPTIONAL {{ ?m le:foundInEnsembleTable ?met }} .
                    OPTIONAL {{ ?m le:foundInSummaryTable ?mst }} .
                    OPTIONAL {{ ?m le:foundInDistributionTable ?mdt }} .
                }}
            }}
        """)
        return [ { 
            "id": self.local_name(row.o),
            "foundInMeasurementTable": {
                "id": self.local_name(row.t),
                "includesVariable": self.get_table_variables(row.t) 
            },
            f"{lctype}ModeledBy": {
                "id": self.local_name(row.m),
                "foundInEnsembleTable": {
                    "id": self.local_name(row.met),
                    "includesVariable": self.get_table_variables(row.met)
                } if row.met is not None else None ,
                "foundInSummaryTable": {
                    "id": self.local_name(row.mst),
                    "includesVariable": self.get_table_variables(row.mst)
                } if row.mst is not None else None ,
                "foundInDistributionTable": {
                    "id": self.local_name(row.mdt),
                    "includesVariable": self.get_table_variables(row.mdt)
                } if row.mdt is not None else None
            } if row.m is not None else None
        } for row in qres ]


    def get_paleo_data(self, dsid):
        return self.get_data(dsid, "Paleo")


    def get_chron_data(self, dsid):
        return self.get_data(dsid, "Chron")


    ##############################################
    # TODO: Search for Datasets based on some filters
    # - Look for "Query LinkedEarth" LiPd Utils from Pyleoclim
    #   https://github.com/LinkedEarth/Pyleoclim_util/blob/master/pyleoclim/utils/lipdutils.py
    ##############################################
    def search_datasets(variableName=[ ], archiveType=[ ], proxyObsType=[ ], infVarType = [ ], sensorGenus=[ ],
                    sensorSpecies=[ ], interpName =[ ], interpDetail =[ ], ageUnits = [ ],
                    ageBound = [ ], ageBoundType = [ ], recordLength = [ ], resolution = [ ],
                    lat = [ ], lon = [ ], alt = [ ], print_response = True, download_lipd = True,
                    download_folder = 'default'):
        pass


    ##############################################
    # TODO: Fetch ensemble data
    # TODO: Load ensemble data
    ##############################################
    def find_ensemble_table_for_variable(self, ensemble_table):
        pass


    ##############################################
    # TODO: Create LiPDSeries and MultipleLiPDSeries objects
    # LiPDSeries is:
    # - Age and/or Year and/or Depth (values) & a Variable (values) + Dataset id + Table id + Variable id 
    # - Look at : https://github.com/LinkedEarth/Pyleoclim_util/blob/master/pyleoclim/core/lipdseries.py
    # - use xAxisTs function (to return depth as well)
    #
    # MultipleLiPDSeries is:
    # - A list of LiPDSeries (could be from one or more datasets)
    ##############################################
