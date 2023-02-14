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

from rdflib.graph import ConjunctiveGraph, Literal, RDF, URIRef, BNode, Collection
from rdflib.namespace import XSD

from io import BytesIO
from urllib.request import urlopen
from urllib.parse import urlparse, urlunparse, quote

from .globals.urls import NSURL, DATAURL, ONTONS, NAMESPACES
from .globals.blacklist import BLACKLIST
from .globals.schema import SCHEMA

from .utils import expand_schema, ucfirst, lcfirst, camelCase, unCamelCase, escape, uniqid, sanitizeId

class LipdToRDF:
    """
    The LipdToRDF class helps in converting a LiPD file to an RDF Graph. 
    It uses the SCHEMA dictionary (from globals/schema.py) to do the conversion

    Parameters
    ----------
    collection_id : str
        (Optional) set a collection id for the lipd file
    """

    def __init__(self, collection_id=None):
        self.graph = ConjunctiveGraph()
        self.lipd_csvs = {}
        self.collection_id = collection_id
        self.graphurl = NSURL
        self.namespace = NSURL + "#"
        self.schema = expand_schema(copy.deepcopy(SCHEMA))

        if self.collection_id:
            self.namespace = NSURL + "/" + collection_id + "#"        


    def convert(self, lipdpath, topath, type="rdf"):
        '''Convert LiPD file to RDF (or Pickled Graph)

        Parameters
        ----------

        lipdpath : str
            path to lipd file (the path could also be a url)

        topath : str
            path to the output file

        type : str
            the output file type : rdf or pickle (we store the pickled rdf graph for efficiency sometimes)
        '''

        self.graph = ConjunctiveGraph()
        
        lpdname = os.path.basename(lipdpath).replace(".lpd", "")
        lpdname = re.sub("\?.+$", "", lpdname)

        self.graphurl = NSURL + "/" + lpdname
        if self.collection_id:
            self.graphurl = NSURL + "/" + self.collection_id + "/" + lpdname

        with tempfile.TemporaryDirectory(prefix="lipd_to_rdf_") as tmpdir:
            self._unzip_lipd_file(lipdpath, tmpdir)
            jsons = self._find_files_with_extension(tmpdir, 'jsonld')
            for jsonpath, _ in jsons:
                jsondir = os.path.dirname(jsonpath)
                csvs = self._find_files_with_extension(jsondir, 'csv')
                self.lipd_csvs = {}
                for csvpath, _ in csvs:
                    csvname = os.path.basename(csvpath)        
                    self.lipd_csvs[csvname] = pd.read_csv(csvpath, header=None)
                self._load_lipd_json_to_graph(jsonpath)                    
                
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

    def _add_extra_dataset_properties(self, obj, objhash) :
        _REQUEST = {} # This is not really used here is it ?
        for key,value in _REQUEST.items() :
            m = re.search(r"^extra_(.+)", key)
            if m is not None:
                prop = m.groups()[0]
                if (not (prop in obj)) :
                    obj[prop] = value
        return [obj, objhash, []]

    def _parse_persons_string(self, authstring, parent = None) :
        authors = []
        if (type(authstring) is list) :
            return self._parse_persons(authstring, None)
        
        if (re.search(r"\s*\s*", authstring)) :
            auths = re.split(r"\s*\s*", authstring)
            for auth in auths:            
                authors.append(self._parse_person(auth))
            
        else : 
            if (re.search(r".*,.*,.*", authstring)) :
                auths = re.split(r"\s*,\s*", authstring)
                i = 0
                while ( i < len(auths) ) :
                    name = auths[i]
                    if not re.search(r"\s", name) :
                        i+=1
                        name = str(str(auths[i]) + " ") + str(name)
                    authors.append({"name" : name})
                    i+=1
                
            else : 
                m = re.search(r"(.+),(.+)", authstring)
                if m is not None:
                    authors.append({"name" : str(str(m.groups()[1]) + " ") + str(m.groups()[0])})
                else : 
                    authors.append({"name" : authstring})
        return authors


    def _parse_person(self, auth, parent = None) :
        authname = auth
        if (type(auth) is dict) :
            authname = auth["name"]
        if authname:
            m = re.search(r"(.+)\s*,\s*(.+)", authname)
            if m is not None:
                return {"name" : str(str(m.groups()[1]) + " ") + str(m.groups()[0])}
            else : 
                return {"name" : authname}

        
    def _parse_persons(self, auths, parent = None) :
        authors = []
        if (not type(auths) is list) :
            return None
        
        for auth in auths: 
            authors.append(self._parse_person(auth, parent))
        return authors

    def _parse_location(self, geo, parent = None) :
        ngeo = {}
        ngeo["locationType"] = geo["type"] if "type" in geo else None
        ngeo["coordinatesFor"] = parent["@id"]
        coords = geo["geometry"]["coordinates"]
        if (coords and len(coords) > 0) :
            ngeo["coordinates"] = str(str(coords[1]) + ",") + str(coords[0])
            ngeo["wgs84:lat"] = coords[1]
            ngeo["wgs84:long"] = coords[0]
            if (len(coords) > 2) :
                ngeo["wgs84:alt"] = coords[2]
        
        if "properties" in geo and isinstance(geo["properties"], dict) :
            for key,value in geo["properties"].items() :
                ngeo[key] = value
        elif isinstance(geo, dict) :
            for key,value in geo.items() :
                if key != "geometry":
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


    def _set_variable_category(self, obj, objhash) :
        # Default category
        obj["@category"] = "MeasuredVariable"
        obj["@schema"] = "Variable"
        if (("variableType" in obj)) :
            varcat = str(obj["variableType"]) + "Variable"
            obj["@category"] = ucfirst(varcat)
            del obj["variableType"]
        else : 
            if (("calibration" in obj)) :
                obj["@category"] = "InferredVariable"
        return [obj, objhash, []]
    
    def _get_lipd_archive_type(self, archiveType) :
        return unCamelCase(archiveType)

    def _get_archive_type(self, id, latitude) :
        if not id:
            return None
        id = id.lower()
        if (id == "tree") :
            return "Wood"
        else : 
            if (id == "bivalve") :
                return "MolluskShell"
            else : 
                if (id == "borehole") :
                    if (latitude > 65 or latitude < -65) :
                        return "GlacierIce"
                    else : 
                        return "Rock"
        return camelCase(id)
    
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
        id += "." + str(iobj["variablename"])
        return id
    
    def _set_inter_variable_links(self, obj, objhash) :
        depthcol = None
        vobjhash = {}
        if "columns" not in obj:
            return [obj, objhash, []]

        for col in obj["columns"] : 
            vobjhash[col["variableName"].lower()] = self._get_variable_id(col, obj["@id"])
        
        depthcol =  vobjhash["depth"] if ("depth" in vobjhash) else None
        for col in obj["columns"] : 
            thiscol = self._get_variable_id(col, obj["@id"])
            if (("inferredFrom" in col)) :
                infcol = col["inferredFrom"].lower()
                if ((infcol in vobjhash)) :
                    col["inferredFrom"] = vobjhash[infcol]
                
            if (depthcol and thiscol != depthcol) :
                col["takenAtDepth"] = depthcol
        return [obj, objhash, []]
    
    def _create_proxy_system(self, obj, hash) :
        varid = obj["@id"]
        # Deal with proxies
        proxyobs = None
        sampleid = None
        if ("proxy" in obj and obj["proxy"]) :
            proxyobs = obj["proxy"]
            del obj["proxy"]
        elif ("OnProxyObservationProperty" in obj and obj["OnProxyObservationProperty"]) :
            proxyobs = obj["OnProxyObservationProperty"]
            del obj["OnProxyObservationProperty"]
        elif ("ProxyObservationType" in obj and obj["ProxyObservationType"]) :
            proxyobs = obj["ProxyObservationType"]
        elif ("proxyObservationType" in obj and obj["proxyObservationType"]) :
            proxyobs = obj["proxyObservationType"]
        
        vartype = obj["@category"]
        if (vartype and vartype == "MeasuredVariable") :
            # Get the archive type
            dsname = self._get_parent_property(obj, "dataSetName")
            geo = self._get_parent_property(obj, "geo")
            latitude = 0
            if (("geometry" in geo) and len(geo["geometry"]["coordinates"]) > 1) :
                latitude = geo["geometry"]["coordinates"][1]
            
            archivetype = self._get_parent_property(obj, "archiveType")
            if (not archivetype) :
                archivetype = self._get_parent_property(obj, "archive")
            
            archivetype = self._get_archive_type(archivetype, latitude)
            # Create sample (archive)
            if (not ("physicalSample" in obj)) :
                cname = self._get_parent_property(obj, "collectionName")
                if (cname) :
                    obj["physicalSample"] = {"name" : cname}
                
            
            if (("physicalSample" in obj)) :
                sample = obj["physicalSample"]
                sampleid =  sample["hasname"] if ("hasname" in sample) else sample["name"]
                if (("hasidentifier" in sample)) :
                    sampleid += "." + str(sample["hasidentifier"])
                else : 
                    if (("identifier" in sample)) :
                        sampleid += "." + str(sample["identifier"])
                if (not (sampleid in hash)) :
                    sampleobj = {
                        "@id" : sampleid, 
                        "@category" : "PhysicalSample", 
                        "@extracats" : [archivetype]
                    }
                    for pkey,pval in sample.items() :
                        sampleobj[pkey] = pval

                    hash[sampleid] = sampleobj
                del obj["physicalSample"]
            
            if type(proxyobs) is list:
                proxyobs = proxyobs[0]

            observationid = self._get_observation(proxyobs)
            #obj["proxy"])
            # Create sensor
            sensorid = ((str(observationid) + ".") if observationid is not None else "") + "DefaultSensor"
            sensor = {
                "@id" : sensorid, 
                "@category" : "Sensor"
            }
            if (("archiveGenus" in obj)) :
                sensor["sensorGenus"] = obj["archiveGenus"]
                sensorid = ucfirst(sensor["sensorGenus"].lower())
                del obj["archiveGenus"]
                if (("archiveSpecies" in obj)) :
                    sensor["sensorSpecies"] = obj["archiveSpecies"]
                    sensorid += " " + sensor["sensorSpecies"].lower()
                    del obj["archiveSpecies"]
                
            
            if (("sensorGenus" in obj)) :
                sensor["sensorGenus"] = obj["sensorGenus"]
                sensorid = ucfirst(sensor["sensorGenus"].lower())
                del obj["sensorGenus"]
                if (("sensorSpecies" in obj)) :
                    sensor["sensorSpecies"] = obj["sensorSpecies"]
                    sensorid += " " + sensor["sensorSpecies"].lower()
                    del obj["sensorSpecies"]
                
            
            if (not (sensorid in hash)) :
                sensor["@id"] = sensorid
                sensor["@category"] = self._guess_sensor_type(archivetype, observationid, sensor)
                hash[sensorid] = sensor
            
            #$hash[$sampleid]["ProxySensorType"] = $sensorid
            # Create a proxy
            #$proxyid = $obj["@id"].".$archivetype.$sensorid.ProxySystem"
            proxyid = "ProxySystem." + str(archivetype)
            if (sensorid) :
                proxyid += "." + str(sensorid) + ""
            
            if (observationid) :
                proxyid += "." + str(observationid) + ""
            
            # TODO: $proxyid .= ".$chronmodel"
            # TODO: $proxyid .= ".$paleomodel"
            if (not (proxyid in hash)) :
                proxy = {
                    "@id" : proxyid, 
                    "@category" : "ProxySystem", 
                    "ProxySensorType" : sensorid,
                    "ProxyArchiveType" : archivetype,
                    "ProxyObservationType" : observationid
                }
                if (("proxySystemModel" in obj)) :
                    proxymodelid = "" + str(proxyid) + ".Model"
                    # TODO: Create proxy sensor/archive/observation models
                    proxymodel = {
                        "@id" : proxymodelid, 
                        "@category" : "ProxySystemModel", 
                        "name" : observationid,
                        "hasProxySensorModel" : "" + str(sensorid) + ".Model",
                        "hasProxyArchiveModel" : "" + str(archivetype) + ".Model",
                        "hasProxyObservationModel" : "" + str(observationid) + ".Model"
                    }
                    proxy["modeledBy"] = proxymodelid
                    hash[proxymodelid] = proxymodel
                    del obj["proxySystemModel"]
                hash[proxyid] = proxy
            
            obj["measuredOn"] = sampleid
            obj["ProxyObservationType"] = observationid
            obj["hasProxySystem"] = proxyid
            if "proxy" in obj:
                del obj["proxy"]
            return [obj, hash, [sampleid, proxyid, sensorid]]
        
        return [obj, hash, []]
    
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
    
    # Unroll the list to a rdf first/rest structure
    def _unroll_values_list_to_rdf(self, lst: list, dtype):
        listitems = []
        for idx, item in enumerate(lst):
            listitems.append(Literal(item, datatype=(XSD[dtype] if dtype in XSD else None)))

        listid = BNode()
        list = Collection(self.graph, listid, listitems)
        return listid


    def _add_variable_values(self, obj, objhash) :
        csvname = obj["@parent"]["@id"] + ".csv"
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
                subobject =  details["subobject"] if ("subobject" in details) else False
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
                                if (type(value) is dict):
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
                
                if (subobject) :
                    if "@subobjects" not in item:
                        item["@subobjects"] = []
                    item["@subobjects"].append({ propkey : value })
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
    def _create_property(self, prop, dtype, cat, icon, multiple) :
        nsprop = prop.split(":", 2)
        ns = ONTONS
        if len(nsprop) > 1 :
            prefix = nsprop[0]
            if prefix in NAMESPACES:
                ns = NAMESPACES[prefix]
            prop = nsprop[1]
        return [ ns + lcfirst(sanitizeId(prop)), dtype ]
    
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
    
    # Set property value
    def _set_property( self, objid, prop, value ):
        if (type(value) is list) :
            for subvalue in value : 
                self._set_property(objid, prop, subvalue)
            return

        (propid, dtype) = prop
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
            
            elif dtype == "List":
                objitem = value
            
            else:
                objitem = Literal(value, datatype=(XSD[dtype] if dtype in XSD else None))

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
        
        subobjects = {}
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
            icon =  details["icon"] if ("icon" in details) else None
            cat =  details["category"] if ("category" in details) else None
            sch =  details["schema"] if ("schema" in details) else None
            if (sch and not cat) :
                cat = sch
            
            fromJson =  details["fromJson"] if ("fromJson" in details) else None
            multiple =  details["multiple"] if ("multiple" in details) else False
            subobject =  details["subobject"] if ("subobject" in details) else False
            if (not prop) :
                continue
                
            # Create Property
            propDI = self._create_property(prop, dtype, cat, icon, multiple)

            # Set property value
            if (dtype == "Individual" or type(value) is dict) :
                self._set_property(objid, propDI, value)
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
                    self._set_property(objid, propDI, value)

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
        except FileNotFoundError as fnf:
            print(directory +' not found ', fnf)

    def _load_lipd_json_to_graph(self, jsonpath, url=None):
        self.graph = ConjunctiveGraph()
        objhash = {}
        
        with open(jsonpath) as f:
            obj = json.load(f)
            
            self._map_lipd_to_json(obj, None, None, "Dataset", "Dataset", objhash)
            if url:
                objhash[obj["@id"]]["hasUrl"] = url
            elif self.collection_id:
                objhash[obj["@id"]]["hasUrl"] = DATAURL + "/" + self.collection_id + "/" + obj["@id"] + ".lpd"
            else:
                objhash[obj["@id"]]["hasUrl"] = DATAURL + "/" + obj["@id"] + ".lpd"

            for key, item in objhash.items():
                self._create_individual_full(item)