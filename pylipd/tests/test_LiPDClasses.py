#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 12:18:41 2025

@author: deborahkhider

Tests for the LiPD classes. 

Naming rules:
1. class: Test{filename}{Class}{method} with appropriate camel case
2. function: test_{method}_t{test_id}
Notes on how to test:
0. Make sure [pytest](https://docs.pytest.org) has been installed: `pip install pytest`
1. execute `pytest {directory_path}` in terminal to perform all tests in all testing files inside the specified directory
2. execute `pytest {file_path}` in terminal to perform all tests in the specified file
3. execute `pytest {file_path}::{TestClass}::{test_method}` in terminal to perform a specific test class/method inside the specified file
4. after `pip install pytest-xdist`, one may execute "pytest -n 4" to test in parallel with number of workers specified by `-n`
"""

import pytest
from pylipd.classes.dataset import Dataset
from pylipd.lipd import LiPD
import pandas as pd
import numpy as np

from pylipd.classes.archivetype import ArchiveTypeConstants
from pylipd.classes.funding import Funding
from pylipd.classes.interpretation import Interpretation
from pylipd.classes.interpretationvariable import InterpretationVariableConstants
from pylipd.classes.location import Location
from pylipd.classes.paleodata import PaleoData
from pylipd.classes.datatable import DataTable
from pylipd.classes.paleounit import PaleoUnitConstants
from pylipd.classes.paleovariable import PaleoVariableConstants
from pylipd.classes.person import Person
from pylipd.classes.publication import Publication
from pylipd.classes.resolution import Resolution
from pylipd.classes.variable import Variable

import json

import re

import uuid

def generate_unique_id(prefix='PYD'):
    # Generate a random UUID
    random_uuid = uuid.uuid4()  # Generates a random UUID.
    
    # Convert UUID format to the specific format we need
    # UUID is usually in the form '1e2a2846-2048-480b-9ec6-674daef472bd' so we slice and insert accordingly
    id_str = str(random_uuid)
    formatted_id = f"{prefix}-{id_str[:5]}-{id_str[9:13]}-{id_str[14:18]}-{id_str[19:23]}-{id_str[24:28]}"
    
    return formatted_id


class TestGet():
    """
    This class test the get information function. Let's use the ODP846 dataset as it contains ensemble tables
    """

    def test_get_dataset(self, odp846):
        D = odp846
        D.get_datasets()
    
    def test_get_name(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        name = ds.getName()
        assert name == 'ODP846.Lawrence.2006'
    
    def test_get_funding(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        funding = ds.getFundings()
        assert len(funding) == 0
    
    def test_get_publication(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        pub = ds.getPublications()
        assert len(pub) == 6
    
    def test_get_pub_info(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        pub = ds.getPublications()
        pub1 = pub[0]
        
        pub1.getTitle()
        authors = pub1.getAuthors()
        authors[0].getName()
        pub1.getJournal()
        pub1.getDOI()
        pub1.getPages()
        pub1.getIssue()
        pub1.getVolume()
        pub1.getYear()
    
    def test_get_location(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        geo = ds.getLocation()
        lat = geo.getLatitude()
        lon = geo.getLongitude()
        elev = geo.getElevation()
        coor = geo.getCoordinates()
        assert lat == -3.1
        assert lon == -90.8
        assert elev == -3296.0
        assert coor == '-3.1,-90.8'
    
    def test_get_paleodata(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        paleodata = ds.getPaleoData()
        assert len(paleodata) == 1
    
    def test_get_chrondata(self,odp846):
        D = odp846
        ds = D.get_datasets()[0]
        chrondata = ds.getChronData()
        assert len(chrondata) == 1
    
    def test_get_datatable(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        paleodata = ds.getPaleoData()
        data_tables = []
        for item in paleodata:
            for table in item.getMeasurementTables(): #get the measurement tables
                df = table.getDataFrame(use_standard_names=True) # grab the data and standardize the variable names
                data_tables.append(df)
        assert len(data_tables) == 2
    
    def test_get_model(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        chrondata = ds.getChronData()
        df_ens = [] # create an empty list to store all ensemble tables across models. 
        for item in chrondata:
            for model in item.getModeledBy():
                for etable in model.getEnsembleTables():
                    df_ens.append(etable.getDataFrame())
        assert len(df_ens) == 1
    
    def test_get_table(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        paleodata = ds.getPaleoData()
        table = paleodata[0].getMeasurementTables()[0]
        
        table.getFileName()
        table.getMissingValue()
              
        var = table.getVariables()
        assert len(var) == 9
        
    def test_get_variable(self, odp846):
        D = odp846
        ds = D.get_datasets()[0]
        paleodata = ds.getPaleoData()
        table = paleodata[0].getMeasurementTables()[0]
        var = table.getVariables()
        var1 = var[0]
        
        var1.getColumnNumber()
        var1.getDescription()
        var1.getFoundInDataset()
        var1.getFoundInTable()
        var1.getInterpretations()
        var1.getMaxValue()
        var1.getMeanValue()
        var1.getMedianValue()
        var1.getMinValue()
        var1.getMissingValue()
        var1.getName()
        var1.getNotes()
        var1.getPartOfCompilations()
        var1.getProxy()
        var1.getProxyGeneral()
        var1.getResolution()
        var1.getStandardVariable()
        var1.getUnits()
        var1.getValues()
        var1.getVariableId()

class TestCreate():
    """
    Test the functionalities to create/edit a LiPD file
    """
    
    def test_create_ds(self):
        
        dataset1 = Dataset()

        # Set the name of the dataset
        dataset1.setName("TestDataset.2024")
        dataset1.id = dataset1.ns + "/" + dataset1.getName() # ** IMPORTANT **
        
        # Set collection name
        dataset1.setCollectionName("TestCollection")
        
        # Set the Archive Type (from a list of constants)
        dataset1.setArchiveType(ArchiveTypeConstants.MarineSediment)
        
        # Add a publication
        pub1 = Publication()
        pub1.setTitle("Sample Publication Title")
        person1 = Person(); person1.setName("Deborah Khider")
        person2 = Person(); person2.setName("Varun Ratnakar")
        pub1.setAuthors([person1, person2])
        # Add the publication to the dataset
        dataset1.addPublication(pub1)
        
        # Add funding information
        funding1 = Funding()
        funding1.addGrant("NSF Grant 23423A")
        funding1.addInvestigator(person1)
        # Add funding to the dataset
        dataset1.addFunding(funding1)
        
        # Add location information
        loc1 = Location()
        loc1.setLatitude("24.21232")
        loc1.setLongitude("48.32323")
        loc1.setElevation("342")
        loc1.setCountry("USA")
        # Set location for the dataset
        dataset1.setLocation(loc1)
        
        # Create Paleodata table
        table1 = DataTable()
        table1.setFileName("paleo0measurement1.csv")
        table1.setMissingValue("NaN")
        
        # Populate the table with variable data
        #
        # Option 1: Via a Dataframe with attributes:
        # ------------------------------------------
        # Create a random dataframe
        df = pd.DataFrame(np.random.randn(100, 2), columns=["site", "ukprime37"])
        # Set column attributes
        df.attrs = {
            "site": {
                'number': 1, 
                'variableName': 'site/hole', 
                'units': 'unitless', 
                'TSid': 'PYTJ3PSH0LT', 
                'variableType': 'measured', 
                'takenAtDepth': 'depth'
            },
            "ukprime37": {
                'number': 2,
                'interpretation': [
                    {
                        'rank': 1.0, 
                        'scope': 'Climate', 
                        'variable': 'temperature', 
                        'variableDetail': 'sea surface', 
                        'direction': 'positive'
                    }
                ], 
                'variableName': 'ukprime37', 
                'resolution': {
                    'hasMaxValue': 10.856999999999971, 
                    'hasMeanValue': 2.3355875057418465, 
                    'hasMedianValue': 2.211999999999989, 
                    'hasMinValue': 0.06999999999993634
                }, 
                'TSid': 'PYTM9N6HCQM', 
                'variableType': 'measured', 
                'takenAtDepth': 'depth' 
            }
        }
        table1.setDataFrame(df)
        
        # Create Another Paleodata table by setting variables with OOP calls
        table2 = DataTable()
        table2.setFileName("paleo0measurement2.csv")
        table2.setMissingValue("NaN")
        #
        # Option 2: Via OOP Calls to create each variable
        # -----------------------------------------------
        # Add a variable
        var1 = Variable()
        var1.setName("site")
        var1.setColumnNumber(1)
        var1.setVariableId("PYTJ3PSH0LT")
        var1.setVariableType("measured")
        var1.set_non_standard_property("takenAtDepth", "depth")
        # Set random values for this variable
        var1.setValues(json.dumps(np.random.randn(100).tolist()))
        
        # Add another variable
        var2 = Variable()
        var2.setName("ukprime37")
        var2.setColumnNumber(2)
        var2.setVariableId('PYTM9N6HCQM')
        var2.setVariableType('measured')
        var2.setStandardVariable(PaleoVariableConstants.Uk37)
        var2.setUnits(PaleoUnitConstants.cm3)
        
        # Add the variable interpretation
        interp1 = Interpretation()
        interp1.setRank("1")
        interp1.setScope("Climate")
        interp1.setVariable(InterpretationVariableConstants.temperature)
        interp1.setVariableDetail("sea surface")
        interp1.setDirection("positive")
        var2.addInterpretation(interp1)
        # Add the variable resolution
        resolution1 = Resolution()
        resolution1.setMaxValue(10.856999999999971)
        resolution1.setMeanValue(2.3355875057418465)
        resolution1.setMedianValue(2.211999999999989)
        resolution1.setMinValue(0.06999999999993634)
        var2.setResolution(resolution1)
        
        # Set random values for this variable
        var2.setValues(json.dumps(np.random.randn(100).tolist()))
        
        table2.setVariables([var1, var2])
        
        # Create Paleodata, and add the created tables to it
        paleodata1 = PaleoData()
        paleodata1.setMeasurementTables([table1, table2])
        
        dataset1.addPaleoData(paleodata1)
        
        
        