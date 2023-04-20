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

    SELECT ?datasetName ?ensembleTable ?ensembleVariableName ?ensembleVariableValues ?ensembleVariableUnits ?ensembleDepthName ?ensembleDepthValues ?ensembleDepthUnits ?notes 
    WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?datasetName .
            FILTER regex(?datasetName, "[dsname].*").
    
        ?ds le:includesChronData ?chron .
        ?chron le:chronModeledBy ?model .
        ?model le:foundInEnsembleTable ?ensembleTable .
            OPTIONAL{?ensembleTable le:notes ?notes}
        
        ?ensembleTable le:includesVariable ?ensvar .
        ?ensvar le:name ?ensembleVariableName .
            FILTER (regex(lcase(?ensembleVariableName), "year.*") || regex(?ensembleVariableName, "age.*")) .
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

    SELECT ?datasetName ?ensembleTable ?ensembleVariableName ?ensembleVariableValues ?ensembleVariableUnits ?ensembleDepthName ?ensembleDepthValues ?ensembleDepthUnits ?notes ?methodobj ?methods
    WHERE {
        ?ds a le:Dataset .
        ?ds le:name ?datasetName .
            FILTER regex(?datasetName, "[dsname].*").
    
        ?ds le:includesChronData ?chron .
        ?chron le:chronModeledBy ?model .
        ?model le:foundInEnsembleTable ?ensembleTable .
            OPTIONAL{?ensembleTable le:notes ?notes}
        
        ?ensembleTable le:includesVariable ?ensvar .
        ?ensvar le:name ?ensembleVariableName .
            FILTER regex(lcase(?ensembleVariableName), "[ensembleVarName].*").
        ?ensvar le:hasValues ?ensembleVariableValues
            OPTIONAL{?ensvar le:hasUnits ?ensembleVariableUnits .}
        
        ?ensembleTable le:includesVariable ?ensdepthvar .
        ?ensdepthvar le:name ?ensembleDepthName .
            FILTER regex(lcase(?ensembleDepthName), "[ensembleDepthVarName].*").
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