import os
import re
import json
import copy
import os.path
import tempfile
import multiprocessing as mp

from rdflib import ConjunctiveGraph, Namespace
from rdf_to_lipd import RDFToLiPD

from utils import ucfirst, lcfirst
from lipd_to_rdf import LipdToRDF
from globals.urls import NSURL, ONTONS
from series.regexes import re_pandas_x_und, re_sheet


EMPTY = ['', ' ', None, 'na', 'n/a', '?', "'", "''"]

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
            if not os.path.isfile(lipdfile):
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
            self.cache_remote_datasets_to_local(dsids)
            ts = self._get_timeseries(dsids)

            # Go back to remote
            self.initialize_graph()
            self.load_remote(self.endpoint)

            return ts
        else:
            ts = self._get_timeseries(dsids)
            return ts

    def _get_timeseries(self, dsids):
        timeseries = {}
        for dsid in dsids:
            converter = RDFToLiPD()            
            d = converter.convert(dsid, self.graph)
            if len(d.items()):
                tss = self.extract(d)
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

    def extract(self, d, whichtables="meas", mode="paleo", time="age"):
        """
        LiPD Version 1.3
        Main function to initiate LiPD to TSOs conversion.

        Each object has a
        "paleoNumber" or "chronNumber"
        "tableNumber"
        "modelNumber"
        "time_id"
        "mode" - chronData or paleoData
        "tableType" - "meas" "ens" "summ"

        :param dict d: Metadata for one LiPD file
        :param str whichtables: all, meas, summ, or ens
        :param str mode: paleo or chron mode
        :return list _ts: Time series
        """
        _root = {}
        _ts = {}
        # _switch = {"paleoData": "chronData", "chronData": "paleoData"}
        _pc = "paleoData"
        if mode == "chron":
            _pc = "chronData"
        _root["mode"] = _pc
        _root["time_id"] = time
        try:
            # Build the root level data.
            # This will serve as the template for which column data will be added onto later.
            for k, v in d.items():
                if k == "funding":
                    _root = self._extract_fund(v, _root)
                elif k == "geo":
                    _root = self._extract_geo(v, _root)
                elif k == 'pub':
                    _root = self._extract_pub(v, _root)
                # elif k in ["chronData", "paleoData"]:
                #     # Store chronData and paleoData as-is. Need it to collapse without data loss.
                #     _root[k] = copy.deepcopy(v)
                else:
                    if k not in ["chronData", "paleoData"]:
                        _root[k] = v
            # Create tso dictionaries for each individual column (build on root data)
            _ts = self._extract_pc(d, _root, _pc, whichtables)
        except Exception as e:
            raise(e)

        return _ts


    def _extract_fund(self, l, _root):
        """
        Creates flat funding dictionary.
        :param list l: Funding entries
        """
        for idx, i in enumerate(l):
            for k, v in i.items():
                _root['funding' + str(idx + 1) + '_' + k] = v
        return _root


    def _extract_geo(self, d, _root):
        """
        Extract geo data from input
        :param dict d: Geo
        :return dict _root: Root data
        """
        # May not need these if the key names are corrected in the future.
        # COORDINATE ORDER: [LON, LAT, ELEV]
        x = ['geo_meanLon', 'geo_meanLat', 'geo_meanElev']
        # Iterate through geo dictionary
        for k, v in d.items():
            # Case 1: Coordinates special naming
            if k == 'coordinates':
                for idx, p in enumerate(v):
                    try:
                        # Check that our value is not in EMPTY.
                        if isinstance(p, str):
                            if p.lower() in EMPTY:
                                # If elevation is a string or 0, don't record it
                                if idx != 2:
                                    # If long or lat is empty, set it as 0 instead
                                    _root[x[idx]] = 0
                            else:
                                # Set the value as a float into its entry.
                                _root[x[idx]] = float(p)
                        # Value is a normal number, or string representation of a number
                        else:
                            # Set the value as a float into its entry.
                            _root[x[idx]] = float(p)
                    except IndexError as e:
                        raise e
            # Case 2: Any value that is a string can be added as-is
            elif isinstance(v, str):
                if k == 'meanElev':
                    try:
                        # Some data sets have meanElev listed under properties for some reason.
                        _root['geo_' + k] = float(v)
                    except ValueError as e:
                        # If the value is a string, then we don't want it
                        raise e
                else:
                    _root['geo_' + k] = v
            # Case 3: Nested dictionary. Recursion
            elif isinstance(v, dict):
                _root = self._extract_geo(v, _root)
        return _root


    def _extract_pub(self, l, _root):
        """
        Extract publication data from one or more publication entries.
        :param list l: Publication
        :return dict _root: Root data
        """
        # For each publication entry
        for idx, pub in enumerate(l):
            # Get author data first, since that's the most ambiguously structured data.
            _root = self._extract_authors(pub, idx, _root)
            # Go through data of this publication
            for k, v in pub.items():
                # Case 1: DOI ID. Don't need the rest of 'identifier' dict
                if k == 'identifier':
                    try:
                        _root['pub' + str(idx + 1) + '_DOI'] = "hello"
                    except KeyError as e:
                        raise e
                # Case 2: All other string entries
                else:
                    if k != 'authors' and k != 'author':
                        _root['pub' + str(idx + 1) + '_' + k] = v
        return _root


    def _extract_authors(self, pub, idx, _root):
        """
        Create a concatenated string of author names. Separate names with semi-colons.
        :param any pub: Publication author structure is ambiguous
        :param int idx: Index number of Pub
        """
        try:
            # DOI Author data. We'd prefer to have this first.
            names = pub['author']
        except KeyError as e:
            try:
                # Manually entered author data. This is second best.
                names = pub['authors']
            except KeyError as e:
                # Couldn't find any author data. Skip it altogether.
                names = False

        # If there is author data, find out what type it is
        if names:
            # Build author names onto empty string
            auth = ''
            # Is it a list of dicts or a list of strings? Could be either
            # Authors: Stored as a list of dictionaries or list of strings
            if isinstance(names, list):
                for name in names:
                    if isinstance(name, str):
                        auth += name + ';'
                    elif isinstance(name, dict):
                        for k, v in name.items():
                            auth += v + ';'
            elif isinstance(names, str):
                auth = names
            # Enter finished author string into target
            _root['pub' + str(idx + 1) + '_author'] = auth[:-1]
        return _root


    def _extract_pc(self, d, root, pc, whichtables):
        """
        Extract all data from a PaleoData dictionary.
        :param dict d: PaleoData dictionary
        :param dict root: Time series root data
        :param str pc: paleoData or chronData
        :param str whichtables: all, meas, summ, or ens
        :return list _ts: Time series
        """
        _ts = []
        try:
            # For each table in pc
            for v in d[pc]:
                if whichtables == "all" or whichtables == "meas":
                    for _table_data1 in v["measurementTable"]:
                        _ts = self._extract_table(_table_data1, copy.deepcopy(root), pc, _ts, "meas")
                if whichtables != "meas":
                    if "model" in v:
                        for _table_data1 in v["model"]:
                            # get the method info for this model. This will be paired to all summ and ens table data
                            _method = self._extract_method(_table_data1["method"])
                            if whichtables == "all" or whichtables == "summ":
                                if "summaryTable" in _table_data1:
                                    for _table_data2 in _table_data1["summaryTable"]:
                                        # take a copy of this tso root
                                        _tso = copy.deepcopy(root)
                                        # add in the method details
                                        _tso.update(_method)
                                        # add in the table details
                                        _ts = self._extract_table(_table_data2, _tso, pc, _ts, "summ")
                            if whichtables == "all" or whichtables == "ens":
                                if "ensembleTable" in _table_data1:
                                    for _table_data2 in _table_data1["ensembleTable"]:
                                        _tso = copy.deepcopy(root)
                                        _tso.update(_method)
                                        _ts = self._extract_table(_table_data2, _tso, pc, _ts, "ens")

        except Exception as e:
            raise e
        return _ts


    def _extract_method(self, method):
        """
        Make a timeseries-formatted version of model method data

        :param dict method: Method data
        :return dict _method: Method data, formatted
        """
        _method = {}
        for k,v in method.items():
            _method["method_" + k] = v
        return _method


    def _extract_special(self, current, table_data):
        """
        Extract year, age, and depth column from table data
        :param dict table_data: Data at the table level
        :param dict current: Current data
        :return dict current:
        """
        try:
            # Add age, year, and depth columns to ts_root where possible
            for v in table_data['columns']:
                s = ""
                k = v["variableName"]

                # special case for year bp, or any variation of it. Translate key to "age""
                if "bp" in k.lower():
                    s = "age"

                # all other normal cases. clean key and set key.
                elif any(x in k.lower() for x in ('age', 'depth', 'year', "yr", "distance_from_top", "distance")):
                    # Some keys have units hanging on them (i.e. 'year_ad', 'depth_cm'). We don't want units on the keys
                    if re_pandas_x_und.match(k):
                        s = k.split('_')[0]
                    elif "distance" in k:
                        s = "depth"
                    else:
                        s = k

                # create the entry in ts_root.
                if s:
                    try:
                        current[s] = v['values']
                    except KeyError as e:
                        # Values key was not found.
                        raise e
                    try:
                        current[s + 'Units'] = v['units']
                    except KeyError as e:
                        # Values key was not found.
                        raise e

        except Exception as e:
            raise e

        return current


    def _extract_table_root(self, d, current, pc):
        """
        Extract data from the root level of a paleoData table.
        :param dict d: paleoData table
        :param dict current: Current root data
        :param str pc: paleoData or chronData
        :return dict current: Current root data
        """
        try:
            for k, v in d.items():
                if isinstance(v, str):
                    current[pc + '_' + k] = v
        except Exception as e:
            raise e
        return current


    def _extract_table_model(self, table_data, current, tt):
        """
        Add in modelNumber and summaryNumber fields if this is a summary table

        :param dict table_data: Table data
        :param dict current: LiPD root data
        :param str tt: Table type "summ", "ens", "meas"
        :return dict current: Current root data
        """
        try:
            if tt in ["summ", "ens"]:
                m = re.match(re_sheet, table_data["tableName"])
                if m:
                    _pc_num= m.group(1) + "Number"
                    current[_pc_num] = m.group(2)
                    current["modelNumber"] = m.group(4)
                    current["tableNumber"] = m.group(6)
                else:
                    print("extract_table_summary: Unable to parse paleo/model/table numbers")
        except Exception as e:
            print("extract_table_summary: {}".format(e))
        return current


    def _extract_table(self, table_data, current, pc, ts, tt):
        """
        Use the given table data to create a time series entry for each column in the table.

        :param dict table_data: Table data
        :param dict current: LiPD root data
        :param str pc: paleoData or chronData
        :param list ts: Time series (so far)
        :param bool summary: Summary Table or not
        :return list ts: Time series (so far)
        """
        current["tableType"] = tt
        # Get root items for this table
        current = self._extract_table_root(table_data, current, pc)
        # Add in modelNumber and tableNumber if this is "ens" or "summ" table
        current = self._extract_table_model(table_data, current, tt)
        # Add age, depth, and year columns to root if available
        _table_tmp = self._extract_special(current, table_data)
        try:
            # Start creating entries using dictionary copies.
            for _col_data in table_data["columns"]:
                # Add column data onto root items. Copy so we don't ruin original data
                _col_tmp = self._extract_columns(_col_data, copy.deepcopy(_table_tmp), pc)
                try:
                    ts.append(_col_tmp)
                except Exception as e:
                    print("extract_table: Unable to create ts entry, {}".format(e))
        except Exception as e:
            raise e
        return ts


    def _extract_columns(self, d, tmp_tso, pc):
        """
        Extract data from one paleoData column
        :param dict d: Column dictionary
        :param dict tmp_tso: TSO dictionary with only root items
        :return dict: Finished TSO
        """
        for k, v in d.items():
            if isinstance(v, dict):
                flat_data = self._extract_nested(pc + "_" + k, v, {})
                for n,m in flat_data.items():
                    tmp_tso[n] = m
            else:
                # Assume if it's not a special nested case, then it's a string value
                tmp_tso[pc + '_' + k] = v
        return tmp_tso


    def _extract_nested(self, crumbs, dat, flat_dat):
        try:
            for k, v in dat.items():
                if isinstance(v, dict):
                    flat_dat = self._extract_nested(crumbs + "_" + k, v, flat_dat)
                else:
                    flat_dat[crumbs + "_" + k] = v
        except Exception as e:
            print("ts: _extract_nested: " + e)

        return flat_dat