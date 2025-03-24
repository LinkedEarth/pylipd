#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:23:27 2023

@author: deborahkhider


Tests for pylipd.lipd

Naming rules:
1. class: Test{filename}{Class}{method} with appropriate camel case
2. function: test_{method}_t{test_id}
Notes on how to test:
0. Make sure [pytest](https://docs.pytest.org) has been installed: `pip install pytest`
1. execute `pytest {directory_path}` in terminal to perform all tests in all testing files inside the specified directory
2. execute `pytest {file_path}` in terminal to perform all tests in the specified file
3. execute `pytest {file_path}::{TestClass}::{test_method}` in terminal to perform a specific test class/method inside the specified file
4. after `pip install pytest-xdist`, one may execute "pytest -n 4" to test in parallel with number of workers specified by `-n`
5. for more details, see https://docs.pytest.org/en/stable/usage.html
"""

import pytest
from pylipd.lipd import LiPD
import urllib as urllib



class TestLiPDLoad():
    
    def test_load_t0(self, odp846):
        '''
        Test for a single file

        '''
        lipd = odp846
    
    def test_load_t1(self,multipleLipds):
        '''
        Test for multiple files
        '''
        lipd, names = multipleLipds

    def test_load_t2(self):
        '''
        Test for remote files
        '''
        lipd_remote = LiPD()
        lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic")
        try:
            lipd_remote.load_remote_datasets(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
        except(urllib.error.HTTPError):
            pass
    
    def test_load_t3(self,pages2k):
        '''
        Test for directory
        '''
        lipd = pages2k

class Testgetall():
    
    def test_dataset_names_t0(self, multipleLipds):
        lipd, true_ids = multipleLipds
        ids = lipd.get_all_dataset_names()
        assert len(ids) == 2 and type(ids[0])==str

    def test_dataset_ids_t0(self, multipleLipds):
        lipd, true_ids = multipleLipds
        ids = lipd.get_all_dataset_ids()
        
    def test_archiveTypes_t0(self,pages2k):
        lipd = pages2k
        archive = lipd.get_all_archiveTypes()
    
    def test_variables_t0(self,odp846):
        lipd = odp846
        df = lipd.get_all_variables()
    
    def test_compilation_t0(self, temp12k):
        lipd = temp12k
        comps = lipd.get_all_compilation_names()
        

class TestManipulation():
    
    def test_remove_t0(self,pages2k):
               
        D=pages2k
        names = D.get_all_dataset_names()
        names_compare = names[1:]
        D_test = D.copy()
        D_test.remove(names[0])
        assert D_test.get_all_dataset_names() == names_compare

    def test_pop_t0(self,pages2k):
        
        D=pages2k
        names = D.get_all_dataset_names()
        D_test = D.copy()
        D_popped = D_test.pop(names[0])
        assert D_test.get_all_dataset_names() == names[1:]
        assert D_popped.get_all_dataset_names()[0] == names[0]

class TestFilter():
    
    def test_geo_t0(self,pages2k):
        D=pages2k
        Lfiltered = D.filter_by_geo_bbox(0,25,50,50)
        assert len(Lfiltered.get_all_dataset_names()) == 5
    
    def test_archive_t0(self,pages2k):
        D=pages2k
        Lfiltered = D.filter_by_archive_type('marine sediment')
        assert len(Lfiltered.get_all_archiveTypes())==1
        assert Lfiltered.get_all_archiveTypes()[0] == 'Marine sediment'
    
    def test_archive_t1(self,pages2k):
        D=pages2k
        Lfiltered = D.filter_by_archive_type('marine|coral')
        assert len(Lfiltered.get_all_archiveTypes())==2
        assert 'Marine sediment' in Lfiltered.get_all_archiveTypes()
        assert 'Coral' in Lfiltered.get_all_archiveTypes()
    
    def test_dataset_t0(self, pages2k):
        D=pages2k
        Lfiltered = D.filter_by_datasetName('Ocn-RedSea.Felis.2000')
        names = Lfiltered.get_all_dataset_names()
        assert len(names) == 1
        assert 'Ocn-RedSea.Felis.2000' in names
    
    def test_dataset_t1(self, pages2k):
        D=pages2k
        Lfiltered = D.filter_by_datasetName('Ocn-RedSea.Felis.2000|Ant-WAIS-Divide.Severinghaus.2012')
        names = Lfiltered.get_all_dataset_names()
        assert len(names) == 2
        assert 'Ocn-RedSea.Felis.2000' in names
        assert 'Ant-WAIS-Divide.Severinghaus.2012'
    
    
    @pytest.mark.parametrize(('timeBoundType', 'recordLength'),
                             [('any', None),
                              ('any', 500),
                              ('entire', None),
                              ('entire', 20),
                              ('entirely',None),
                              ('entirely', 100)
                                 ])
    def test_time_t0(self,timeBoundType,recordLength,pages2k):
        D=pages2k
        Lfiltered = D.filter_by_time(timeBound=[0,1800], timeBoundType=timeBoundType,recordLength=recordLength)

    def test_compilation_t0(self, temp12k):
        D=temp12k
        DFiltered = D.filter_by_compilationName('Temp12k')
        
        
        
class TestGet():
    @pytest.mark.parametrize('dataframe',['True', 'False'])
    def test_get_timeseries_t0(self, odp846, dataframe):
        D = odp846
        ts_list=D.get_timeseries(D.get_all_dataset_names(), to_dataframe = dataframe)
    
    def test_bibtex_t0(self, odp846):
                
        lipd = odp846
        bibs, df = lipd.get_bibtex(save=False)
        
    def test_get_t0(self, multipleLipds):
        D,names = multipleLipds
        all_datasets = D.get_all_dataset_names()
        ds = D.get(all_datasets[0])
        
    def test_lipd_t0(self,odp846):
        lipd = odp846
        lipd_json = lipd.get_lipd(lipd.get_all_dataset_names()[0])
          
    def test_ens_t0(self,odp846):

        D=odp846
               
        ens_df = D.get_ensemble_tables()
        assert len(ens_df.index) == 1
    
    @pytest.mark.parametrize('mode',['chron', 'paleo'])
    def test_get_timeseries_essentials_t0(self, odp846, mode):
        D = odp846
        df = D.get_timeseries_essentials(mode=mode)
    
    def test_get_timeseries_essentials_t1(self, odp846):
        D = odp846
        df = D.get_timeseries_essentials(dsnames=D.get_all_dataset_names())
    
    @pytest.mark.parametrize('ensname',['year','age'])
    def test_ens_t1(self,odp846, ensname):
        D=odp846
        ens_df = D.get_ensemble_tables(ensembleVarName=ensname)
        if ensname == 'year':
            assert len(ens_df.index) == 0
        else:
            assert len(ens_df.index) == 1
    
    def test_ens_t2(self, odp846):

        D=odp846
        names = D.get_all_dataset_names()
        ens_df = D.get_ensemble_tables(dsname=names[0])
        assert len(ens_df.index) == 1
    
    def test_var_name_t0(self,pages2k):
        
        D=pages2k
        D.get_all_variable_names()
    
    def test_get_dataset_properties_t0(self,pages2k):
        D=pages2k
        D.get_dataset_properties()
    
    def test_get_variable_properties_t0(self,pages2k):
        D=pages2k
        D.get_variable_properties()
    
    def test_get_model_properties_t0(self,odp846):
        D=odp846
        D.get_model_properties()
    
    def test_get_locations_t0(self,pages2k):
        D=pages2k
        D.get_all_locations()
                
class TestTransform():

    def test_lipd_series(self, odp846):
        D=odp846
        S = D.to_lipd_series()

class TestRdf():
    
    def test_convert_to_rdf_t0(self):
        lipd = LiPD()
        try:
            lipd.convert_lipd_dir_to_rdf("../data/Pages2k", "all-lipd.nq")
        except:
            lipd.convert_lipd_dir_to_rdf("./examples/data/Pages2k", "all-lipd.nq")

        
                