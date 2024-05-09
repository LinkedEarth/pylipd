from .synonyms import SYNONYMS

"""
The SCHEMA dictionary defines the conversion from and to RDF and LiPD
@fromJson refers to functions in LipdToRDF
@toJson refers to functions in RDFToLiPD
"""

SCHEMA = {
    'Dataset': {
        '@id': ['{dataSetName}'],
        '@toJson_pre': [
            '_set_archive_type_label'
        ],
        'datasetId': {
            'name': 'hasDatasetId'
        },
        'dataSetName': { 
            'name': 'hasName', 
            'alternates': ['paleoArchiveName'] 
        },
        'dataSource': { 
            'name': 'hasDataSource'
        },
        'originalDataURL': { 
            'name': 'hasOriginalDataUrl', 
            'alternates': ['originalDataUrl', 'additionalDataUrl', 'originalDataSource', 'originalDataURL', 'originalSourceUrl', 'paleoData_WDSPaleoUrl'] 
        },
        'dataContributor': {
            'name': 'hasContributor',
            'schema': 'Person',
            'alternates': ['whoEnteredinDB', 'MetadataEnteredByWhom', 'contributorName'],
            'fromJson': '_parse_persons'
        },
        'archiveType': {
            'name': 'hasArchiveType', 
            'alternates':[
                'archive',
                'paleoDataArchive',
                'paleoData_Archive',
                'Archive'
            ],
            'type': 'Individual',
            'synonyms': SYNONYMS['ARCHIVES']['ArchiveType'],
            'skip_auto_convert_to_json': True
        },
        'changelog': {
            'name': 'hasChangeLog',
            'schema': 'ChangeLog'
        },
        'notes': {
            'name': 'hasNotes'
        },
        'collectionName': {
            'name': 'hasCollectionName',
            'alternates': ['collectionName1', 'collectionName2', 'collectionName3']
        },
        'collectionYear': {
            'name': 'hasCollectionYear'
        },
        'investigator': {
            'name': 'hasInvestigator',
            'alternates': ['investigators'],
            'schema': 'Person',
            'multiple': True,
            'fromJson': '_parse_persons'
        },
        'creator': {
            'name': 'hasCreator',
            'schema': 'Person',
            'multiple': True,
            'fromJson': '_parse_persons'
        },
        'funding': { 
            'name': 'hasFunding', 
            'multiple': True, 
            'schema': 'Funding' 
        },
        'pub': { 
            'name': 'hasPublication', 
            'multiple': True, 
            'schema': 'Publication' 
        },
        'geo': {
            'name': 'hasLocation',
            'schema': 'Location',
            'fromJson': '_parse_location',
            'toJson': '_location_to_json'
        },
        'paleoData': {
            'name': 'hasPaleoData',
            'multiple': True,
            'schema': 'PaleoData'
        },
        'chronData': {
            'name': 'hasChronData',
            'multiple': True,
            'schema': 'ChronData'
        },
        'googleSpreadSheetKey': {
            'name': 'hasSpreadsheetLink',
            'fromJson': '_get_google_spreadsheet_url',
            'toJson': '_get_google_spreadsheet_key'
        },
        'dataSetVersion': { 
            'name': 'hasVersion' 
        }
    },
    'Compilation': {
        '@id': ['{compilationName}', '.', '{@id}'],
        'compilationName': {
            'name': 'hasName'
        },
        'compilationVersion': {
            'name': 'hasVersion'
        }
    },
    'ChangeLog': {
        '@id': ['{@parent.@id}', '.ChangeLog.', '{@index}'],
        '@category': 'ChangeLog',
        'changes': {
            'name': 'hasChanges',
            'type': 'Individual'
        },
        'notes': {
            'name': 'hasNotes'
        }
    },
    'Funding': {
        '@id': [
            '{fundingAgency|agency}',
            '.',
            '{fundingGrant|grant}'
        ],
        'agency': { 
            'name': 'hasFundingAgency', 
            'alternates': ['fundingAgency'] 
        },
        'grant': {
            'name': 'hasGrant',
            'multiple': True,
            'alternates': ['fundingGrant']
        },
        'country': {
            'name': 'hasFundingCountry',
            'alternates': ['fundingCountry']
        },
        'investigator': {
            'name': 'hasInvestigator',
            'schema': 'Person',
            'multiple': True,
            'fromJson': '_parse_persons'
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
            'name': 'hasTitle' 
        },
        'abstract': { 
            'name': 'hasAbstract'
        },
        'institution': { 
            'name': 'hasInstitution'
        },
        'issue': { 
            'name': 'hasIssue'
        },
        'journal': { 
            'name': 'hasJournal'
        },    
        'volume': { 
            'name': 'hasVolume',
            'type': 'string'
        },
        'pages': { 
            'name': 'hasPages'
        },
        'year': { 
            'name': 'hasYear', 
            'alternates': ['pubYear'] 
        },        
        'publisher': { 
            'name': 'hasPublisher'
        },
        'report': { 
            'name': 'hasReport'
        },
        'type': { 
            'name': 'hasType'
        },
        'citation': { 
            'name': 'hasCitation', 
            'type': 'string'
        },
        'citeKey': { 
            'name': 'hasCiteKey', 
            'type': 'string'
        },
        'url': { 
            'name': 'hasUrl', 
            'alternates': ['link'],
            'multiple': True 
        },
        'dataUrl': { 
            'name': 'hasDataUrl', 
            'alternates': ['data_Url', 'pubDataUrl'],
            'multiple': True 
        },
        'doi': {
            'name': 'hasDOI',
            'type': 'string'
        },
        'author': {
            'name': 'hasAuthor',
            'alternates': ['authors'],
            'schema': 'Person',
            'multiple': True,
            'fromJson': '_parse_persons'
        },
        'firstauthor': {
            'name': 'hasFirstAuthor',
            'alternates': ['firstAuthor'],
            'schema': 'Person',
            'multiple': True,
            'fromJson': '_parse_persons'
        }
    },
    'PaleoData': {
        '@id': [
            '{@parent.dataSetName}',
            '.PaleoData',
            '{@index}'
        ],
        'paleoDataName': { 
            'name': 'hasName' 
        },
        'measurementTable': {
            'alternates': ['paleoMeasurementTable'],
            'name': 'hasMeasurementTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'model': {
            'alternates': ['paleoModel'],            
            'name': 'modeledBy',
            'multiple': True,
            'schema': 'Model'
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
            'name': 'hasMeasurementTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'model': {
            'alternates': ['chronModel'],            
            'name': 'modeledBy',
            'multiple': True,
            'schema': 'Model'
        }
    },
    'Model': {
        '@id': ['{@parent.@id}', '.Model', '{@index}'],
        'method': { 
            'name': 'hasCode'
        },
        'summaryTable': {
            'name': 'hasSummaryTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'ensembleTable': {
            'name': 'hasEnsembleTable',
            'multiple': True,
            'schema': 'DataTable'
        },
        'distributionTable': {
            'name': 'hasDistributionTable',
            'multiple': True,
            'schema': 'DataTable'
        }
    },    
    'DataTable': {
        '@id': ['{filename}', '_trunc(4)'],
        'filename': { 
            'name': 'hasFileName'
        },
        'columns': {
            'name': 'hasVariable',
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
            '_wrap_uncertainty',
            '_add_found_in_table',
            '_add_found_in_dataset',
            '_add_variable_values',
            '_add_standard_variable',
            '_stringify_column_numbers_array'
        ],
        '@toJson_pre': [
            '_remove_found_in_table',
            '_remove_found_in_dataset',
            '_set_variable_name_from_standard_variable_label',
            '_set_units_label',
            '_set_proxy_label',
            '_set_proxy_general_label'
        ],
        '@toJson': [
            '_unwrap_uncertainty',
            '_extract_variable_values',
            '_unarray_column_number'
        ],
        'number': { 
            'name': 'hasColumnNumber', 
            'type': 'integer'
        },
        'TSid': { 
            'name': 'hasVariableId', 
            'alternates': ['tsid', 'tSid'] 
        },
        'variableName': { 
            'name': 'hasName' 
        },
        'variableType': { 
            'name': 'hasType' 
        },
        'units': { 
            'name': 'hasUnits',
            'type': 'Individual',
            'synonyms': SYNONYMS['UNITS']['PaleoUnit'],
            'skip_auto_convert_to_json': True
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
        'description': {
            'name': 'hasDescription'
        },
        'isPrimary': {
            'name': 'isPrimary',
            'type': 'boolean'
        },
        'isComposite': {
            'name': 'isComposite',
            'type': 'boolean'
        },
        'measurementInstrument': {
            'name': 'hasInstrument',
            'type': 'Individual',
            'category': 'Instrument'
        },
        'calibration': {
            'name': 'calibratedVia',
            'schema': 'Calibration',
            'type': 'Individual',
            'multiple': True
        },
        'interpretation': {
            'name': 'hasInterpretation',
            'schema': 'Interpretation',
            'category': 'Interpretation',
            'type': 'Individual',
            'multiple': True
        },
        'resolution': {
            'name': 'hasResolution',
            'category': 'Resolution',
            'schema': 'Resolution',
            'type': 'Individual',
            'alternates': ['hasResolution']
        },
        'physicalSample': {
            'type': 'Individual',
        },
        'uncertainty': { 
            'name': 'hasUncertainty',
            'schema': 'Uncertainty', 
            'type': 'Individual'
        },
        'proxy': {
            'name': 'hasProxy',
            'type': 'Individual',
            'synonyms': SYNONYMS['PROXIES']['PaleoProxy'],
            'skip_auto_convert_to_json': True
        },
        'proxyGeneral': {
            'name': 'hasProxyGeneral',
            'type': 'Individual',
            'synonyms': SYNONYMS['PROXIES']['PaleoProxyGeneral'],
            'skip_auto_convert_to_json': True
        },
        'inCompilationBeta': {
            'name': 'partOfCompilation',
            'schema': 'Compilation',
            'category': 'Compilation'
        },
        'compilation_nest': {
            'name': 'hasCompilationNest',
            'alternates': ['pages2kRegion', 'paleoDIVERSiteId', 'sisalSiteId', 'LegacyClimateDatasetId', 
                           'LegacyClimateSiteId', 'ch2kCoreCode', 'coralHydro2kGroup', 'iso2kCertification', 
                           'iso2kUI', 'ocean2kID', 'pages2kId', 'pages2kID', 'QCCertification', 'SISALEntityID' ]
        },
        'notes': {
            'name': 'hasNotes',
            'alternates': ['qcNotes', 'qCNotes', 'qCnotes', 'qcnotes', 'QCnotes', 'QCNotes']
        },
        'hasValues': {
            'type': 'string'
        },
        'foundInTable': {
            'type': 'Individual'
        },
        'foundInDataset': {
            'type': 'Individual'
        },
        'hasStandardVariable': {
            'type': 'EnumeratedIndividual'
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
        '@toJson_pre': [
            '_set_units_label'
        ],
        'hasMaxValue': { 'name': 'hasMaxValue', 'alternates': ['hasMax'], 'type': 'float' },
        'hasMinValue': { 'name': 'hasMinValue', 'alternates': ['hasMin'], 'type': 'float' },
        'hasMeanValue': { 'name': 'hasMeanValue', 'alternates': ['hasMean'], 'type': 'float' },
        'hasMedianValue': { 'name': 'hasMedianValue', 'alternates': ['hasMedian'], 'type': 'float' },
        'units': { 
            'name': 'hasUnits',
            'type': 'Individual',
            'synonyms': SYNONYMS['UNITS']['PaleoUnit'],
            'skip_auto_convert_to_json': True
        }
    },
    'Location': {
        '@id': ['{@parent.dataSetName}', '.Location'],
        'coordinates': { 
            'type': 'Geographic_coordinate' 
        },
        'coordinatesFor': { 
            'type': 'Individual' 
        },
        'continent': { 'name': 'hasContinent' },
        'country': { 'name': 'hasCountry' },
        'countryOcean': { 'name': 'hasCountryOcean' },
        'description': { 'name': 'hasDescription' },
        'elevation': { 'name': 'hasElevation' },
        'geometryType': { 'name': 'hasGeometryType' },
        'latitude': { 'name': 'hasLatitude' },
        'longitude': { 'name': 'hasLongitude' },
        'locationName': { 'name': 'hasLocationName', 'alternates': ['secondarySiteName'] },
        'ocean': { 'name': 'hasOcean', 'alternates': ['ocean2'] },
        'siteName': { 'name': 'hasSiteName' },
        'notes': { 'name': 'hasNotes' }
    },
    'Interpretation': {
        '@id': [
            '{@parent.@id}',
            '.Interpretation',
            '{@index}'
        ],
        '@toJson_pre': [
            '_set_units_label',
            '_set_seasonality_labels',
        ],        
        'variable': { 
            'name': 'hasVariable',
            'type': 'Individual',
            'synonyms': SYNONYMS['INTERPRETATION']['InterpretationVariable'],
            'skip_auto_convert_to_json': True
        },
        'variableGeneral': { 
            'name': 'hasVariableGeneral',
            'alternates': ['variableGroup']
        },
        'variableGeneralDirection': { 
            'name': 'hasVariableGeneralDirection',
            'alternates': ['variableGroupDirection'] 
        },
        'variableDetail': { 
            'name': 'hasVariableDetail', 
            'alternates': ['variabledetail'] 
        },        
        'seasonality': { 
            'name': 'hasSeasonality',
            'type': 'Individual',
            'synonyms': SYNONYMS['INTERPRETATION']['InterpretationSeasonality'],
            'skip_auto_convert_to_json': True
        },
        'seasonalityOriginal': { 
            'name': 'hasSeasonalityOriginal',
            'type': 'Individual',
            'synonyms': SYNONYMS['INTERPRETATION']['InterpretationSeasonality'],
            'skip_auto_convert_to_json': True
        },
        'seasonalityGeneral': { 
            'name': 'hasSeasonalityGeneral',
            'type': 'Individual',
            'synonyms': SYNONYMS['INTERPRETATION']['InterpretationSeasonality'],
            'skip_auto_convert_to_json': True
        },
        'integrationTime': {
            'name': 'hasIntegrationTime',
            'type': 'Individual',
            'schema': 'IntegrationTime'
        },
        'notes': { 'name': 'hasNotes' },
        'rank': { 'name': 'hasRank' }, # TODO: Auto-create if it doesnt exist
        'basis': { 'name': 'hasBasis' },
        'scope': { 'name': 'hasScope' },
        'mathematicalRelation': { 'name': 'hasMathematicalRelation' },
        'direction': { 
            'name': 'hasInterpretationDirection', 
            'alternates': ['interpDirection']
        },
        'local': { 
            'name': 'isLocal', 
            'alternates': ['local']
        }
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
            'name': 'hasUnits',
            'type': 'Individual',
            'synonyms': SYNONYMS['UNITS']['PaleoUnit']
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
    'Calibration': {
        '@id': ['{@parent.@id}', '.Calibration'],
        '@fromJson': ['_wrap_uncertainty'],
        '@toJson': ['_unwrap_uncertainty'],
        'datasetRange': {
            'name': 'hasDatasetRange'
        },
        'doi': {
            'name': 'hasDOI',
            'alternates': ['calibrationDOI', 'hasDOI', 'transferFunctionDOI']
        },
        'equation': {
            'name': 'hasEquation',
            'alternates': ['calibrationEquation']
        },
        'equationIntercept': {
            'name': 'hasDatasetRange'
        },
        'equationR2': {
            'name': 'hasDatasetRange'
        },
        'equationSlope': {
            'name': 'hasDatasetRange'
        },
        'equationSlopeUncertainty': {
            'name': 'hasDatasetRange'
        },
        'method': {
            'name': 'hasDatasetRange'
        },
        'methodDetail': {
            'name': 'hasDatasetRange'
        },
        'proxyDataset': {
            'name': 'hasProxyDataset',
            'alternates': ['transferFunctionTrainingSet']
        },
        'targetDataset': {
            'name': 'hasTargetDataset',
            'alternates': ['target', 'dataset']
        },
        'hasSeasonality': {
            'name': 'seasonality',
            'alternates': ['transferFunctionTrainingSet']
        },
        'notes': {
            'name': 'hasNotes',
            'alternates': ['Note']
        },
        'uncertainty': { 
            'name': 'hasUncertainty',
            'alternates': ['uncertainty', 'calibrationUncertainty', 'temperature12kUncertainty', 'transferFunctionUncertainty'],
        },     
        'hasUncertainty': {
            'type': 'Individual',
            'schema': 'Uncertainty'
        }
    },
    'Person': { 
        '@id': ['{name}'],
        'name': {
            'name': 'hasName'
        }
    },
    'Uncertainty': {
        '@id': {
            '{@parent.@id}',
            '.Uncertainty',
            '{@index}'
        },
        'uncertaintyType': { 
            'name': 'hasUncertaintyType'
        }
    }
}