import os
import re
import json
import os.path
import tempfile
import multiprocessing as mp

from rdflib import ConjunctiveGraph, Namespace

from pylipd.rdf_to_lipd import RDFToLiPD
from pylipd.lipd_to_rdf import LipdToRDF
from pylipd.legacy_utils import LiPD_Legacy

from .utils import ucfirst, lcfirst
from .globals.urls import NSURL, ONTONS

###########################################
# TODO:
# -----------------------------------------
# Pass the "Collection id" to the LiPD to RDF conversion
# - Use it for Default namespace & for hasURL
# - Mark URL prefix in globals
# Recreate the RDF files & Send .nq files to the endpoint
# Reload the graphs to the endpoint
# Move the LiPD files to the server 
###########################################
def convert_to_rdf(lipdfile, rdffile, collection_id=None):
    converter = LipdToRDF(collection_id)    
    """Worker that converts one lipdfile to an rdffile"""
    try:
        converter.convert(lipdfile, rdffile)
    except Exception as e:
        print(f"ERROR: Could not convert LiPD file {lipdfile} to RDF")            
        raise e
        raise(e)

def multi_convert_to_rdf(filemap, collection_id=None):
    """Create a pool to convert all lipdfiles to rdffiles"""
    pool = mp.Pool(mp.cpu_count())
    args = [(lipdfile, rdffile, collection_id) for lipdfile, rdffile in filemap.items()]
    pool.starmap(convert_to_rdf, args, chunksize=1)
    pool.close()


class LiPD(object):
    def __init__(self):
        self.initialize_graph()
        self.remote = False

    def initialize_graph(self):
        self.graph = ConjunctiveGraph()
        self.graph.bind("le", Namespace(ONTONS))        
        #self.graph.bind("", Namespace(NS))

    def load_from_dir(self, dir_path, collection_id=None):
        if not os.path.isdir(dir_path):
            print(f"Directory {dir_path} does not exist")
            return

        lipdfiles = []
        for path in os.listdir(dir_path):
            if os.path.isfile(path) and path.endswith(".lpd"):
                fullpath = os.path.join(dir_path, path)
                lipdfiles.append(fullpath)
        self.load(lipdfiles, collection_id)


    # Allows loading http locations
    def load(self, lipdfiles, collection_id=None):
        if type(lipdfiles) is not list:
            lipdfiles = [lipdfiles]
            
        filemap = {}
        for lipdfile in lipdfiles:
            print(lipdfile)
            if not os.path.isfile(lipdfile) and not lipdfile.startswith("http"):
                print(f"File {lipdfile} does not exist")
                continue

            rdffile = tempfile.NamedTemporaryFile().name
            filemap[lipdfile] = rdffile
        
        print(f"Loading {len(filemap.keys())} LiPD files" + (" from Collection: {collection_id}" if collection_id else ""))
        
        multi_convert_to_rdf(filemap, collection_id)
        print("Conversion to RDF done..")

        self.remote = False
        print("Loading RDFs into graph")
        for lipdfile in lipdfiles:
            rdffile = filemap[lipdfile]
            if os.path.exists(rdffile):
                self.graph.parse(rdffile, format="nquads")
                os.remove(rdffile)
        print("Loaded..")


    def set_endpoint(self, endpoint):
        self.remote = True
        self.endpoint = endpoint


    def convert_lipd_dir_to_rdf(self, lipd_dir, rdf_file, collection_id=None):
        filemap = {}
        for path in os.listdir(lipd_dir):
            fullpath = os.path.join(lipd_dir, path)
            tmp_rdf_file = tempfile.NamedTemporaryFile().name
            filemap[fullpath] = tmp_rdf_file
        
        print(f"Starting conversion of {len(filemap.keys())} LiPD files")

        multi_convert_to_rdf(filemap, collection_id)
        
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


    def query(self, query, result="sparql"):
        if self.remote:
            matches = re.match(r"\s*SELECT\s+(.+)\s+WHERE\s+{(.+)}\s*", query, re.DOTALL)
            if matches:
                vars = matches.group(1)
                where = matches.group(2)
                query = f"SELECT {vars} WHERE {{ SERVICE <{self.endpoint}> {{ {where} }} }}"
        return self.graph.query(query, result=result)


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

    def load_remote_datasets(self, dsids):
        if dsids == None or len(dsids) == 0:
            raise Exception("No dataset ids to cache")
        dsidstr = (' '.join('<' + NSURL + "/" + dsid + '>' for dsid in dsids))
        print("Caching datasets from remote endpoint..")
        qres = self.query(f"SELECT ?s ?p ?o ?g WHERE {{ GRAPH ?g {{ ?s ?p ?o }} VALUES ?g {{ {dsidstr} }} }}")

        # Reinitialize graph
        self.initialize_graph()
        for row in qres:
            self.graph.add((row.s, row.p, row.o, row.g))
        print("Done..")
        self.remote = False

    def get_timeseries(self, dsids):
        if self.remote:
            # Cache datasets locally - to speed up queries
            self.load_remote_datasets(dsids)
            ts = self._get_timeseries(dsids)

            # Go back to remote
            self.initialize_graph()
            self.set_endpoint(self.endpoint)

            return ts
        else:
            ts = self._get_timeseries(dsids)
            return ts

    def _get_timeseries(self, dsids):
        timeseries = {}
        for dsid in dsids:
            converter = RDFToLiPD()            
            d = converter.convert(dsid, self.graph)
            print("Extracting timeseries from dataset: " + dsid + " ...")
            if len(d.items()):
                tss = LiPD_Legacy().extract(d)
                timeseries[dsid] = tss
        return timeseries

    def get_lipd(self, dsid):
        converter = RDFToLiPD()            
        return converter.convert(dsid, self.graph)

    def get_dataset(self, dsid, data_only=False):
        ds = self.get_all_properties(dsid)
        ds["id"] = str(dsid)
        ds["includesPaleoData"] = self.get_paleo_data(dsid)
        ds["includesChronData"] = self.get_chron_data(dsid)
        if not data_only:
            ds["collectedFrom"] = self.get_dataset_property_object_properties(dsid, "collectedFrom")
            ds["publishedIn"] = self.get_dataset_property_object_properties(dsid, "publishedIn")
        return ds


    def get_datasets(self, dsids=None, data_only=False):
        extraclause = ""
        if dsids != None:
            dsidstr = (' '.join('<' + NSURL + "#" + dsid + '>' for dsid in dsids))
            extraclause = f"VALUES ?s {{ {dsidstr} }} ."

        query = f"""
            SELECT ?s WHERE {{ 
                ?s a le:Dataset .
                {extraclause}
            }}
            """
        qres = self.query(query)
        return [self.get_dataset(row.s, data_only) for row in qres]

    def get_all_dataset_ids(self):
        query = f"""
            SELECT ?dsname WHERE {{ 
                ?ds a le:Dataset .
                ?ds le:name ?dsname
            }}
            """
        qres = self.query(query)
        return [row.dsname for row in qres]

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