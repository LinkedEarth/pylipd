"""
The LipdToRDF class helps in converting a LiPD file to an RDF Graph.
It uses the SCHEMA dictionary (from globals/schema.py) to do the conversion
"""

import copy
import json
import pickle
import re
import os
import os.path
import zipfile
import tempfile
import pandas as pd

from rdflib import RDFS
from rdflib.graph import ConjunctiveGraph, Literal, RDF, URIRef, BNode, Collection
from rdflib.namespace import XSD

from io import BytesIO
from urllib.request import urlopen
from urllib.parse import urlparse, urlunparse, quote

from ..globals.urls import NSURL, DATAURL, ONTONS, NAMESPACES
from ..globals.blacklist import BLACKLIST
from ..globals.synonyms import SYNONYMS
from ..globals.schema import SCHEMA

from .utils import expand_schema, ucfirst, lcfirst, camelCase, unCamelCase, escape, uniqid, sanitizeId

class LipdToRDF:
    """
    The LipdToRDF class helps in converting a LiPD file to an RDF Graph. 
    It uses the SCHEMA dictionary (from globals/schema.py) to do the conversion
    """

    def __init__(self, standardize=True, add_labels=True):
        self.graph = ConjunctiveGraph()
        self.lipd_csvs = {}
        self.graphurl = NSURL
        self.namespace = NSURL + "/"
        self.standardize = standardize
        self.add_labels = add_labels
        self.schema = expand_schema(copy.deepcopy(SCHEMA))  


    def convert(self, lipdpath):
        '''Convert LiPD file to RDF Graph

        Parameters
        ----------

        lipdpath : str
            path to lipd file (the path could also be a url)

        '''
        self.graph = ConjunctiveGraph()
        
        lpdname = os.path.basename(lipdpath).replace(".lpd", "")
        lpdname = re.sub("\?.+$", "", lpdname)

        self.graphurl = NSURL + "/" + lpdname

        with tempfile.TemporaryDirectory(prefix="lipd_to_rdf_") as tmpdir:
            self._unzip_lipd_file(lipdpath, tmpdir)
            jsons = self._find_files_with_extension(tmpdir, 'jsonld')
            for jsonpath, _ in jsons:
                jsondir = os.path.dirname(jsonpath)
                csvs = self._find_files_with_extension(jsondir, 'csv')
                self.lipd_csvs = {}
                for csvpath, _ in csvs:
                    csvname = os.path.basename(csvpath)        
                    try:
                        self.lipd_csvs[csvname] = pd.read_csv(csvpath, header=None)
                    except:
                        # If normal load doesn't work, try to detect the number of columns and load it that way
                        print(f"WARNING: CSV file '{csvname}' might have inconsistent number of columns !!\nDetecting number of columns to load ..\n")
                        self.lipd_csvs[csvname] = self._detect_columns_and_load(csvpath)
                self._load_lipd_json_to_graph(jsonpath)

    def _detect_columns_and_load(self, filename):
        # detect number of columns
        num_columns=0
        with open(filename) as f:
            for line in f.readlines():
                num = len(line.split(','))
                if num > num_columns:
                    num_columns=num
        # load with pre-determined number of columns
        df=pd.read_csv(filename,names=range(num_columns))
        return df


    def serialize(self, topath, type="rdf"):
        '''Write LiPD RDF Graph to RDF file (or Pickle file)

        Parameters
        ----------

        topath : str
            path to the output file

        type : str
            the output file type : rdf or pickle (we store the pickled rdf graph for efficiency sometimes)
        '''

        if self.graph:
            if type == "rdf":
                self.graph.serialize(topath, format="nquads", encoding="utf-8")
            elif type == "pickle":
                with open(topath, 'wb') as f:
                    pickle.dump(self.graph, f)


    def _unzip_lipd_file(self, lipdfile, unzipdir):
        if lipdfile.startswith("http"):
            # If this is a URL
            # Handle special characters in url (if any)
            res = urlparse(lipdfile)
            lipdurl = urlunparse(res._replace(path=quote(res.path)))

            # Open url and unzip
            resp = urlopen(lipdurl)
            with zipfile.ZipFile(BytesIO(resp.read())) as zip_ref:
                zip_ref.extractall(unzipdir)
        else:
            # If this is a local file
            # Unzip file
            with zipfile.ZipFile(lipdfile, 'r') as zip_ref:
                zip_ref.extractall(unzipdir)

    def _parse_persons_string(self, author_string, parent = None) :
        # Check for semi-colon delimiter and split accordingly
        if ";" in author_string:
            author_split = re.split("\s*;\s*", author_string)
            # Further split the authors with commas if necessary
            author_list = []
            for author in author_split:
                author = author
                if "," in author:
                    last_first = re.split("\s*,\s*", author)
                    author_list.append(f"{last_first[1]} {last_first[0]}")
                else:
                    author_list.append(author)
            authors = author_list
        else:
            # Split the author string with commas
            author_list = []
            author_split = re.split("\s*,\s*", author_string)
            if len(author_split) % 2 == 0:
                # Even number : last name first name
                for i in range(0, len(author_split), 2):
                    author_list.append(f"{author_split[i+1]} {author_split[i]}")
            else:
                # Odd number : first name last name
                for author in author_split:
                    author_list.append(author)
            authors = author_list
        return authors


    def _parse_persons(self, auths, parent = None) :
        authors = []
        if (not type(auths) is list) :
            auths = [auths]
        
        for authstr in auths: 
            authname = None
            if type(authstr) is dict:
                if "name" in authstr:
                    authname = authstr["name"]
            else:
                authname = authstr
            
            if authname:
                auth = self._parse_persons_string(authname, parent)
                if type(auth) is list:
                    authors.extend(auth)
                else:
                    authors.append(auth)
        
        return [{"name": auth} for auth in authors]


    def _parse_location(self, geo, parent = None) :
        ngeo = {}
        ngeo["locationType"] = geo["type"] if "type" in geo else None
        ngeo["coordinatesFor"] = parent["@id"]
        coords = geo["geometry"]["coordinates"]
        if (coords and len(coords) > 0) :
            ngeo["coordinates"] = str(str(coords[1]) + ",") + str(coords[0])
            ngeo["wgs84:lat"] = coords[1]
            ngeo["hasLatitude"] = coords[1]
            ngeo["latitude"] = coords[1]

            ngeo["wgs84:long"] = coords[0]
            ngeo["longitude"] = coords[0]
            ngeo["hasLongitude"] = coords[0]
            
            if (len(coords) > 2) :
                ngeo["wgs84:alt"] = coords[2]
                ngeo["elevation"] = coords[2]
                ngeo["hasElevation"] = coords[2]
        
        if "properties" in geo and isinstance(geo["properties"], dict) :
            for key,value in geo["properties"].items() :
                ngeo[key] = value
        elif isinstance(geo, dict) :
            for key,value in geo.items() :
                if key != "geometry":
                    # Do not add lat long if they are already added
                    if f"wgs84:{key}" not in ngeo:
                        ngeo[key] = value
        return ngeo


    def _get_uncertainty(self, val, parent = None) :
        uncertainty = {}
        uncertainty["hasValue"] = val
        uncertainty["analytical"] = val
        uncertainty["reproducibility"] = val
        return uncertainty

    def _get_google_spreadsheet_url(self, key, parent = None) :
        return "https://docs.google.com/spreadsheets/d/" + str(key) + ""
    
    def _get_parent_property(self, obj, prop) :
        parent = obj["@parent"]
        while (parent) :
            if ((prop in parent)) :
                return parent[prop]
            
            parent = parent["@parent"]
        return None

    def _get_parent_with_property_value(self, obj, prop, val) :
        parent = obj["@parent"]
        while (parent) :
            if ((prop in parent) and parent[prop] == val) :
                return parent
            
            parent = parent["@parent"]
        return None
    
    def _set_identifier_properties(self, pub, objhash) :
        props = {}
        if "identifier" in pub :
            for identifier in pub["identifier"] : 
                if identifier["type"] == "doi" :
                    if "hasDOI" not in pub:
                        pub["hasDOI"] = []  
                    pub["hasDOI"].append(identifier["id"])
                else : 
                    if identifier["type"] == "issn" :
                        if "hasISSN" not in pub:
                            pub["hasISSN"] = []                      
                        pub["hasISSN"].append(identifier["id"])
                    elif identifier["type"] == "isbn" :
                        if "hasISBN" not in pub:
                            pub["hasISBN"] = []                          
                        pub["hasISBN"].append(identifier["id"])
                
                if (("url" in identifier)) :
                    if "hasLink" not in pub:
                        pub["hasLink"] = []  
                    pub["hasLink"].append(identifier["url"])

            del pub["identifier"]
        
        return [pub, objhash, []]
    
    def _values_to_string(self, obj, objhash) :
        if "values" in obj :
            if (type(obj["values"]) is list) :
                obj["values"] = ", ".join(obj["values"])
        return [obj, objhash, []]

    
    def _guess_sensor_type(self, archive, observation, sensor) :
        if (('sensorGenus' in sensor) or ('sensorSpecies' in sensor)) :
            if (archive == "MarineSediment") :
                return "Foraminifera"
            elif (archive == "Coral") :
                return "Polyp"
            elif (archive == "Wood") :
                return "Vegetation"
            elif (archive == "MolluskShell") :
                return "Bivalves"
            elif (archive == "Sclerosponge") :
                return "Sponge"
            return "OrganicSensor"
        else : 
            if (archive == "MarineSediment" and (observation == "Uk37" or observation == "Alkenone")) :
                type = "Coccolithophores"
            elif (archive == "MarineSediment" and observation == "TEX86") :
                type = "Archea"
            elif (archive == "MarineSediment" and observation == "D18O") :
                type = "Foraminifera"
            elif (archive == "MarineSediment" and observation == "Mg/Ca") :
                type = "Foraminifera"
            elif (archive == "LakeSediment" and (observation == "Uk37" or observation == "Alkenone")) :
                type = "Coccolithophores"
            elif (archive == "LakeSediment" and observation == "TEX86") :
                type = "Archea"
            elif (archive == "LakeSediment" and observation == "Midge") :
                type = "Chironomids"
            elif (archive == "LakeSediment" and observation == "BSi") :
                type = "Diatoms"
            elif (archive == "LakeSediment" and observation == "Chironomid") :
                type = "Chironomids"
            elif (archive == "LakeSediment" and observation == "Reflectance") :
                type = "PhotosyntheticAlgae"
            elif (archive == "LakeSediment" and observation == "Pollen") :
                type = "Watershed"
            elif (archive == "Coral") :
                return "Polyp"
            elif (archive == "Wood") :
                return "Vegetation"
            elif (archive == "MolluskShell") :
                return "Bivalves"
            elif (archive == "Sclerosponge") :
                return "Sponge"
            elif (archive == "Speleothem") :
                return "Karst"
            elif (archive == "GlacierIce") :
                return "Snow"
            elif (archive == "LakeSediment" and observation == "VarveThickness") :
                return "Catchment"
            elif (archive == "GlacierIce" and observation == "Melt") :
                return "IceSurface"
            elif (archive == "Borehole") :
                return "Soil"
            else : 
                return "InorganicSensor"
    
    def _get_observation(self, observation) :
        if observation is None:
            return None
        if (observation.lower() == "alkenone") :
            return "Uk37"
        return camelCase(observation)

    def _get_variable_id(self, obj, parentid) :
        iobj = dict((k.lower(), v) for k, v in obj.items())
        if "tsid" not in iobj:
            iobj["tsid"] = uniqid()
        id =  parentid + "." + iobj["tsid"]
        id += "." + str(iobj.get("variablename", ""))
        return id
    
    def _wrap_integration_time(self, obj, objhash) :
        objid = obj["@id"]
        # Deal with integrationTime
        pvals = {}
        for key,value in obj.items() :
            if (re.search(r"^integrationTime\$", key, re.IGNORECASE)) :
                pvals["hasValue"] = value
                del obj[key]
            else:
                m = re.search(r"^integrationTime(.+)", key)
                if m is not None:
                    nkey = m.groups()[0]
                    nkey_lcfirst = lcfirst(nkey)
                    pvals[nkey_lcfirst] = value
                    del obj[key]

        if len(pvals.values()) > 0:
            intimeid = objid + '.IntegrationTime'
            obj['integrationTime'] = intimeid
            intime = {}
            intime['@id'] = intimeid
            intime['@category'] = 'IntegrationTime'
            intime['@schema'] = 'IntegrationTime'
            intime.update(pvals)
            objhash[intimeid] = intime
            return [obj, objhash, [intimeid]]
        
        return [obj, objhash, []]

    def _add_interpretation_rank(self, obj, objhash):
        if "rank" not in obj or type(obj["rank"]) != int:
            rank = obj["@index"] - 1
            obj["rank"] = rank
        return [obj, objhash, []]
    
    def _wrap_uncertainty(self, obj, objhash) :
        objid = obj["@id"]
        # Deal with uncertainty
        pvals = {}
        keys_to_be_deleted = []
        for key,value in obj.items() :
            if (re.search(r"^uncertainty\$", key, re.IGNORECASE)) :
                pvals["hasValue"] = value
                keys_to_be_deleted.append(key)
            elif (re.search(r"^uncertainty", key, re.IGNORECASE)) :
                pvals[key] = value
                keys_to_be_deleted.append(key)

        for key in keys_to_be_deleted:
            del obj[key]

        if len(pvals.values()) > 0 :
            uncid = "" + str(objid) + ".Uncertainty"
            obj["hasUncertainty"] = uncid
            uncertainty = {
                "@id": uncid,
                "@category": "Uncertainty"
            }
            for prop,value in pvals.items() :
                uncertainty[prop] = value
            
            objhash[uncid] = uncertainty
            return [obj, objhash, [uncid]]
        
        return [obj, objhash, []]
    
    def _add_found_in_table(self, obj, objhash) :
        obj["foundInTable"] = obj["@parent"]["@id"]
        return [obj, objhash, []]
    
    def _add_found_in_dataset(self, obj, objhash) :
        parent = obj["@parent"]
        top = parent
        while (parent) :
            top = parent
            parent = parent["@parent"]
        obj["foundInDataset"] = top["@id"]
        return [obj, objhash, []]
        
    # Unroll the list to a rdf first/rest structure
    def _unroll_values_list_to_rdf(self, lst: list, dtype):
        listitems = []
        for idx, item in enumerate(lst):
            listitems.append(Literal(item, datatype=(XSD[dtype] if dtype in XSD else None)))

        listid = BNode()
        list = Collection(self.graph, listid, listitems)
        return listid

    def _parse_changes(self, changes, parent=None):
        newChanges = []
        if not isinstance(changes, list):
            changes = [changes]
        
        for change in changes:
            for name in change.keys():
                notes = change[name] or []
                newChange = {
                    "name": name,
                    "notes": [item[0] for item in notes]
                }
                newChanges.append(newChange)
        return newChanges
    

    def _add_variable_values(self, obj, objhash) :
        if "filename" in obj["@parent"]:
            csvname = obj["@parent"]["filename"]
        else:
            csvname = re.sub(r"^.*\.", "", obj["@parent"]["@id"]) + ".csv"

        if "number" not in obj:
            obj["number"] = obj["@index"]
        if type(obj["number"]) is str:
            obj["number"] = int(obj["number"])
        if not isinstance(obj["number"], list):
            obj["number"] = [obj["number"]]
        
        indices = [int(col)-1 for col in obj["number"]]
        if csvname in self.lipd_csvs:
            df = self.lipd_csvs[csvname]
            values = []
            if len(indices) == 1:
                if indices[0] < len(df.columns):
                    df_values = df[indices[0]]
                    values = df_values.tolist()
                    #dtype = "float" if df_values.dtypes == "float64" else "string"
            else:
                df_values = df[indices]
                values = df_values.values.tolist()
                #dtype = "float" if df_values[0].dtypes == "float64" else "string"

            # TODO: Dumping to json string for now. 
            # - Compressing string if it is too long (otherwise loading to RDF hangs)
            valstring = json.dumps(values)
            #if len(valstring) > 1000000:
            #    valstring =json.dumps({"base64_zlib": zip_string(valstring)})
            obj["hasValues"] = valstring

            # rdf:Seq doesn't seem to be importing well in GraphDB            
            #bnodeid = self._unroll_values_list_to_rdf(values, dtype)
            #obj["hasValues"] = bnodeid

            return [obj, objhash, []]
        return [obj, objhash, []]

    def _add_standard_variable(self, obj, objhash) :
        if "variableName" in obj:
            name = obj["variableName"]
            synonyms = SYNONYMS["VARIABLES"]["PaleoVariable"]
            if type(name) is str and name.lower() in synonyms:
                obj["hasStandardVariable"] = synonyms[name.lower()]["id"]
                # Only add object label in the current graph if set
                if self.add_labels:
                    label = synonyms[name.lower()]["label"]                        
                    self._set_object_label(obj["hasStandardVariable"], label)

        return [obj, objhash, []]

    def _stringify_column_numbers_array(self, obj, objhash):
        if "number" in obj and isinstance(obj["number"], list) and len(obj["number"]) > 1:
            obj["hasColumnNumber"] = json.dumps(obj["number"])
            del obj["number"]
        return [obj, objhash, []]
    
    def _modify_structure_if_needed(self, obj, objhash, schema) :
        if (("@fromJson" in schema)) :
            for func in schema["@fromJson"]: 
                fn = getattr(self, func)
                (obj, objhash, newids) = fn(obj, objhash)
                for newid in newids : 
                    if ((newid in objhash)) :
                        newobj = objhash[newid]
                        if (type(newobj) is dict) and ("@category" in newobj) :
                            newschid = newobj["@category"]
                            newschema =  self.schema[newschid] if (newschid in self.schema) else {}
                            (objhash[newid], objhash) = self._modify_structure_if_needed(newobj, objhash, newschema)
        
        return [obj, objhash]
    
    def _get_compound_key_id(self, compound_key, obj) :
        tobj = obj
        for key in compound_key : 
            if ((type(tobj) is dict) and (key in tobj)) :
                tobj = tobj[key]
            else : 
                return None
            
        if not type(tobj) is dict:
            return tobj
        
        return None
    
    def _get_binding_key_id(self, key, obj) :
        key_options = key.split("|")
        for optkey in key_options : 
            compound_key = optkey.split(".")
            keyid = self._get_compound_key_id(compound_key, obj)
            if (keyid) :
                return keyid
        return uniqid()
    
    def _get_function_key_id(self, fn, arg, curobjid) :
        if (fn == "trunc") :
            return curobjid[0:0 + len(curobjid) - int(arg)]
        elif (fn == "uniqid") :
            return str(curobjid) + uniqid(arg)
        return curobjid
    
    def _create_id_from_pattern(self, pattern, obj) :
        objid = ""
        for key in pattern : 
            m = re.search(r"{(.+)}", key)
            if m and len(m.groups()) > 0 :
                objid += str(self._get_binding_key_id(m.groups()[0], obj))
            else : 
                m = re.search(r"_(.+)\((.*)\)", key)
                if m and len(m.groups()) > 1:
                    fn = m.groups()[0]
                    arg = m.groups()[1]
                    objid = str(self._get_function_key_id(fn, arg, objid))
                else : 
                    objid += str(key)
        return objid
    
    def _fix_title(self, titleid) :
        return titleid.replace(r"@\\x{FFFD}@u", '_')
    
    def _get_object_id(self, obj, category, schema) :
        if type(obj) is dict:
            objid =  "Unknown." + uniqid(category)
        else:
            objid = ucfirst(obj).replace(" ", "_")
        if (("@id" in schema)) :
            objid = self._create_id_from_pattern(schema["@id"], obj)
        
        return self._fix_title(objid)
    
    def _map_lipd_to_json(self, obj, parent, index, category, schemaname, hash) :
        schema =  self.schema[schemaname] if (schemaname in self.schema) else {}
        
        if not type(obj) is dict:
            return obj
        
        obj["@parent"] = parent
        obj["@index"] = index
        obj["@schema"] = schemaname
        
        objid = self._get_object_id(obj, category, schema)
        if (("@id" in obj)) :
            objid = obj["@id"]
        if ((objid in hash)) :
            return objid
        obj["@id"] = objid
        
        (obj, hash) = self._modify_structure_if_needed(obj, hash, schema)
        
        if ("@category" in obj) :
            category = obj["@category"]
        hash[objid] = {
            "@id": objid,
            "@category" : category,
            "@schema" : schemaname
        }
        item = hash[objid]
        
        if type(obj) is dict :
            for propkey,value in obj.items() :
                if (propkey[0] == "@") :
                    continue
                
                if propkey in BLACKLIST :
                    continue
                
                details = {}
                pname = propkey
                if propkey in schema :
                    details = schema[propkey]
                    pname =  details["name"] if ("name" in details) else propkey
                
                dtype =  details["type"] if ("type" in details) else None
                cat =  details["category"] if ("category" in details) else None
                sch =  details["schema"] if ("schema" in details) else None
                fromJson =  details["fromJson"] if ("fromJson" in details) else None
                if (sch and not cat) :
                    cat = sch
                if (fromJson) :
                    fn = getattr(self, fromJson)
                    value = fn(value, obj)
                    if (not value) :
                        continue
                    
                    if (pname) :
                        if (type(value) is list) :
                            index = 1
                            for subvalue in value:                              
                                if (type(subvalue) is dict):
                                    if propkey not in item:
                                        item[propkey] = []
                                    item[propkey].append(self._map_lipd_to_json(subvalue, obj, index, cat, sch, hash))
                                    index+=1
                        else : 
                            if (type(value) is dict):
                                item[propkey] = self._map_lipd_to_json(value, obj, None, cat, sch, hash)
                            else : 
                                item[propkey] = value
                            
                        
                    else : 
                        if (type(value) is dict):
                            for subpropkey,subvalue in value.items() :
                                item[subpropkey] = subvalue
                    continue
                
                if (not pname) :
                    continue
                
                if (type(value) is list):
                    index = 1
                    for subvalue in value: 
                        if propkey not in item:
                            item[propkey] = []                    
                        item[propkey].append(self._map_lipd_to_json(subvalue, obj, index, cat, sch, hash))
                        index+=1
                    
                else : 
                    if (type(value) is dict):
                        if propkey not in item:
                            item[propkey] = []                      
                        item[propkey].append(self._map_lipd_to_json(value, obj, None, cat, sch, hash))
                    else : 
                        if (dtype == "Individual") :
                            item[propkey] = value
                            if (not (value in hash)) :
                                hash[value] = {
                                    "@id" : value,
                                    "@category" : cat,
                                    "@schema" : sch
                                }
                        else : 
                            item[propkey] = value

        hash[objid] = item
        return objid
    
    def _guess_data_value_type(self, val) :
        value = str(val)
        if (re.search(r"^-?\d+$", value)) :
            return "float" #"integer"
        
        if (re.search(r"^-?\d+\.\d+$", value)) :
            return "float"
        
        if (re.search(r"^[2][0-9]{3}[-][0-1][0-9][-][0-3][0-9]( |T)[0-9]{2}:[0-9]{2}:[0-9]{2}", value)) :
            return "datetime"
                
        if (re.search(r"^[2][0-9]{3}[-][0-1][0-9][-][0-3][0-9]", value)) :
            return "date"
        
        if (re.search(r"^(true|false)$", value, re.IGNORECASE)) :
            return "boolean"
        
        if (re.search(r"^http", value)) :
            return "url"
        
        #if (re.search(r"^.+@.+\..+", value)) :
        #    return "Email"
        
        if (re.search(r"^\".+\"$", value)) :
            return "string"
        
        if (re.search(r"^'.+'$", value)) :
            return "string"
        
        return "string"
    
    def _guessValueType(self, value) :
        if value:
            if type(value) is list :
                for subvalue in value :
                    return self._guessValueType(subvalue)
            elif type(value) is dict : 
                return "Individual"
            
            else : 
                valtype = self._guess_data_value_type(value)
                return valtype

        return "string"
    
    def _get_property_details(self, key, schema, value) :
        pname = key
        details = {
            "name": pname
        }
        if (key in schema) and ("@@processed" in schema[key]) :
            return schema[key]
        
        # Get details from schema
        if (key in schema) :
            for skey,svalue in schema[key].items() :
                details[skey] = svalue
        
        if (("schema" in details)) :
            details["type"] = "Individual"
        
        pname = lcfirst(details["name"])
        
        # Get more details from the property definition (if it exists)
        """
        newname = resolveProperty(pname)
        if (newname) :
            details["type"] = getOntPropertyRange(newname)
            details["name"] = newname
        """ 
        
        if (not ("type" in details)) :
            details["type"] = self._guessValueType(value)
            if (not ("type" in details)) :
                details["type"] = "string"

        details["@@processed"] = True
        schema[key] = details
        return details
    
    # Create individual
    def _create_individual(self, objid) :
        return self.namespace + sanitizeId(objid)
    
    # Create class
    def _create_class(self, category) :
        return ONTONS + sanitizeId(category)
    
    # Create property
    def _create_property(self, prop, dtype, cat, multiple) :
        nsprop = prop.split(":", 2)
        ns = ONTONS
        if len(nsprop) > 1 :
            prefix = nsprop[0]
            if prefix in NAMESPACES:
                ns = NAMESPACES[prefix]
            prop = nsprop[1]
        return [ ns + lcfirst(sanitizeId(prop)), dtype, cat, multiple ]
    
    # Set individual classes
    def _set_individual_classes(self, objid, category, extracats) :
        if objid and category:
            self.graph.add((
                URIRef(objid),
                RDF.type,
                URIRef(category),
                URIRef(self.graphurl)
            ))
        for ecat in extracats:
            if objid and ecat:
                self.graph.add((
                    URIRef(objid),
                    RDF.type,
                    URIRef(self._create_class(ecat)),
                    URIRef(self.graphurl)
                ))
    
    # Set object label
    def _set_object_label(self, objid, label) :
        if objid and label:
            self.graph.add((
                URIRef(objid),
                RDFS.label,
                Literal(label),
                URIRef(self.graphurl)
            ))

    # Set property value
    def _set_property_value( self, objid, prop, value ):
        if (type(value) is list) :
            for subvalue in value : 
                self._set_property_value(objid, prop, subvalue)
            return

        (propid, dtype, cat, multiple) = prop
        if objid and value:
            objitem = None

            if dtype == "float" or dtype == "integer":
                if re.search("^.*[^a-zA-Z]?nan[^a-zA-Z]?.*$", str(value).lower()):
                    return
                if re.search("^.*[^a-zA-Z]?na[^a-zA-Z]?.*$", str(value).lower()):
                    return

            if type(value) is str:
                value = escape(value)

            if dtype == "boolean":
                value = str(value).lower()
                if value != "true":
                    value = "false"
            
            elif dtype == "float":
                m = re.search(r"(\-?\d+\.?\d*)", str(value))
                if m:
                    value = m.group(1)
                else:
                    value = 0.0

            elif dtype == "integer":
                m = re.search(r"(\-?\d+)", str(value))
                if m:
                    value = m.group(1)
                else:
                    value = 0

            if dtype == "Individual":
                value = self._create_individual(value)
                objitem = URIRef(value)
            
            elif dtype == "EnumeratedIndividual":
                objitem = URIRef(value)
            
            elif dtype == "List":
                objitem = value
            
            else:
                objitem = Literal(value, datatype=(XSD[dtype] if dtype in XSD else None))

            # FIXME: Do not add if property doesn't allow multiple values and a value already exists
            if not multiple:
                existing = list(self.graph.triples((URIRef(objid), URIRef(propid), None)))
                if len(existing) > 0:
                    return
            
            self.graph.add((
                URIRef(objid),
                URIRef(propid),
                objitem,
                URIRef(self.graphurl)
            ))
    
    def _create_individual_full(self, obj) :
        category = obj["@category"]
        extracats =  obj["@extracats"] if ("@extracats" in obj) else {}
        schemaname =  obj["@schema"] if ("@schema" in obj) else category
        schema =  self.schema[schemaname] if (schemaname in self.schema) else {}
        objid = obj["@id"]
        if (not objid) :
            return
        
        # Create category
        if (category) :
            category = self._create_class(category)
        
        objid = self._create_individual(objid)
        
        # Set Individual classes
        self._set_individual_classes(objid, category, extracats)
        
        for key,value in obj.items() :
            if (key[0] == "@") :
                continue
            
            details = self._get_property_details(key, schema, value)
            prop = details["name"]
            dtype = details["type"]
            synonyms = details.get("synonyms", {})
            cat =  details["category"] if ("category" in details) else None
            sch =  details["schema"] if ("schema" in details) else None
            if (sch and not cat) :
                cat = sch
            
            fromJson =  details["fromJson"] if ("fromJson" in details) else None
            multiple =  details["multiple"] if ("multiple" in details) else False
            if (not prop) :
                continue
                
            # Create Property
            propDI = self._create_property(prop, dtype, cat, multiple)

            # Set property value
            if dtype == "Individual":
                if type(value) is str and synonyms:
                    # If the value is a string and there are synonyms for this Individual
                    if value.lower() in synonyms:
                        # If we have a synonym-mapping for the value to an Individual
                        
                        propDI[1] = "EnumeratedIndividual" # Rename property type to be an enumeration
                        synid = synonyms[value.lower()]["id"]
                        if not self.standardize:
                            # If we don't want to standardize, then create a unique id for the individual
                            synid += "." + uniqid()
                        self._set_property_value(objid, propDI, synid)
                        # Only add object label in the current graph if set
                        if self.add_labels:
                            if self.standardize:
                                # Set the standard label for the individual
                                label = synonyms[value.lower()]["label"]
                            else:
                                # Set the user label for the individual
                                label = value
                            self._set_object_label(synid, label)
                    else:
                        # We don't have a synonym-mapping for the value. Create an individual and set its label to the value
                        propDI[1] = "EnumeratedIndividual"
                        synid = self._create_individual(value) + "." + uniqid()
                        self._set_property_value(objid, propDI, synid)
                        self._set_object_label(synid, value)
                else:
                    # There are no synonyms, and value is not a string. Just use it directly
                    self._set_property_value(objid, propDI, value)
            elif type(value) is dict:
                self._set_property_value(objid, propDI, value)
            else : 
                if (dtype == "File") :
                    # Enable this ?
                    """
                    fileid = uploadFile(value)
                    if (fileid) :
                        protectIndividual(fileid)
                        data = set_property(data, propDI, fileid)
                    """

                else : 
                    self._set_property_value(objid, propDI, value)

    def _find_files_with_extension(self, directory, extension):
        myregexobj = re.compile('\.'+extension+'$')
        try: 
            for entry in os.scandir(directory):
                if entry.is_file() and myregexobj.search(entry.path): 
                    yield entry.path, entry.name
                elif entry.is_dir():   # if its a directory, then repeat process as a nested function
                    yield from self._find_files_with_extension(entry.path, extension)
        except OSError as ose:
            print('Cannot access ' + directory +'. Probably a permissions error ', ose)

    def _load_lipd_json_to_graph(self, jsonpath, url=None):
        self.graph = ConjunctiveGraph()
        objhash = {}
        
        with open(jsonpath) as f:
            obj = json.load(f)
            if "dataSetName" in obj:
                self.graphurl = NSURL + "/" + sanitizeId(obj["dataSetName"])
            
            self._map_lipd_to_json(obj, None, None, "Dataset", "Dataset", objhash)
            if url:
                objhash[obj["@id"]]["hasUrl"] = url
            else:
                objhash[obj["@id"]]["hasUrl"] = DATAURL + "/" + obj["@id"] + ".lpd"

            for key, item in objhash.items():
                self._create_individual_full(item)