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

QUERY_ENSEMBLE_TABLE_SHORT = """
    PREFIX le: <http://linked.earth/ontology#>
    PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>

    SELECT ?datasetName ?ensembleTable ?ensembleVariableName ?ensembleVariableValues ?ensembleVariableUnits ?ensembleDepthName ?ensembleDepthValues ?ensembleDepthUnits ?notes 
    WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?datasetName .
            FILTER regex(?datasetName, "[dsname].*", "i").
    
        ?ds le:includesChronData ?chron .
        ?chron le:chronModeledBy ?model .
        ?model le:foundInEnsembleTable ?ensembleTable .
            OPTIONAL{?ensembleTable le:notes ?notes}
        
        ?ensembleTable le:includesVariable ?ensvar .
        ?ensvar le:name ?ensembleVariableName .
            FILTER (regex(lcase(?ensembleVariableName), "year.*", "i") || regex(?ensembleVariableName, "age.*", "i")) .
        ?ensvar le:hasValues ?ensembleVariableValues
            OPTIONAL{?ensvar le:hasUnits ?ensembleVariableUnits .}
        
        ?ensembleTable le:includesVariable ?ensdepthvar .
        ?ensdepthvar le:name ?ensembleDepthName .
            FILTER regex(lcase(?ensembleDepthName), "[ensembleDepthVarName].*").
        ?ensdepthvar le:hasValues ?ensembleDepthValues .
            OPTIONAL{?ensdepthvar le:hasUnits ?ensembleDepthUnits .}
    }
"""

QUERY_ENSEMBLE_TABLE = """
    PREFIX le: <http://linked.earth/ontology#>
    PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>

    SELECT ?datasetName ?ensembleTable ?ensembleVariableName ?ensembleVariableValues ?ensembleVariableUnits ?ensembleDepthName ?ensembleDepthValues ?ensembleDepthUnits ?notes
    WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?datasetName .
            FILTER regex(?datasetName, "[dsname].*", "i").
    
        ?ds le:includesChronData ?chron .
        ?chron le:chronModeledBy ?model .
        ?model le:foundInEnsembleTable ?ensembleTable .
            OPTIONAL{?ensembleTable le:notes ?notes}
        
        ?ensembleTable le:includesVariable ?ensvar .
        ?ensvar le:name ?ensembleVariableName .
            FILTER regex(lcase(?ensembleVariableName), "[ensembleVarName].*", "i").
        ?ensvar le:hasValues ?ensembleVariableValues
            OPTIONAL{?ensvar le:hasUnits ?ensembleVariableUnits .}
        
        ?ensembleTable le:includesVariable ?ensdepthvar .
        ?ensdepthvar le:name ?ensembleDepthName .
            FILTER regex(lcase(?ensembleDepthName), "[ensembleDepthVarName].*", "i").
        ?ensdepthvar le:hasValues ?ensembleDepthValues .
            OPTIONAL{?ensdepthvar le:hasUnits ?ensembleDepthUnits .}
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

QUERY_VARIABLE = """
    PREFIX le: <http://linked.earth/ontology#>

    SELECT ?uri ?varid ?varname 
    WHERE {
        ?uri le:name ?varname .
        ?uri le:hasVariableID ?varid
    }
"""

QUERY_VARIABLE_GRAPH = """
    PREFIX le: <http://linked.earth/ontology#>

    CONSTRUCT {
        <[varid]> ?p1 ?o1 .
        <[varid]> ?pv1 ?v1 .
        ?s2 ?pv2 ?v2 .
    }
    WHERE {
        # level 1
        <[varid]> ?p1 ?o1 # get objects
            FILTER (
                (?p1 NOT IN (le:foundInTable, le:takenAtDepth)) &&
                isIRI(?o1)
            ) .
        <[varid]> ?pv1 ?v1  # get primitives
            FILTER (isLiteral(?v1)) .
        
        BIND (?o1 as ?s2) . # rename binding for readability

        # level 2
        ?s2 ?pv2 ?v2 
            FILTER (isLiteral(?v2)) .
    }
"""

QUERY_ALL_VARIABLES_GRAPH = """
    PREFIX le: <http://linked.earth/ontology#>

    INSERT {
        GRAPH ?var
        {
            ?var ?pv1 ?v1 .
            ?var ?p1 ?o1 .        
            ?o1 ?pv2 ?v2 .
            ?o1 ?p2 ?o2 .
            ?o2 ?pv3 ?v3 .
            ?var le:foundInTable ?table .
            ?var le:foundInDataset ?ds .
        }
    }
    WHERE {
        ?table le:includesVariable ?var .
        {
            {
                # level 1
                ?var le:foundInDataset ?ds .
                ?var ?pv1 ?v1  # get primitives
                    FILTER (isLiteral(?v1)) .
            }
            UNION
            {
                # level 2
                {
                    ?var ?p1 ?o1
                        FILTER (?p1 NOT IN (le:foundInTable, le:foundInDataset, le:takenAtDepth)) .
                    ?o1 ?pv2 ?v2 
                        FILTER (isLiteral(?v2)) .
                } .
            }
            #UNION
            #{
            #    # level 3
            #    {
            #        ?var ?p1 ?o1
            #            FILTER (?p1 NOT IN (le:foundInTable, le:foundInDataset, le:takenAtDepth)) .
            #        ?o1 ?p2 ?o2
            #            FILTER (?p1 NOT IN (le:foundInTable, le:foundInDataset, le:takenAtDepth)) .
            #        ?o2 ?pv3 ?v3
            #            FILTER (isLiteral(?v2)) .
            #    } .
            #}
        }
    }
"""


QUERY_FILTER_GEO = """
    PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>

    SELECT ?dsname WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?dsname .
        ?ds le:collectedFrom ?loc .
        ?loc wgs84:lat ?lat .
        ?loc wgs84:long ?lon .
        FILTER ( ?lat >= [latMin] && ?lat < [latMax] && ?lon >= [lonMin] && ?lon < [lonMax] ) .
    }
"""

QUERY_FILTER_ARCHIVE_TYPE = """
    SELECT ?dsname WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?dsname .
        ?ds le:proxyArchiveType ?archiveType .
        FILTER regex(?archiveType, "[archiveType].*", "i")
    }
"""

QUERY_FILTER_VARIABLE_NAME = """
    SELECT ?uri ?dsuri ?tableuri ?id ?name WHERE {
        ?uri le:hasVariableID ?id .
        ?uri le:name ?name .
        FILTER regex(?name, "[name].*", "i") .
        ?uri le:foundInDataset ?dsuri .
        ?uri le:foundInTable ?tableuri .
    }
"""