import json
import re
import uuid
import os
import os.path
import zipfile
import tempfile
import pandas as pd
from globals import SCHEMA, BLACKLIST, NS, ONTONS
from utils import ucfirst, lcfirst, camelCase, unCamelCase, fromCamelCase, escape, uniqid, sanitizeId

class LipdToRDF(object):
    
    def __init__(self):
        self.triples = []
        self.lipd_csvs = {}

    def convert(self, lipdpath, rdfpath):
        self.triples = []
        with tempfile.TemporaryDirectory(prefix="lipd_to_rdf_") as tmpdir:
            self.unzip_lipd_file(lipdpath, tmpdir)
            jsons = self.find_files_with_extension(tmpdir, 'jsonld')
            for jsonpath, _ in jsons:
                jsondir = os.path.dirname(jsonpath)
                csvs = self.find_files_with_extension(jsondir, 'csv')
                self.lipd_csvs = {}
                for csvpath, _ in csvs:
                    csvname = os.path.basename(csvpath)        
                    self.lipd_csvs[csvname] = pd.read_csv(csvpath, header=None)
                self.convertLipdJsonToRDF(jsonpath, rdfpath)

    def unzip_lipd_file(self, lipdfile, unzipdir):
        with zipfile.ZipFile(lipdfile, 'r') as zip_ref:
            zip_ref.extractall(unzipdir)

    def addExtraDatasetProperties(self, obj, objhash) :
        _REQUEST = {} # This is not really used here is it ?
        for key,value in _REQUEST.items() :
            m = re.search(r"^extra_(.+)", key)
            if m is not None:
                prop = m.groups()[0]
                if (not (prop in obj)) :
                    obj[prop] = value
        return [obj, objhash, []]

    def parsePersonsString(self, authstring, parent = None) :
        authors = []
        if (type(authstring) is list) :
            return self.parsePersons(authstring, None)
        
        if (re.search(r"\s*\s*", authstring)) :
            auths = re.split(r"\s*\s*", authstring)
            for auth in auths:            
                authors.append(self.parsePerson(auth))
            
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


    def parsePerson(self, auth, parent = None) :
        authname = auth
        if (type(auth) is dict) :
            authname = auth["name"]
        m = re.search(r"(.+)\s*,\s*(.+)", authname)
        if m is not None:
            return {"name" : str(str(m.groups()[1]) + " ") + str(m.groups()[0])}
        else : 
            return {"name" : authname}

        
    def parsePersons(self, auths, parent = None) :
        authors = []
        if (not type(auths) is list) :
            return None
        
        for auth in auths: 
            authors.append(self.parsePerson(auth, parent))
        return authors

    def parseLocation(self, geo, parent = None) :
        ngeo = {}
        ngeo["locationType"] = geo["type"] if "type" in geo else None
        ngeo["coordinatesFor"] = parent["@id"]
        coords = geo["geometry"]["coordinates"]
        if (coords and len(coords) > 0) :
            ngeo["coordinates"] = str(str(coords[1]) + ",") + str(coords[0])
            ngeo["Wgs84:Lat"] = coords[1]
            ngeo["Wgs84:Long"] = coords[0]
            # FIXME: For now assuming points
            wkt = str(str("POINT(" + str(coords[1])) + " ") + str(coords[0])
            if (len(coords) > 2) :
                ngeo["Wgs84:Alt"] = coords[2]
                wkt += " " + str(coords[2])
            
            wkt += ")"
            ngeo["Geo:HasGeometry"] = {
                "@id" : str(parent["@id"]) + ".Geometry",
                "@category" : "Geo:Geometry",
                "Geo:AsWKT" : wkt
            }
        
        if "properties" in geo :
            for key,value in geo["properties"].items() :
                ngeo[key] = value
        return ngeo


    def locationToJson(self, geo, parent = None) :
        geojson = {
            "geometry":
                {
                    "coordinates" : [],
                    "properties" : []
                }
        }
        if "coordinates" in geo :
            latlong = geo["coordinates"].split(",")
            geojson["geometry"]["coordinates"][0] = float(latlong[1])
            geojson["geometry"]["coordinates"][1] = float(latlong[0])
            geojson["geometry"]["type"] = "Point"
        
        if "wgs84:Long" in geo :
            geojson["geometry"]["coordinates"][0] = float(geo["wgs84:Long"])
        
        if "wgs84:Lat" in geo :
            geojson["geometry"]["coordinates"][1] = float(geo["wgs84:Lat"])
        
        if "wgs84:Alt" in geo :
            geojson["geometry"]["coordinates"][2] = float(geo["wgs84:Alt"])
        
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
                    else : 
                        geojson["properties"][prop] = value
        
        return geojson

    def getUncertainty(self, val, parent = None) :
        uncertainty = {}
        uncertainty["hasValue"] = val
        uncertainty["analytical"] = val
        uncertainty["reproducibility"] = val
        return uncertainty

    def getGoogleSpreadsheetURL(self, key, parent = None) :
        return "https://docs.google.com/spreadsheets/d/" + str(key) + ""

    def getGoogleSpreadsheetKey(self, url:str, parent = None) :
        return url.replace("https://docs.google.com/spreadsheets/d/", "")
    
    def getParentProperty(self, obj, prop) :
        parent = obj["@parent"]
        while (parent) :
            if ((prop in parent)) :
                return parent[prop]
            
            parent = parent["@parent"]
        return None

    def getParentWithPropertyValue(self, obj, prop, val) :
        parent = obj["@parent"]
        while (parent) :
            if ((prop in parent) and parent[prop] == val) :
                return parent
            
            parent = parent["@parent"]
        return None
    
    def setIdentifierProperties(self, pub, objhash) :
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
    
    def valuesToString(self, obj, objhash) :
        if "values" in obj :
            if (type(obj["values"]) is list) :
                obj["values"] = ", ".join(obj["values"])
        return [obj, objhash, []]


    def setVariableCategory(self, obj, objhash) :
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
    
    def getLiPDArchiveType(self, archiveType) :
        return unCamelCase(archiveType)

    def getArchiveType(self, id, latitude) :
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
    
    def guessSensorType(self, archive, observation, sensor) :
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
    
    def getObservation(self, observation) :
        if observation is None:
            return None
        if (observation.lower() == "alkenone") :
            return "Uk37"
        return camelCase(observation)

    def getVariableId(self, obj, parentid) :
        iobj = dict((k.lower(), v) for k, v in obj.items())
        id =  parentid + "." + iobj["tsid"]
        id += "." + str(iobj["variablename"])
        return id
    
    def setInterVariableLinks(self, obj, objhash) :
        depthcol = None
        vobjhash = {}
        for col in obj["columns"] : 
            vobjhash[col["variableName"].lower()] = self.getVariableId(col, obj["@id"])
        
        depthcol =  vobjhash["depth"] if ("depth" in vobjhash) else None
        for col in obj["columns"] : 
            thiscol = self.getVariableId(col, obj["@id"])
            if (("inferredFrom" in col)) :
                infcol = col["inferredFrom"].lower()
                if ((infcol in vobjhash)) :
                    col["inferredFrom"] = vobjhash[infcol]
                
            if (depthcol and thiscol != depthcol) :
                col["takenAtDepth"] = depthcol
        return [obj, objhash, []]
    
    def removeDepthProperty(self, val, parent = None) :
        if (("takenAtDepth" in val)) :
            del val["takenAtDepth"]
        return val
    
    def createProxySystem(self, obj, hash) :
        varid = obj["@id"]
        # Deal with proxies
        proxyobs = None
        sampleid = None
        if ("proxy" in obj) :
            proxyobs = obj["proxy"]
            del obj["proxy"]
        elif ("OnProxyObservationProperty" in obj) :
            proxyobs = obj["OnProxyObservationProperty"]
            del obj["OnProxyObservationProperty"]
        elif ("ProxyObservationType" in obj) :
            proxyobs = obj["ProxyObservationType"]
        
        vartype = obj["@category"]
        if (vartype and vartype == "MeasuredVariable") :
            # Get the archive type
            dsname = self.getParentProperty(obj, "dataSetName")
            geo = self.getParentProperty(obj, "geo")
            latitude = 0
            if (("geometry" in geo) and len(geo["geometry"]["coordinates"]) > 1) :
                latitude = geo["geometry"]["coordinates"][1]
            
            archivetype = self.getParentProperty(obj, "archiveType")
            if (not archivetype) :
                archivetype = self.getParentProperty(obj, "archive")
            
            archivetype = self.getArchiveType(archivetype, latitude)
            # Create sample (archive)
            if (not ("physicalSample" in obj)) :
                cname = self.getParentProperty(obj, "collectionName")
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
            
            observationid = self.getObservation(proxyobs)
            #obj["proxy"])
            # Create sensor
            sensorid = (str(observationid) if observationid is not None else "") + "DefaultSensor"
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
                sensor["@category"] = self.guessSensorType(archivetype, observationid, sensor)
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
    
    def wrapIntegrationTime(self, obj, objhash) :
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

    def wrapUncertainty(self, obj, objhash) :
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
    
    def addFoundInTable(self, obj, objhash) :
        obj["foundInTable"] = obj["@parent"]["@id"]
        return [obj, objhash, []]
    
    # Unroll the list to a rdf first/rest structure
    def unrollValuesListToRDF(self, lst: list, dtype):
        bnodeid = "_:values" + uniqid()
        rdfns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xsdns = "http://www.w3.org/2001/XMLSchema#"
        self.triples.append([
            bnodeid,
            f"<{rdfns}type>",
            f"<{rdfns}Seq>"
        ])
        for idx, item in enumerate(lst):
            self.triples.append([
                bnodeid,
                f"<{rdfns}_{idx+1}>",
                f"\"{item}\"^^<{xsdns}{dtype}>"
            ])
        return bnodeid
    
    def addVariableValues(self, obj, objhash) :
        csvname = obj["@parent"]["@id"] + ".csv"
        colnum = int(obj["number"]) - 1
        if csvname in self.lipd_csvs:
            df = self.lipd_csvs[csvname]
            col = df[colnum]
            values = col.tolist()
            dtype = "float" if col.dtypes == "float64" else "string"
            # TODO: Dumping to json string for now. 
            # rdf:Seq doesn't seem to be importing well in GraphDB
            obj["hasValues"] = json.dumps(values)
            #bnodeid = unrollValuesListToRDF(values, dtype)
            #obj["hasValues"] = bnodeid
            return [obj, objhash, []]
        return [obj, objhash, []]
    
    ### Object json reverse conversion
    def removeFoundInTable(self, var, parent = None) :
        if (("foundInTable" in var)) :
            del var["foundInTable"]
        return var
    
    ### Testing Lipd Json to Ontology
    def expandSchema(self) :
        xschema = {}
        for key,props in SCHEMA.items() :
            # Add core schema too
            xschema[key] = props
            for lipdkey,pdetails in props.items() :
                if not type(pdetails) is dict:
                    continue
                
                if (("alternates" in pdetails)) :
                    for altkey in pdetails["alternates"]: 
                        xschema[key][altkey] = pdetails
        SCHEMA = xschema
    
    def modifyStructureIfNeeded(self, obj, objhash, schema) :
        if (("@fromJson" in schema)) :
            for func in schema["@fromJson"]: 
                fn = getattr(self, func)
                (obj, objhash, newids) = fn(obj, objhash)
                for newid in newids : 
                    if ((newid in objhash)) :
                        newobj = objhash[newid]
                        if (type(newobj) is dict) and ("@category" in newobj) :
                            newschid = newobj["@category"]
                            newschema =  SCHEMA[newschid] if (newschid in SCHEMA) else {}
                            (objhash[newid], objhash) = self.modifyStructureIfNeeded(newobj, objhash, newschema)
        
        return [obj, objhash]
    
    def getCompoundKeyId(self, compound_key, obj) :
        tobj = obj
        for key in compound_key : 
            if ((type(tobj) is dict) and (key in tobj)) :
                tobj = tobj[key]
            else : 
                return None
            
        if not type(tobj) is dict:
            return tobj
        
        return None
    
    def getBindingKeyId(self, key, obj) :
        key_options = key.split("|")
        for optkey in key_options : 
            compound_key = optkey.split(".")
            keyid = self.getCompoundKeyId(compound_key, obj)
            if (keyid) :
                return keyid
        return uniqid()
    
    def getFunctionKeyId(self, fn, arg, curobjid) :
        if (fn == "trunc") :
            return curobjid[0:0 + len(curobjid) - int(arg)]
        elif (fn == "uniqid") :
            return str(curobjid) + uniqid(arg)
        return curobjid
    
    def createIdFromPattern(self, pattern, obj) :
        objid = ""
        for key in pattern : 
            m = re.search(r"{(.+)}", key)
            if m and len(m.groups()) > 0 :
                objid += str(self.getBindingKeyId(m.groups()[0], obj))
            else : 
                m = re.search(r"_(.+)\((.*)\)", key)
                if m and len(m.groups()) > 1:
                    fn = m.groups()[0]
                    arg = m.groups()[1]
                    objid = str(self.getFunctionKeyId(fn, arg, objid))
                else : 
                    objid += str(key)
        return objid
    
    def fixTitle(self, titleid) :
        return titleid.replace(r"@\\x{FFFD}@u", '_')
    
    def getObjectId(self, obj, category, schema) :
        if type(obj) is dict:
            objid =  "Unknown." + uniqid(category)
        else:
            objid = ucfirst(obj).replace(" ", "_")
        if (("@id" in schema)) :
            objid = self.createIdFromPattern(schema["@id"], obj)
        
        return self.fixTitle(objid)
    
    def mapLipdJson(self, obj, parent, index, category, schemaname, hash) :
        schema =  SCHEMA[schemaname] if (schemaname in SCHEMA) else {}
        SCHEMA[schemaname] = schema
        
        if not type(obj) is dict:
            return obj
        
        obj["@parent"] = parent
        obj["@index"] = index
        obj["@schema"] = schemaname
        
        objid = self.getObjectId(obj, category, schema)
        if (("@id" in obj)) :
            objid = obj["@id"]
        if ((objid in hash)) :
            return objid
        obj["@id"] = objid
        
        (obj, hash) = self.modifyStructureIfNeeded(obj, hash, schema)
        
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
                                    item[propkey].append(self.mapLipdJson(subvalue, obj, index, cat, sch, hash))
                                    index+=1
                        else : 
                            if (type(value) is dict):
                                item[propkey] = self.mapLipdJson(value, obj, None, cat, sch, hash)
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
                        item[propkey].append(self.mapLipdJson(subvalue, obj, index, cat, sch, hash))
                        index+=1
                    
                else : 
                    if (type(value) is dict):
                        if propkey not in item:
                            item[propkey] = []                      
                        item[propkey].append(self.mapLipdJson(value, obj, None, cat, sch, hash))
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
    
    def guessDataValueType(self, val) :
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
    
    def guessValueType(self, value) :
        if value:
            if type(value) is list :
                for subvalue in value :
                    return self.guessValueType(subvalue)
            elif type(value) is dict : 
                return "Individual"
            
            else : 
                valtype = self.guessDataValueType(value)
                return valtype

        return "string"
    
    def getPropertyDetails(self, key, schema, value) :
        pname = fromCamelCase(key)
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
        
        pname = ucfirst(details["name"])
        
        # Get more details from the property definition (if it exists)
        """
        newname = resolveProperty(pname)
        if (newname) :
            details["type"] = getOntPropertyRange(newname)
            details["name"] = newname
        """ 
        
        if (not ("type" in details)) :
            details["type"] = self.guessValueType(value)
            if (not ("type" in details)) :
                details["type"] = "string"

        details["@@processed"] = True
        schema[key] = details
        return details
    
    # Create individual
    def createIndividual(self, objid) :
        return NS + sanitizeId(objid)
    
    # Create class
    def createClass(self, category) :
        return ONTONS + sanitizeId(category)
    
    # Create property
    def createProperty(self, prop, dtype, cat, icon, multiple) :
        return [ ONTONS + lcfirst(sanitizeId(prop)), dtype ]
    
    # Set individual classes
    def setIndividualClasses(self, objid, category, extracats) :
        rdftype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        if objid and category:
            self.triples.append([
                "<"+objid+">",
                "<"+rdftype+">",
                "<"+category+">"
            ])
        for ecat in extracats:
            if objid and ecat:
                self.triples.append([
                    "<"+objid+">",
                    "<"+rdftype+">",
                    "<"+self.createClass(ecat)+">"
                ])
    
    # Set property value
    def setProperty( self, objid, prop, value ):
        if (type(value) is list) :
            for subvalue in value : 
                self.setProperty(objid, prop, subvalue)
            return

        (propid, dtype) = prop
        if objid and value:
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
                value = self.createIndividual(value)
                value = "<" + value + ">"
            elif dtype == "List":
                value = value
            else:
                value = '"' + str(value) + '"' + "^^<http://www.w3.org/2001/XMLSchema#" + dtype + ">"
            
            self.triples.append([
                "<"+objid+">",
                "<"+propid+">",
                value
            ])
    # Set subobject propvals
    def setSubobjects(self, objid, subobjid, subpropvals, schema) :
        if (not subpropvals) :
            return
        
        subobjectid = str(objid) + "_" + str(subobjid)
        for pval in subpropvals : 
            for key,value in pval.items() :
                if (key[0] == "@") :
                    continue
                
                details = self.getPropertyDetails(key, schema, value)
                prop = details["name"]
                type = details["type"]
                icon =  details["icon"] if ("icon" in details) else None
                cat =  details["category"] if ("category" in details) else None
                sch =  details["schema"] if ("schema" in details) else None
                fromJson =  details["fromJson"] if ("fromJson" in details) else None
                multiple =  details["multiple"] if ("multiple" in details) else False
                # Create & set Property
                propDI = self.createProperty(prop, type, cat, icon, multiple)
                self.setProperty(subobjectid, propDI, value)
                #print "|$key=$value"

        #print "\n"
        return
    
    def createIndividualFull(self, obj) :
        category = obj["@category"]
        extracats =  obj["@extracats"] if ("@extracats" in obj) else {}
        schemaname =  obj["@schema"] if ("@schema" in obj) else category
        schema =  SCHEMA[schemaname] if (schemaname in SCHEMA) else {}
        objid = obj["@id"]
        if (not objid) :
            return
        
        subobjects = {}
        # Create category
        if (category) :
            category = self.createClass(category)
        
        objid = self.createIndividual(objid)
        
        # Set Individual classes
        self.setIndividualClasses(objid, category, extracats)
        
        for key,value in obj.items() :
            if (key[0] == "@") :
                continue
            
            details = self.getPropertyDetails(key, schema, value)
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
            propDI = self.createProperty(prop, dtype, cat, icon, multiple)
            
            # Set property value
            if (dtype == "Individual" or type(value) is dict) :
                self.setProperty(objid, propDI, value)
            else : 
                if (dtype == "File") :
                    # Enable this ?
                    """
                    fileid = uploadFile(value)
                    if (fileid) :
                        protectIndividual(fileid)
                        data = setProperty(data, propDI, fileid)
                    """

                else : 
                    self.setProperty(objid, propDI, value)

    def find_files_with_extension(self, directory, extension):
        myregexobj = re.compile('\.'+extension+'$')
        try: 
            for entry in os.scandir(directory):
                if entry.is_file() and myregexobj.search(entry.path): 
                    yield entry.path, entry.name
                elif entry.is_dir():   # if its a directory, then repeat process as a nested function
                    yield from self.find_files_with_extension(entry.path, extension)
        except OSError as ose:
            print('Cannot access ' + directory +'. Probably a permissions error ', ose)
        except FileNotFoundError as fnf:
            print(directory +' not found ', fnf)

    def convertLipdJsonToRDF(self, jsonpath, rdfpath, url=None):
        self.triples.clear()    
        objhash = {}
        
        with open(jsonpath) as f:
            obj = json.load(f)
            obj["hasUrl"] = url
        
            self.mapLipdJson(obj, None, None, "Dataset", "Dataset", objhash)

            for key, item in objhash.items():
                self.createIndividualFull(item)

            with open(rdfpath, "w") as f:
                for triple in self.triples:
                    f.write(" ".join(triple) + " .\n")
                f.close()