from pylipd.globals.urls import ONTONS, NAMESPACES

QUERY_DSNAME = """
    SELECT ?dsname WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?dsname
    }
"""

QUERY_DSID = """
    SELECT ?dsid WHERE {
        ?ds a le:Dataset .
        OPTIONAL{?ds le:hasDatasetId ?dsid}
    }
"""

QUERY_UNIQUE_ARCHIVE_TYPE = """
    SELECT distinct ?archiveType WHERE {
        ?ds a le:Dataset .
        ?ds le:hasArchiveType ?archiveTypeObj .
        ?archiveTypeObj rdfs:label ?archiveType .
    }
"""

QUERY_ENSEMBLE_TABLE_SHORT = """
    PREFIX le: <http://linked.earth/ontology#>

    SELECT ?datasetName ?ensembleTable ?ensembleVariableName ?ensembleVariableValues ?ensembleVariableUnits ?ensembleDepthName ?ensembleDepthValues ?ensembleDepthUnits ?notes 
    WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?datasetName .
            FILTER regex(?datasetName, "[dsname].*", "i").
    
        ?ds le:hasChronData ?chron .
        ?chron le:modeledBy ?model .
        ?model le:hasEnsembleTable ?ensembleTable .
            OPTIONAL{?ensembleTable le:hasNotes ?notes}
        
        ?ensembleTable le:hasVariable ?ensvar .
        ?ensvar le:hasName ?ensembleVariableName .
            FILTER (regex(lcase(?ensembleVariableName), "year.*", "i") || regex(?ensembleVariableName, "age.*", "i")) .
        ?ensvar le:hasValues ?ensembleVariableValues
            OPTIONAL{
                ?ensvar le:hasUnits ?ensembleVariableUnitsObj .
                ?ensembleVariableUnitsObj rdfs:label ?ensembleVariableUnits .
            }
        
        ?ensembleTable le:hasVariable ?ensdepthvar .
        ?ensdepthvar le:hasName ?ensembleDepthName .
            FILTER regex(lcase(?ensembleDepthName), "[ensembleDepthVarName].*").
        ?ensdepthvar le:hasValues ?ensembleDepthValues .
            OPTIONAL{
                ?ensdepthvar le:hasUnits ?ensembleDepthUnitsObj .
                ?ensembleDepthUnitsObj rdfs:label ?ensembleDepthUnits .
            }
    }
"""

QUERY_ENSEMBLE_TABLE = """
    PREFIX le: <http://linked.earth/ontology#>

    SELECT ?datasetName ?ensembleTable ?ensembleVariableName ?ensembleVariableValues ?ensembleVariableUnits ?ensembleDepthName ?ensembleDepthValues ?ensembleDepthUnits ?notes ?methodobj ?methods
    WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?datasetName .
            FILTER regex(?datasetName, "[dsname].*", "i").
    
        ?ds le:hasChronData ?chron .
        ?chron le:modeledBy ?model .
        ?model le:hasEnsembleTable ?ensembleTable .
            OPTIONAL{?ensembleTable le:hasNotes ?notes}
        
        ?ensembleTable le:hasVariable ?ensvar .
        ?ensvar le:hasName ?ensembleVariableName .
            FILTER regex(lcase(?ensembleVariableName), "[ensembleVarName].*", "i").
        ?ensvar le:hasValues ?ensembleVariableValues
            OPTIONAL{
                ?ensvar le:hasUnits ?ensembleVariableUnitsObj .
                ?ensembleVariableUnitsObj rdfs:label ?ensembleVariableUnits .
            }
        
        ?ensembleTable le:hasVariable ?ensdepthvar .
        ?ensdepthvar le:hasName ?ensembleDepthName .
            FILTER regex(lcase(?ensembleDepthName), "[ensembleDepthVarName].*", "i").
        ?ensdepthvar le:hasValues ?ensembleDepthValues .
            OPTIONAL{
                ?ensdepthvar le:hasUnits ?ensembleDepthUnitsObj .
                ?ensembleDepthUnitsObj rdfs:label ?ensembleDepthUnits .
            }
    }
"""


QUERY_BIBLIO = """
    SELECT ?dsname ?title (GROUP_CONCAT(?authorName;separator=" and ") as ?authors) 
    ?doi ?pubyear ?year ?journal ?volume ?issue ?pages ?type ?publisher ?report ?citeKey ?edition ?institution ?url ?url2
    WHERE { 
        ?ds a le:Dataset .
        ?ds le:hasName ?dsname .
        ?ds le:hasPublication ?pub .
        OPTIONAL{?pub le:hasDOI ?doi .}
        OPTIONAL{
            ?pub le:hasAuthor ?author .
            ?author le:hasName ?authorName .
        }
        OPTIONAL{?pub le:publicationYear ?pubyear .}
        OPTIONAL{?pub le:hasYear ?year .}
        OPTIONAL{?pub le:hasTitle ?title .}
        OPTIONAL{?pub le:hasJournal ?journal .}
        OPTIONAL{?pub le:hasVolume ?volume .}
        OPTIONAL{?pub le:hasIssue ?issue .}
        OPTIONAL{?pub le:hasPages ?pages .}
        OPTIONAL{?pub le:hasType ?type .}
        OPTIONAL{?pub le:hasPublisher ?publisher .}
        OPTIONAL{?pub le:hasReport ?report .}
        OPTIONAL{?pub le:hasCiteKey ?citeKey .}
        OPTIONAL{?pub le:hasEdition ?edition .}
        OPTIONAL{?pub le:hasInstitution ?institution .}
        OPTIONAL{?pub le:hasLink ?url .}
        OPTIONAL{?pub le:hasUrl ?url2 .}
    }
    GROUP BY ?pub ?dsname ?title ?doi ?year ?pubyear ?journal ?volume ?issue ?pages ?type ?publisher ?report ?citeKey ?edition ?institution ?url ?url2
"""

QUERY_DISTINCT_VARIABLE="""
    PREFIX le: <http://linked.earth/ontology#>
    
    SELECT distinct ?variableName 
    WHERE {
        ?uri le:hasName ?variableName .
        ?uri le:hasVariableId ?TSID
    }
    

"""

QUERY_DISTINCT_PROXY = """
    PREFIX le: <http://linked.earth/ontology#>
    
    SELECT distinct ?proxy 
    WHERE {
        OPTIONAL{?uri le:hasProxy ?proxyObj .
                 ?proxyObj rdfs:label ?proxy .}
        ?uri le:hasVariableId ?TSID
    }
    

"""

QUERY_VARIABLE = """
    PREFIX le: <http://linked.earth/ontology#>

    SELECT ?uri ?TSID ?variableName 
    WHERE {
        ?uri le:hasName ?variableName .
        ?uri le:hasVariableId ?TSID
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
            ?var le:foundInDatasetName ?dsname
        }
    }
    WHERE {
        ?table le:hasVariable ?var .
        {
            {
                # level 1
                ?var le:foundInDataset ?ds .
                ?ds le:hasName ?dsname .
                ?var ?pv1 ?v1  # get primitives
                    FILTER (isLiteral(?v1)) .
            }
            UNION
            {
                # level 2
                {
                    ?var ?p1 ?o1
                        FILTER (?p1 NOT IN (le:foundInTable, le:foundInDataset)) .
                    ?o1 ?pv2 ?v2 
                        FILTER (isLiteral(?v2)) .
                } .
            }
            #UNION
            #{
            #    # level 3
            #    {
            #        ?var ?p1 ?o1
            #            FILTER (?p1 NOT IN (le:foundInTable, le:foundInDataset)) .
            #        ?o1 ?p2 ?o2
            #            FILTER (?p1 NOT IN (le:foundInTable, le:foundInDataset)) .
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
        ?ds le:hasName ?dsname .
        ?ds le:hasLocation ?loc .
        ?loc le:hasLatitude ?lat .
        ?loc le:hasLongitude ?lon .
        FILTER ( ?lat >= [latMin] && ?lat < [latMax] && ?lon >= [lonMin] && ?lon < [lonMax] ) .
    }
"""

QUERY_FILTER_ARCHIVE_TYPE = """
    SELECT ?dsname WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?dsname .
        ?ds le:hasArchiveType ?archiveTypeObj .
        ?archiveTypeObj rdfs:label ?archiveType .
        FILTER regex(?archiveType, "[archiveType].*", "i")
    }
"""

QUERY_FILTER_DATASET_NAME = """
    SELECT ?dsname WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?dsname .
        FILTER regex(?dsname, "[datasetName].*", "i")
    }
"""

QUERY_FILTER_TIME = """
    SELECT ?dsname ?minage ?maxage WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?dsname .
        
        ?ds le:hasPaleoData ?data .
        ?data le:hasMeasurementTable ?table .
        ?table le:hasVariable ?var .
        ?table le:hasVariable ?timevar .
        ?timevar le:hasName ?time_variableName .
        FILTER (regex(?time_variableName, "year.*") || regex(?time_variableName, "age.*")) .
        ?timevar le:hasMinValue ?minage .
        ?timevar le:hasMaxValue ?maxage .
}
"""

QUERY_FILTER_VARIABLE_NAME = """
    SELECT ?uri ?dsuri ?dsname ?tableuri ?id ?name WHERE {
        ?uri le:hasVariableId ?id .
        ?uri le:hasName ?name .
        FILTER regex(?name, "[name].*", "i") .
        ?uri le:foundInDataset ?dsuri .
        ?uri le:foundInDatasetName ?dataSetName .
        ?uri le:foundInTable ?tableuri .
    }
"""

QUERY_FILTER_VARIABLE_PROXY = """
    SELECT ?uri ?dsuri ?dsname ?tableuri ?id ?proxy WHERE {
        ?uri le:hasVariableId ?id .
        ?uri le:hasProxy ?proxyObj .
        ?proxyObj rdfs:label ?proxy .
        FILTER regex(?proxy, "[proxy].*", "i") .
        ?uri le:foundInDataset ?dsuri .
        ?uri le:foundInDatasetName ?dataSetName .
        ?uri le:foundInTable ?tableuri .
    }
"""

QUERY_FILTER_VARIABLE_RESOLUTION = """
    SELECT ?uri ?dsuri ?dsname ?tableuri ?id ?v WHERE {
        ?uri le:hasVariableId ?id .
        ?uri le:hasResolution ?res .
        ?res le:has[stat]Value ?v .
        FILTER(?v<[value]) .
        ?uri le:foundInDataset ?dsuri .
        ?uri le:foundInDatasetName ?dataSetName .
        ?uri le:foundInTable ?tableuri .        
    }
"""


QUERY_TIMESERIES_ESSENTIALS_PALEO ="""
    PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX le: <http://linked.earth/ontology#>

    SELECT ?dataSetName ?archiveType ?geo_meanLat ?geo_meanLon ?geo_meanElev 
    ?paleoData_variableName ?paleoData_values ?paleoData_units 
    ?paleoData_proxy ?paleoData_proxyGeneral ?time_variableName ?time_values 
    ?time_units ?depth_variableName ?depth_values ?depth_units WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?dataSetName .
            FILTER regex(?dataSetName, "[dsname].*", "i").
        
        OPTIONAL{
            ?ds le:hasArchiveType ?archiveTypeObj .
            ?archiveTypeObj rdfs:label ?archiveType .
        }
        
        ?ds le:hasLocation ?loc .
        OPTIONAL { ?loc le:hasLatitude ?geo_meanLat } .
        OPTIONAL { ?loc le:hasLongitude ?geo_meanLon } .
        OPTIONAL { ?loc le:hasElevation ?geo_meanElev } .
        
        ?ds le:hasPaleoData ?data .
        ?data le:hasMeasurementTable ?table .
        ?table le:hasVariable ?var .
        
        ?var le:hasName ?paleoData_variableName .
        FILTER (!regex(?paleoData_variableName, "year.*") && !regex(?paleoData_variableName, "age.*") && !regex(?paleoData_variableName, "depth.*")) .
   		
        ?var le:hasValues ?paleoData_values .
        OPTIONAL{
            ?var le:hasUnits ?paleoData_unitsObj .
            ?paleoData_unitsObj rdfs:label ?paleoData_units .
        }
        OPTIONAL{
            ?var le:hasProxy ?paleoData_proxyObj .
            ?paleoData_proxyObj rdfs:label ?paleoData_proxy .
        }
        OPTIONAL{
            ?var le:hasProxyGeneral ?paleoData_proxyGeneralObj .
            ?paleoData_proxyGeneralObj rdfs:label ?paleoData_proxyGeneral .
        }
        
        
        OPTIONAL{
            ?table le:hasVariable ?timevar .
            ?timevar le:hasName ?time_variableName .
                FILTER (regex(?time_variableName, "year.*") || regex(?time_variableName, "age.*")) .
            ?timevar le:hasValues ?time_values .
            OPTIONAL{
                ?timevar le:hasUnits ?time_unitsObj .
                ?time_unitsObj rdfs:label ?time_units .
            }
        }
        
        OPTIONAL{
            ?table le:hasVariable ?depthvar .
            ?depthvar le:hasName ?depth_variableName .
                FILTER (regex(?depth_variableName, "depth.*")) .
            ?depthvar le:hasValues ?depth_values .
            OPTIONAL{
                ?depthvar le:hasUnits ?depth_unitsObj .
                ?depth_unitsObj rdfs:label ?depth_units .
            }
        }
        
    }
"""

QUERY_TIMESERIES_ESSENTIALS_CHRON ="""
    PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX le: <http://linked.earth/ontology#>

    SELECT ?dataSetName ?archiveType ?geo_meanLat ?geo_meanLon ?geo_meanElev 
    ?chronData_variableName ?chronData_values ?chronData_units 
    ?time_variableName ?time_values 
    ?time_units ?depth_variableName ?depth_values ?depth_units WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?dataSetName .
            FILTER regex(?dataSetName, "[dsname].*", "i").
        
        OPTIONAL{
            ?ds le:hasArchiveType ?archiveTypeObj .
            ?archiveTypeObj rdfs:label ?archiveType .
        }
        
        ?ds le:hasLocation ?loc .
        OPTIONAL { ?loc le:hasLatitude ?geo_meanLat } .
        OPTIONAL { ?loc le:hasLongitude ?geo_meanLon } .
        OPTIONAL { ?loc le:hasElevation ?geo_meanElev } .
        
        ?ds le:hasChronData ?data .
        ?data le:hasMeasurementTable ?table .
        ?table le:hasVariable ?var .
        ?var le:hasName ?chronData_variableName .
   		
        ?var le:hasValues ?chronData_values .
        OPTIONAL{
            ?var le:hasUnits ?chronData_unitsObj .
            ?chronData_unitsObj rdfs:label ?chronData_units .
        }
        
        OPTIONAL{?table le:hasVariable ?timevar .
        ?timevar le:hasName ?time_variableName .
            FILTER (regex(?time_variableName, "year.*") || regex(?time_variableName, "age.*")) .
        ?timevar le:hasValues ?time_values .
            OPTIONAL{
                ?timevar le:hasUnits ?time_unitsObj .
                ?time_unitsObj rdfs:label ?time_units .
            }
        }
        
        OPTIONAL{?table le:hasVariable ?depthvar .
        ?depthvar le:hasName ?depth_variableName .
            FILTER (regex(?depth_variableName, "depth.*")) .
        ?depthvar le:hasValues ?depth_values .
            OPTIONAL{
                ?depthvar le:hasUnits ?depth_unitsObj .
                ?depth_unitsObj rdfs:label ?depth_units .
            }
        }
    }
"""

QUERY_VARIABLE_PROPERTIES="""
    PREFIX le: <http://linked.earth/ontology#>
    SELECT  DISTINCT ?property where {
    
    ?ds a le:Dataset .
    
    {?ds le:hasPaleoData ?data .
    ?data le:hasMeasurementTable ?table .
    ?table le:hasVariable ?var .
    ?var ?property ?value .}
    
    UNION
    
    {OPTIONAL{?ds le:hasChronData ?data1 .
    ?data1 le:hasMeasurementTable ?table1 .
    ?table1 le:hasVariable ?var1 .
    ?var1 ?property ?value1 .}}
    
    }
"""

## At the LiPDSeries level

QUERY_LiPDSERIES_PROPERTIES="""
    SELECT DISTINCT ?p WHERE {
        ?uri ?p ?v .}
    """

QUERY_DATASET_PROPERTIES="""
    PREFIX le: <http://linked.earth/ontology#>
    SELECT DISTINCT ?property where {
    ?ds a le:Dataset .
    ?ds ?property ?value .
    }
"""

QUERY_MODEL_PROPERTIES="""
    PREFIX le: <http://linked.earth/ontology#>
    SELECT  DISTINCT ?property where {
    
    ?ds a le:Dataset .
    
    {OPTIONAL{?ds le:hasPaleoData ?data .
              ?data le:modeledBy ?paleomodel .
              ?paleomodel ?property ?value .}}
    
    UNION
    
    {OPTIONAL{?ds le:hasChronData ?chron .
              ?chron le:modeledBy ?chronmodel .
              ?chronmodel ?property ?value .}}
    
    }
"""

QUERY_VARIABLE_ESSENTIALS="""
    PREFIX le: <http://linked.earth/ontology#>
    SELECT ?dataSetName ?archiveType ?name ?TSID ?values ?units ?proxy where {
        ?var le:hasName ?name .
        ?var le:foundInDatasetName ?dataSetName .
            #FILTER regex(?dataSetName, "[dsname].*", "i").
            
        OPTIONAL{?var le:hasVariableId ?TSID .}
        ?var le:hasValues ?values .
        OPTIONAL{
            ?var le:hasUnits ?unitsObj .
            ?unitsObj rdfs:label ?units .
        }
        OPTIONAL{
            ?var le:hasArchiveType ?archiveTypeObj .
            ?archiveTypeObj rdfs:label ?archiveType .
        }
        OPTIONAL{
            ?var le:hasProxy ?paleoData_proxyObj .
            ?paleoData_proxyObj rdfs:label ?paleoData_proxy .
        }    
    }
"""

QUERY_LOCATION ="""
    PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX le: <http://linked.earth/ontology#>

    SELECT ?dataSetName ?geo_meanLat ?geo_meanLon ?geo_meanElev WHERE {
        ?ds a le:Dataset .
        ?ds le:hasName ?dataSetName .
            FILTER regex(?dataSetName, "[dsname].*", "i").
        
        ?ds le:hasLocation ?loc .
        OPTIONAL { ?loc le:hasLatitude ?geo_meanLat } .
        OPTIONAL { ?loc le:hasLongitude ?geo_meanLon } .
        OPTIONAL { ?loc le:hasElevation ?geo_meanElev } .
    }
"""

QUERY_FILTER_COMPILATION="""
        SELECT DISTINCT ?dataSetName WHERE {
            ?ds a le:Dataset .
            ?ds le:hasName ?dataSetName .
        
            ?ds le:hasPaleoData ?data .
            ?data le:hasMeasurementTable ?table .
            ?table le:hasVariable ?var .
            
            ?var le:partOfCompilation ?compilation . 
            ?compilation le:hasName ?compilationName .
            FILTER regex(?compilationName, "[compilationName].*", "i")}
            
    """

QUERY_COMPILATION_NAME="""
        PREFIX le: <http://linked.earth/ontology#>
        
        SELECT DISTINCT ?compilationName WHERE {
            ?var a le:Variable .
            ?var le:partOfCompilation ?compilation . 
            ?compilation le:hasName ?compilationName .}
"""
