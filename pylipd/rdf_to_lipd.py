"""
The RDFToLiPD class helps in converting an RDF Graph to a LiPD file.
It uses the SCHEMA dictionary (from globals/schema.py) to do the conversion
"""

import copy
import os
import re
import csv
import bagit
import json
import tempfile
import zipfile

from rdflib.graph import ConjunctiveGraph, URIRef

from .globals.urls import NSURL
from .globals.blacklist import REVERSE_BLACKLIST
from .globals.schema import SCHEMA

from .utils import ucfirst, lcfirst, unCamelCase, unzip_string

class RDFToLiPD:
    """
    The RDFToLiPD class helps in converting an RDF Graph to a LiPD file.
    It uses the SCHEMA dictionary (from globals/schema.py) to do the conversion
    """    
    def __init__(self, graph):
        self.graph = graph
        self.lipd_csvs = {}
        self.graphurl = NSURL
        self.namespace = NSURL + "#"

    def convert(self, dsname, lipdfile):
        '''Convert RDF graph to a LiPD file

        Parameters
        ----------

        graph : rdflib.ConjunctiveGraph
            the RDF graph object

        '''
        lipd = self.convert_to_json(dsname)

        with tempfile.TemporaryDirectory(prefix="rdf_to_lipd_") as tmpdir:
            # Create a temporary data directory
            datadir = f"{tmpdir}/{dsname}"
            os.makedirs(datadir)

            # Create the csv files and metadata jsonld
            self._create_csvs(lipd, datadir)
            with(open(f"{datadir}/metadata.jsonld", "w")) as f:
                json.dump(lipd, f, indent=4, default=str)
            
            # Convert data directory to a bag
            bagit.make_bag(datadir, checksums=['md5'])

            # Zip the bag
            self._zip_directory(datadir, lipdfile)

        return lipd

    def convert_to_json(self, dsname):
        '''Convert RDF graph to a LiPD file

        Parameters
        ----------

        graph : rdflib.ConjunctiveGraph
            the RDF graph object

        '''
        self.schema = copy.deepcopy(SCHEMA)
        self.rschema = self._get_schema_reverse_map()

        self.allfacts = {}
        self._get_indexed_facts(self.namespace + dsname)
        
        lipd = self._convert_to_lipd(self.namespace + dsname, "Dataset", "Dataset", pagesdone={})
        lipd = self._post_processing(lipd)
        return lipd

    def _get_table_data(self, table):
        csvdata = []
        numrows = 0
        
        table["columns"] = sorted(table["columns"], key=lambda x: x["number"] if ("number" in x and type(x["number"]) is int) else 99999)

        for col in table["columns"]:
            if "values" in col:
                numrows = len(col["values"])
                break
        
        for rowidx in range(numrows):
            row = []
            for col in table["columns"]:
                if "values" in col:
                    colindices = []
                    if "number" in col:
                        colnum = col["number"]
                        colindices.append(colnum)
                    else:
                        colindices.append(1)
                    
                    for colindex in colindices:
                        if type(colindex) is list:
                            sorted(colindex)
                            firstidx = colindex[0]
                            for subindex in colindex:
                                idx = subindex - 1
                                if idx >= len(row):
                                    row.extend([""] * (idx - len(row) + 1))
                                row[idx] = col["values"][rowidx][subindex-firstidx]

                        else:
                            idx = colindex - 1
                            if idx >= len(row):
                                row.extend([""] * (idx - len(row) + 1))
                            row[idx] = col["values"][rowidx]

            csvdata.append(row)

        # Delete the values field (since we've extracted the csv data)
        for col in table["columns"]:
            if "values" in col:
                del col["values"]

        return csvdata
    
    def _create_csvs(self, lipd, datadir):
        csvs = {}
        datakeys = ["paleoData", "chronData"]
        for datakey in datakeys:
            if datakey in lipd:
                for data in lipd[datakey]:
                    if "measurementTable" in data:
                        for table in data["measurementTable"]:
                            csvs[table["filename"]] = self._get_table_data(table)
                    if "model" in data:
                        for model in data["model"]:
                            if "ensembleTable" in model:
                                for table in model["ensembleTable"]:
                                    csvs[table["filename"]] = self._get_table_data(table)
                            if "summaryTable" in model:
                                for table in model["summaryTable"]:
                                    csvs[table["filename"]] = self._get_table_data(table)

        for csvname, csvdata in csvs.items():
            # writing to csv file 
            with open(f"{datadir}/{csvname}", 'w') as csvfile: 
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerows(csvdata)


    def _zip_directory(self, datadir, lipdfile):
        # Zip the bag
        with zipfile.ZipFile(lipdfile, 'w') as zipf:
            for root, dirs, files in os.walk(datadir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(datadir, '..')))

    '''
    def _zip_lipd_dir(self, lipddir, lipdfile):
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
    '''
    
    def _get_property_details(self, pname, schema) :
        details = { "name": pname }
        # Create property
        if schema and (pname in schema) :
            for skey,svalue in schema[pname].items() :
                details[skey] = svalue
        return details

    def _get_rdf_property_details(self, pname, fullkey, schema) :
        key = pname
        pname = lcfirst(pname)
        details = { "name": pname }
		# Check for full key in schema
        if schema and (fullkey in schema):
            for ind, svalue in schema[fullkey].items():
                details[ind] = svalue
		
        # Or check for just pname in schema
        elif schema and (key in schema):
            for ind, svalue in schema[key].items():
                details[ind] = svalue

        return details;


    def _get_schema_reverse_map(self) :
        newschema = {}
        for schid,sch in self.schema.items() :
            newsch = {}
            for prop,details in sch.items() :
                if (prop[0] == "@") :
                    continue
                
                if (("hack" in details)) :
                    continue
                
                pdetails = self._get_property_details(prop, sch)
                pname = pdetails["name"]
                pdetails["name"] = prop
                newsch[pname] = pdetails
                if (("category" in pdetails)) :
                    catpname = pname + "." + ucfirst(pdetails["category"])
                    newsch[catpname] = pdetails
                
                if (("schema" in pdetails)) :
                    schpname = pname + "." + ucfirst(pdetails["schema"])
                    newsch[schpname] = pdetails

            newschema[schid] = newsch
        
        return newschema

    def _local_name(self, url):
        return str(url).split("#")[-1]

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
                value["@datatype"] = str(row.o.datatype)
            result[pname].append(value)
        return result

    def _get_facts(self, id):
        query = f"SELECT ?p ?o WHERE {{ <{id}> ?p ?o }}"
        qres = self.graph.query(query)
        return self._get_prop_values_from_query_result_p_o(qres)

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


    def _convert_to_lipd(self, id, category, schemaname, pagesdone={}) :
        if id in self.allfacts:
            facts = self.allfacts[id]

            if id in pagesdone:
                return pagesdone[id]
            
            schema =  self.rschema[schemaname] if (schemaname in self.rschema) else None
            if (schemaname and not category) :
                category = schemaname
            
            if "type" in facts:
                cats = facts["type"]
                for cat in cats:
                    if (cat["@type"] == "uri") :
                        category = self._local_name(cat["@id"])
                        break
            
            obj = {
                "@id":id,
                "@category":category,
                "@schema":schemaname
            }

            pagesdone[id] = obj

            for pname, pfacts in facts.items() :
                if pname in REVERSE_BLACKLIST:
                    continue
                prop = pname
                prop = re.sub("/\\s/", "_", prop)
                # Get a sample value page category, and use to make a property key
                propkey = prop
                for value in pfacts: 
                    if value["@type"] == "uri" :
                        if value["@id"] in self.allfacts :
                            pfact = self.allfacts[value["@id"]]
                            if "type" in pfact:
                                valcats = pfact["type"]
                                for valcat in valcats:
                                    if (valcat["@type"] == "uri") :
                                        valcatname = self._local_name(valcat["@id"])
                                        propkey = prop + "." + valcatname
                                        break

                details = self._get_rdf_property_details(prop, propkey, schema)
                name = details["name"]
                ptype =  details["type"] if ("type" in details) else None
                cat =  details["category"] if ("category" in details) else None
                sch =  details["schema"] if ("schema" in details) else None
                if (cat and not sch) :
                    sch = cat
                
                toJson =  details["toJson"] if ("toJson" in details) else None
                multiple =  details["multiple"] if ("multiple" in details) else False

                if len(pfacts) > 0 :
                    if (multiple) :
                        obj[name] = []
                    
                    for pfact in pfacts : 
                        if pfact["@type"] == "uri" :
                            val = self._convert_to_lipd(pfact["@id"], cat, sch, pagesdone)
                        else:
                            val = pfact["@value"]
                        
                        if (toJson) :
                            fn = getattr(self, toJson)
                            val = fn(val)
                                                
                        # If there is already a value present
                        # - Then this need to be marked as "multiple"
                        if (not multiple) and (name in obj) and (not type(obj[name]) is list):
                            multiple = True
                            obj[name] = [obj[name]]
                        
                        if (multiple) :
                            obj[name].append(val)
                        else : 
                            obj[name] = val

            return obj
        else : 
            return re.sub("/_/", " ", id)


    def _post_processing(self, obj, parent=None):
        if not(type(obj) is dict):
            return obj
		
        if not("@schema" in obj):
            return obj

        # FIXME: Hack to avoid recursion
        schemaname = obj["@schema"]
        tschema = self.schema[schemaname] if schemaname in self.schema else None

        if tschema and "@toJson_pre" in tschema:
            for func in tschema["@toJson_pre"]:
                fn = getattr(self, func)
                obj = fn(obj, parent)        

        for key,value in obj.items():
            if type(value) is list:
                for i in range(len(value)):
                    obj[key][i] = self._post_processing(value[i], obj)
            else:
                obj[key] = self._post_processing(value, obj)

        if tschema and "@toJson" in tschema:
            for func in tschema["@toJson"]:
                fn = getattr(self, func)
                obj = fn(obj, parent)

        # FIXME: Only remove hasValues.. LiPD CSVs should be created outside this function beforehand
        if "hasValues" in obj:
            valuestr = obj["hasValues"]
            obj["values"] = json.loads(valuestr)
            del obj["hasValues"]
        
        del obj["@id"]
        del obj["@schema"]
        del obj["@category"]
        if "type" in obj:
            del obj["type"] 

        return obj

    #########################################
    # Converters
    #########################################
    def _location_to_json(self, geo, parent = None) :
        geojson = {
            "geometry":
                {
                    "coordinates" : [0, 0, 0],
                },
            "properties": {}
        }
        if "coordinates" in geo :
            latlong = geo["coordinates"].split(",")
            geojson["geometry"]["coordinates"] = [ float(latlong[1]), float(latlong[0]), float(latlong[2]) if len(latlong)>2 else 0 ]
            geojson["geometry"]["type"] = "Point"
        
        if "long" in geo :
            geojson["geometry"]["coordinates"][0] = float(geo["long"])
        
        if "lat" in geo :
            geojson["geometry"]["coordinates"][1] = float(geo["lat"])
        
        if "alt" in geo and geo["alt"] != "NA":
            geojson["geometry"]["coordinates"][2] = float(geo["alt"])
        
        for prop,value in geo.items() :
            if prop[0] == "@" :
                continue
            
            if prop == "locationType" :
                geojson["type"] = geo["locationType"]
            else : 
                if prop == "coordinates" or prop == "coordinatesFor":
                    # Ignore
                    pass
                else : 
                    if re.search(r"^(geo|wgs84):", prop) :
                        # Ignore
                        pass
                    elif prop in ["long", "lat", "alt"] :
                        pass
                    else : 
                        geojson["properties"][prop] = value
        
        return geojson


    def _get_google_spreadsheet_key(self, url:str, parent = None) :
        return url.replace("https://docs.google.com/spreadsheets/d/", "")

    def _remove_found_in_table(self, var, parent = None) :
        if "foundInTable" in var :
            del var["foundInTable"]
        return var

    def _remove_found_in_dataset(self, var, parent = None) :
        if "foundInDataset" in var :
            del var["foundInDataset"]
        return var
    
    def __get_variable_archive_types(self, item, atypes) :
        if type(item) is dict:
            nitem = {}
            for key,value in item.items() :
                if (key == "archiveType") :
                    atypes[value] = 1
                else : 
                    [nitem[key], atypes] = self.__get_variable_archive_types(value, atypes)
            
        elif type(item) is list:
            nitem = []
            for value in item :
                [nit, atypes] = self.__get_variable_archive_types(value, atypes)
                nitem.append(nit)
                
        else : 
            nitem = item
        return [nitem, atypes]

    def _get_variable_archive_types(self, var, parent = None) :
        [var, atypes] = self.__get_variable_archive_types(var, {})
        for atype,ok in atypes.items() :
            var["archiveType"] = atype
        return var

    def _get_lipd_archive_type(self, archiveType):
        return unCamelCase(archiveType)

    def _extract_from_proxy_system(self, var, parent = None) :
        if (("hasProxySystem" in var)) :
            ps = var["hasProxySystem"]
            #var["proxy"] = ps["name"]
            if (("hasProxySensor" in ps)) :
                psensor = ps["hasProxySensor"]
                if type(psensor) is dict:
                    if (("sensorGenus" in psensor)) :
                        var["sensorGenus"] = psensor["sensorGenus"]
                    
                    if (("sensorSpecies" in psensor)) :
                        var["sensorSpecies"] = psensor["sensorSpecies"]

            del var["hasProxySystem"]
        if (("measuredOn" in var)) :
            archive = var["measuredOn"]
            if type(archive) is dict and "@category" in archive:
                archiveType = archive["@category"]
                var["archiveType"] = self._get_lipd_archive_type(archiveType)
            elif type(archive) is str:
                var["archiveType"] = self._get_lipd_archive_type(archive)
            del var["measuredOn"]
        return var

    def _unwrap_uncertainty(self, var, parent = None) :
        if (("hasUncertainty" in var)) :
            unc = var["hasUncertainty"]
            if (("hasValue" in unc)) :
                var["uncertainty"] = float(unc["hasValue"])
                del unc["hasValue"]
            
            for key,value in unc.items() :
                if (key[0] != "@") :
                    var[key] = value
                
            del var["hasUncertainty"]
        return var

    def _unwrap_integration_time(self, interp, parent = None) :
        if (("integrationTime" in interp)) :
            intime = interp["integrationTime"]
            if (("hasValue" in intime)) :
                interp["integrationTime"] = float(intime["hasValue"])
                del intime["hasValue"]
            
            for key,value in intime.items() :
                if (key[0] != "@") :
                    interp["integrationTime" + ucfirst(key)] = value

            del interp["hasIntegrationTime"]
        return interp

    def _collect_variables_by_id(self, item, arr) :
        if not (type(item) is dict):
            return arr

        # Data is a Hash
        if ("@category" in item) and ("@id" in item) and re.match("/Variable\$/", item["@category"]) :
            arr[item["@id"]] = item
        else : 
            for key,value in item.items() :
                if (key[0] != "@") :
                    arr = self._collect_variables_by_id(item[key], arr)
        return arr

    def _set_variable_type(self, var, parent = None) :
        if (var["@category"] == "MeasuredVariable") :
            var["variableType"] = "measured"
        
        if (var["@category"] == "InferredVariable") :
            var["variableType"] = "inferred"
        return var

    def _remove_depth_property(self, val, parent = None) :
        if "takenAtDepth" in val :
            del val["takenAtDepth"]
        return val

    def _create_publication_identifier(self, pub, parent = None) :
        identifiers = []
        if (("hasDOI" in pub)) :
            identifier = {}
            identifier["type"] = "doi"
            identifier["id"] = pub["hasDOI"]
            if (("link" in pub)) :
                for link in pub["link"].values() : 
                    if (re.match("/dx.doi.org/", link)) :
                        identifier["url"] = link
                del pub["link"]
            del pub["hasDOI"]
            identifiers.append(identifier)

        pub["identifier"] = identifiers
        return pub

    def _change_seasonality_type(self, interp, parent = None) :
        if (("seasonality" in interp)) :
            if type(interp["seasonality"]) is list:
                newseasonality = []
                for svalue in interp["seasonality"]:
                    newseasonality.append(float(svalue))
                interp["seasonality"] = newseasonality
        return interp

    def _values_to_array(self, resolution, parent = None) :
        if (("values" in resolution)) :
            return resolution["values"].split(",")

    def _unarray_column_number(self, var, parent = None) :
        if not var:
            return var
        if ("number" in var) and (type(var["number"]) is list) and (len(var["number"]) == 1) :
            var["number"] = var["number"][0]
        if ("number" in var) and (type(var["number"]) is str) :
            var["number"] = json.loads(var["number"])
        return var

    def _extract_variable_values(self, var, parent = None) :
        if "hasValues" in var:
            valuestr = var["hasValues"]
            values = json.loads(valuestr)
            if type(values) is dict and "base64_zlib" in values:
                values = unzip_string(values["base64_zlib"])
                var["hasValues"] = values
        return var