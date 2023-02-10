"""
The SCHEMA dictionary defines the conversion from and to RDF and LiPD
@fromJson refers to functions in LipdToRDF
@toJson refers to functions in RDFToLiPD
"""

SCHEMA = {
    'Dataset': {
        '@id': ['{dataSetName}'],
        '@fromJson': ['_add_extra_dataset_properties'],
        '@toJson': ['_get_variable_archive_types'],
        'dataSetName': { 
            'name': 'name', 
            'alternates': ['paleoArchiveName'] 
        },
        'originalDataURL': { 
            'name': 'hasLink', 
            'alternates': ['dataURL'] 
        },
        'dataContributor': {
            'name': 'author',
            'schema': 'Person',
            'alternates': ['whoEnteredinDB', 'MetadataEnteredByWhom'],
            'fromJson': '_parse_person'
        },
        'archiveType': {
            'name': 'proxyArchiveType',
            'alternates':[
                'archive',
                'paleoDataArchive',
                'paleoData_Archive'
            ]
        },
        'changelog': {
            'name': 'hasChangeLog',
            'schema': 'ChangeLog'
        },
        'investigator': {
            'name': 'contributor',
            'schema': 'Person',
            'multiple': True,
            'fromJson': '_parse_persons'
        },
        'investigators': {
            'name': 'contributor',
            'schema': 'Person',
            'hack': True,
            'fromJson': '_parse_persons_string'
        },
        'funding': { 
            'name': 'fundedBy', 
            'multiple': True, 
            'schema': 'Funding' 
        },
        'pub': { 
            'name': 'publishedIn', 
            'multiple': True, 
            'schema': 'Publication' 
        },
        'geo': {
            'name': 'collectedFrom',
            'schema': 'Location',
            'fromJson': '_parse_location',
            'toJson': '_location_to_json'
        },
        'paleoData': {
            'name': 'includesPaleoData',
            'multiple': True,
            'schema': 'PaleoData'
        },
        'chronData': {
            'name': 'includesChronData',
            'multiple': True,
            'schema': 'ChronData'
        },
        'googleSpreadSheetKey': {
            'name': 'hasSpreadsheetLink',
            'fromJson': '_get_google_spreadsheet_url',
            'toJson': '_get_google_spreadsheet_key'
        },
        'dataSetVersion': { 
            'name': 'datasetVersion' 
        }
    },
    'Compilation': {
        '@id': ['{compilationName}', '.', '{@id}'],
        'compilationName': {
            'name': 'name'
        },
        'compilationVersion': {
            'name': 'version'
        }
    },
    'ChangeLog': {
        '@id': ['{@parent.@id}', '.ChangeLog.', '{@index}'],
        '@category': 'ChangeLog',
        'changes': {
            'name': 'hasChanges',
            'type': 'Individual'
        }
    },
    'Funding': {
        '@id': [
            '{fundingAgency|agency}',
            '.',
            '{fundingGrant|grant}'
        ],
        'agency': { 
            'name': 'fundingAgency', 
            'alternates': ['fundingAgency'] 
        },
        'grant': {
            'name': 'grantNumber',
            'multiple': True,
            'alternates': ['fundingGrant']
        },
        'country': {
            'name': 'fundingCountry',
            'alternates': ['fundingCountry']
        }
    },
    'Publication': {
        '@id': [
            'Publication.',
            '{identifier.0.id|@parent.dataSetName}',
            '{index}'
        ],
        '@fromJson': ['_set_identifier_properties'],
        '@toJson': ['_create_publication_identifier'],
        'title': { 
            'name': 'title' 
        },
        'year': { 
            'name': 'publicationYear', 
            'alternates': ['pubYear'] 
        },
        'citation': { 
            'name': 'citation', 
            'type': 'string',
            'alternates': ['reference'] 
        },
        'link': { 
            'name': 'hasLink', 
            'multiple': True 
        },
        'doi': {
            'name': 'hasDOI',
            'type': 'string'
        },
        'author': {
            'name': 'author',
            'schema': 'Person',
            'multiple': True,
            'fromJson': '_parse_persons'
        },
        'authors': {
            'name': 'author',
            'schema': 'Person',
            'fromJson': '_parse_persons_string',
            'hack': True
        }
    },
    'PaleoData': {
        '@id': [
            '{@parent.dataSetName}',
            '.PaleoData',
            '{@index}'
        ],
        'paleoDataName': { 
            'name': 'name' 
        },
        'measurementTable': {
            'alternates': ['paleoMeasurementTable'],
            'name': 'foundInMeasurementTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'model': {
            'alternates': ['paleoModel'],            
            'name': 'paleoModeledBy',
            'multiple': True,
            'schema': 'Model',
            'category': 'PaleoModel'
        }
    },
    'ChronData': {
        '@id': [
            '{@parent.dataSetName}',
            '.ChronData',
            '{@index}'
        ],
        'measurementTable': {
            'alternates': ['chronMeasurementTable'],
            'name': 'foundInMeasurementTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'model': {
            'alternates': ['chronModel'],            
            'name': 'chronModeledBy',
            'multiple': True,
            'schema': 'Model',
            'category': 'ChronModel'
        }
    },
    'Model': {
        '@id': ['{@parent.@id}', '.Model', '{@index}'],
        'method': { 
            'name': 'hasCode', 
            'schema': 'SoftwareCode' 
        },
        'summaryTable': {
            'name': 'foundInSummaryTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'ensembleTable': {
            'name': 'foundInEnsembleTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'distributionTable': {
            'name': 'foundInDistributionTable',
            'multiple': True,
            'schema': 'DataTable'
        }
    },
    'SoftwareCode': {
        '@id': {
            '{@parent.@id}',
            '.',
            '{name|software}'
        },
        'runCommand': { 
            'name': 'hasExecutionCommand' 
        },
        'runEnv': { 
            'name': 'hasExecutionEnvironment' 
        },
        'parameters': { 
            'type': 'string' 
        },
        'software': { 
            'name': 'name' 
        }
    },
    'DataTable': {
        '@id': ['{filename}', '_trunc(4)'],
        '@fromJson': ['_set_inter_variable_links'],
        'filename': { 
            'name': 'hasFileName', 
            'type': 'File' 
        },
        'columns': {
            'name': 'includesVariable',
            'multiple': True,
            'schema': 'Variable'
        },
        'missingValue': { 
            'name': 'hasMissingValue' 
        }
    },
    'Variable': {
        '@id': [
            '{foundInTable|@parent.@id}',
            '.',
            '{TSid|tsid|tSid}',
            '.',
            '{variableName|name}'
        ],
        '@fromJson': [
            '_set_variable_category',
            '_wrap_uncertainty',
            '_create_proxy_system',
            '_add_found_in_table',
            '_add_variable_values',
            '_stringify_column_numbers_array'
        ],
        '@toJson': [
            '_set_variable_type',
            '_unwrap_uncertainty',
            '_extract_from_proxy_system',
            '_remove_found_in_table',
            '_remove_depth_property',
            '_extract_variable_values',
            '_unarray_column_number'
        ],
        'number': { 
            'name': 'hasColumnNumber', 
            'type': 'integer'
        },
        'TSid': { 
            'name': 'hasVariableID', 
            'alternates': ['tsid', 'tSid'] 
        },
        'variableName': { 
            'name': 'name' 
        },
        'units': { 
            'name': 'hasUnits' 
        },
        'measurementMethod': { 
            'name': 'method' 
        },
        'measurementStandard': { 
            'name': 'standard' 
        },
        'missingValue': { 
            'name': 'hasMissingValue' 
        },
        'hasMaxValue': { 
            'name': 'hasMaxValue', 
            'alternates': ['hasMax'], 
            'type': 'float' 
        },
        'hasMinValue': { 
            'name': 'hasMinValue', 
            'alternates': ['hasMin'], 
            'type': 'float' 
        },
        'hasMeanValue': { 
            'name': 'hasMeanValue', 
            'alternates': ['hasMean'], 
            'type': 'float' 
        },
        'hasMedianValue': { 
            'name': 'hasMedianValue', 
            'alternates': ['hasMedian'], 
            'type': 'float' 
        },
        'instrument': {
            'name': 'measuredBy',
            'type': 'Individual',
            'category': 'Instrument'
        },
        'calibration': {
            'name': 'calibratedVia',
            'schema': 'CalibrationModel',
            'multiple': True
        },
        'interpretation': {
            'name': 'interpretedAs',
            'schema': 'Interpretation',
            'category': 'Interpretation',
            'multiple': True
        },
        'hasResolution': {
            'alternates': ['resolution'],
            'name': 'hasResolution',
            'category': 'Resolution',
            'schema': 'Resolution',
            'alternates': ['hasResolution']
        },
        'inferredFrom': { 
            'schema': 'Variable', 
            'category': 'MeasuredVariable' 
        },
        'hasUncertainty': { 
            'schema': 'Uncertainty', 
            'multiple': True 
        },
        'hasValues': {
            'type': 'string'
        },
        'foundInTable': {
            'type': 'Individual'
        },
        'hasProxySystem': {
            'type': 'Individual'
        },
        'takenAtDepth': {
            'type': 'Individual'
        },
        'inCompilationBeta': {
            'name': 'partOfCompilation',
            'schema': 'Compilation',
            'category': 'Compilation'
        }
    },
    'ProxySystemModel': {
        '@id': ['{@parent.@id}', '.ProxySystemModel'],
        'method': { 
            'name': 'hasCode', 
            'schema': 'SoftwareCode' 
        }
    },
    'PhysicalSample': {
        'hasidentifier': { 
            'name': 'hasIGSN' 
        },
        'hasname': { 
            'name': 'name' 
        },
        'housedat': { 
            'name': 'housedAt' 
        }
    },
    'Resolution': {
        '@id': ['{@parent.@id}', '.Resolution'],
        'hasMaxValue': { 'name': 'hasMaxValue', 'alternates': ['hasMax'], 'type': 'float' },
        'hasMinValue': { 'name': 'hasMinValue', 'alternates': ['hasMin'], 'type': 'float' },
        'hasMeanValue': { 'name': 'hasMeanValue', 'alternates': ['hasMean'], 'type': 'float' },
        'hasMedianValue': { 'name': 'hasMedianValue', 'alternates': ['hasMedian'], 'type': 'float' },
        'units': { 
            'name': 'hasUnits' 
        }    
        #'@fromJson': ['_values_to_string'],
        #'@toJson': ['_values_to_array']
    },
    'Location': {
        '@id': ['{@parent.dataSetName}', '.Location'],
        'siteName': { 
            'name': 'name' 
        },
        'coordinates': { 
            'type': 'Geographic_coordinate' 
        },
        'coordinatesFor': { 
            'type': 'Individual' 
        }
    },
    'Interpretation': {
        '@id': [
            '{@parent.@id}',
            '.Interpretation',
            '{@index}'
        ],
        '@toJson': ['_change_seasonality_type'],
        'interpDirection': {
            'name': 'interpretationDirection',
            'alternates': [
                'dir',
                'interpDir',
                'interpdirection',
                'direction'
            ]
        },
        'variable': { 
            'name': 'name' 
        },
        'variableDetail': { 
            'name': 'detail', 
            'alternates': ['variabledetail'] 
        },
        'integrationTime': {
            'name': 'hasIntegrationTime',
            'type': 'Individual',
            'schema': 'IntegrationTime'
        },
        'rank': { 'name': 'hasRank' },
        'basis': { 'name': 'relevantQuote' },
        'local': { 'name': 'isLocal' }
    },
    'IsotopeInterpretation': {
        '@id': {
            '{@parent.@id}',
            '.IsotopeInterpretation',
            '{@index}'
        },
        '@fromJson': ['_wrap_integration_time'],
        '@toJson': ['_unwrap_integration_time'],
        'integrationTime': {
            'name': 'hasIntegrationTime',
            'type': 'Individual',
            'schema': 'IntegrationTime'
        },
        'independentVariable': {
            'name': 'hasIndependentVariable',
            'schema': 'IndependentVariable',
            'multiple': True
        }
    },
    'IntegrationTime': {
        '@fromJson': ['_wrap_uncertainty'],
        '@toJson': ['_unwrap_uncertainty'],
        'basis': { 
            'name': 'relevantQuote' 
        },
        'units': { 
            'name': 'hasUnits' 
        },
        'independentVariable': {
            'name': 'hasIndependentVariable',
            'schema': 'IndependentVariable',
            'multiple': True
        }
    },
    'IndependentVariable': {
        '@id': {
            '{@parent.@id}',
            '.',
            '{name}'
        },
        'basis': { 
            'name': 'relevantQuote' 
        },
        'direction': {
            'name': 'interpretationDirection',
            'alternates': ['dir', 'interpDir', 'interpDirection']
        },
        'mathematicalRelation': { 
            'name': 'equation' 
        },
        'rank': { 
            'name': 'hasRank' 
        }
    },
    'CalibrationModel': {
        '@id': ['{@parent.@id}', '.Calibration'],
        '@fromJson': ['_wrap_uncertainty'],
        '@toJson': ['_unwrap_uncertainty'],
        'reference': { 
            'name': 'relevantQuote' 
        }
    },
    'Person': { '@id': ['{name}'] },
    'Uncertainty': {
        '@id': {
            '{@parent.@id}',
            '.Uncertainty',
            '{@index}'
        }
    }
}