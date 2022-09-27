SCHEMA = {
    'Dataset': {
        '@id': ['{dataSetName}'],
        '@fromJson': ['addExtraDatasetProperties'],
        '@toJson': ['getVariableArchiveTypes'],
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
            'fromJson': 'parsePerson'
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
            'fromJson': 'parsePersons'
        },
        'investigators': {
            'name': 'contributor',
            'schema': 'Person',
            'hack': True,
            'fromJson': 'parsePersonsString'
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
            'fromJson': 'parseLocation',
            'toJson': 'locationToJson'
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
            'fromJson': 'getGoogleSpreadsheetURL',
            'toJson': 'getGoogleSpreadsheetKey'
        },
        'dataSetVersion': { 
            'name': 'datasetVersion' 
        }
    },
    'ChangeLog': {
        '@id': ['{@parent.@id}', '.ChangeLog.', '{@index}'],
        '@category': 'ChangeLog'
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
        '@fromJson': ['setIdentifierProperties'],
        '@toJson': ['createPublicationIdentifier'],
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
        'author': {
            'name': 'author',
            'schema': 'Person',
            'multiple': True,
            'fromJson': 'parsePersons'
        },
        'authors': {
            'name': 'author',
            'schema': 'Person',
            'fromJson': 'parsePersonsString',
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
            'name': 'foundInMeasurementTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'model': {
            'alternatives': ['paleoModel'],            
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
            'name': 'foundInMeasurementTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'model': {
            'alternatives': ['chronModel'],            
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
        '@fromJson': ['setInterVariableLinks'],
        'filename': { 
            'name': 'hasFileName', 
            'type': 'File' 
        },
        'columns': {
            'name': 'includesVariable',
            'multiple': True,
            'schema': 'Variable'
        }
    },
    'Variable': {
        '@id': [
            '{foundInTable|@parent.@id}',
            '.',
            '{TSid|tsid}',
            '.',
            '{variableName|name}'
        ],
        '@fromJson': [
            'setVariableCategory',
            'wrapUncertainty',
            'createProxySystem',
            'addFoundInTable',
            'addVariableValues'
        ],
        '@toJson': [
            'setVariableType',
            'unwrapUncertainty',
            'extractFromProxySystem',
            'removeFoundInTable',
            'removeDepthProperty'
        ],
        'number': { 
            'name': 'hasColumnNumber', 
            'type': 'integer',
            'multiple': True
        },
        'TSid': { 
            'name': 'hasVariableID', 
            'alternates': ['tsid'] 
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
        'hasMaxValue': { 'type': 'float' },
        'hasMinValue': { 'type': 'float' },
        'hasMeanValue': { 'type': 'float' },
        'hasMedianValue': { 'type': 'float' },
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
        'useInGlobalTemperatureAnalysis': { 
            'name': 'useInPAGES2kGlobalTemperatureAnalysis' 
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
        'hasMaxValue': { 'type': 'float' },
        'hasMinValue': { 'type': 'float' },
        'hasMeanValue': { 'type': 'float' },
        'hasMedianValue': { 'type': 'float' },        
        #'@fromJson': ['valuesToString'],
        #'@toJson': ['valuesToArray']
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
        '@toJson': ['changeSeasonalityType'],
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
        '@fromJson': ['wrapIntegrationTime'],
        '@toJson': ['unwrapIntegrationTime'],
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
        '@fromJson': ['wrapUncertainty'],
        '@toJson': ['unwrapUncertainty'],
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
        '@fromJson': ['wrapUncertainty'],
        '@toJson': ['unwrapUncertainty'],
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