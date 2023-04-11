from pylipd.globals.urls import ONTONS, NAMESPACES

QUERY_DSNAME = """
    SELECT ?dsname WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?dsname
    }
"""

QUERY_DSID = """
    SELECT ?dsid WHERE {
        ?ds a le:Dataset .
        OPTIONAL{?ds le:datasetId ?dsid}
    }
"""

QUERY_ENSEMBLE_TABLE = """
    PREFIX le: <http://linked.earth/ontology#>
    PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>

    SELECT ?dsname ?lat ?lon ?archive ?table ?varname ?varunits ?val ?timevarname ?timeunits ?timeval 
    ?depthvarname ?depthunits ?depthval 
    ?enstable ?ensvarname ?ensval ?ensunits ?ensdepthvarname ?ensdepthval ?ensdepthunits 
    WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?dsname .
        
        ?ds le:collectedFrom ?loc . 
        ?loc wgs:lat ?lat .
        ?loc wgs:long ?lon .
        
        ?ds le:proxyArchiveType ?archive .
            FILTER regex(?archive, "[archiveType].*") .
            
        ?ds le:includesPaleoData ?data .
        ?data le:foundInMeasurementTable ?table .
        
        ?table le:includesVariable ?var .
        ?var le:name ?varname .
            FILTER regex(?varname, "[varName].*") .
        ?var le:hasValues ?val .
            OPTIONAL{?var le:hasUnits ?varunits } .

        ?table le:includesVariable ?timevar .
        ?timevar le:name ?timevarname .
            FILTER regex(?timevarname, "[timeVarName].*").
        ?timevar le:hasValues ?timeval .
            OPTIONAL{?timevar le:hasUnits ?timeunits }
        
        OPTIONAL{?table le:includesVariable ?depthvar .
        ?depthvar le:name ?depthvarname .
            FILTER regex(?depthvarname, "[depthVarName].*").
        ?depthvar le:hasValues ?depthval .
            OPTIONAL{?depthvar le:hasUnits ?depthunits .}}
        
        ?ds le:includesChronData ?chron .
        ?chron le:chronModeledBy ?model .
        ?model le:foundInEnsembleTable ?enstable .
        
        ?enstable le:includesVariable ?ensvar .
        ?ensvar le:name ?ensvarname .
            FILTER regex(?ensvarname, "[ensembleVarName].*").
        
        ?enstable le:includesVariable ?ensdepthvar .
        ?ensdepthvar le:name ?ensdepthvarname .
            FILTER regex(?ensdepthvarname, "[ensembleDepthVarName].*").
        ?ensdepthvar le:hasValues ?ensdepthval .
            OPTIONAL{?ensdepthvar le:hasUnits ?ensdepthunits .}
    }
"""


QUERY_BIBLIO = """
    SELECT ?dsname ?title (GROUP_CONCAT(?authorName;separator=" and ") as ?authors) 
    ?doi ?pubyear ?year ?journal ?volume ?issue ?pages ?type ?publisher ?report ?citeKey ?edition ?institution ?url ?url2
    WHERE { 
        ?ds a le:Dataset .
        ?ds le:name ?dsname .
        ?ds le:publishedIn ?pub .
        OPTIONAL{?pub le:hasDOI ?doi .}
        OPTIONAL{
            ?pub le:author ?author .
            ?author le:name ?authorName .
        }
        OPTIONAL{?pub le:publicationYear ?year .}
        OPTIONAL{?pub le:pubYear ?pubyear .}
        OPTIONAL{?pub le:title ?title .}
        OPTIONAL{?pub le:journal ?journal .}
        OPTIONAL{?pub le:volume ?volume .}
        OPTIONAL{?pub le:issue ?issue .}
        OPTIONAL{?pub le:pages ?pages .}
        OPTIONAL{?pub le:type ?type .}
        OPTIONAL{?pub le:publisher ?publisher .}
        OPTIONAL{?pub le:report ?report .}
        OPTIONAL{?pub le:citeKey ?citeKey .}
        OPTIONAL{?pub le:edition ?edition .}
        OPTIONAL{?pub le:institution ?institution .}
        OPTIONAL{?pub le:hasLink ?url .}
        OPTIONAL{?pub le:url ?url2 .}
    }
    GROUP BY ?pub ?dsname ?title ?doi ?year ?pubyear ?journal ?volume ?issue ?pages ?type ?publisher ?report ?citeKey ?edition ?institution ?url ?url2
"""