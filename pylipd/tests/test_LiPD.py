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

class TestLiPDLoad():
    
    def test_load_t0(self):
        url = 'https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd'
       
        lipd = LiPD()
        lipd.load(url)
    
    def test_load_t1(self):
        url = ['https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd',
               'https://lipdverse.org/data/LCd0404b13039620e9ec2b82dbdcf87861/1_0_1//LedovyiObryvExposureNorthernSection.Anderson.2002.lpd']
        
        lipd = LiPD()
        lipd.load(url)

    def test_load_t2(self):
        
            # Fetch LiPD data from remote RDF Graph
        lipd_remote = LiPD()
        lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
        lipd_remote.load_remote_datasets(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
            #print(lipd_remote.get_all_dataset_names())
    

class TestLiPDnames():
    
    def test_get_all_dataset_names_t0(self):
        url = ['https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd',
               'https://lipdverse.org/data/LCd0404b13039620e9ec2b82dbdcf87861/1_0_1//LedovyiObryvExposureNorthernSection.Anderson.2002.lpd']
        
        true_ids = ['Ocn-Philippines.Stott.2007','LedovyiObryvExposureNorthernSection.Anderson.2002']
        
        
        lipd = LiPD()
        lipd.load(url)
        ids = lipd.get_all_dataset_names()
        assert ids == true_ids

class TestLiPDids():
    def test_get_all_dataset_ids_t0(self):
        url = ['https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd',
               'https://lipdverse.org/data/LCd0404b13039620e9ec2b82dbdcf87861/1_0_1//LedovyiObryvExposureNorthernSection.Anderson.2002.lpd']
        
        true_ids = ['RRh3T4NCsf4MgrxhXbJq','LCd0404b13039620e9ec2b82dbdcf87861']
        
        
        lipd = LiPD()
        lipd.load(url)
        ids = lipd.get_all_dataset_ids()
        assert ids == true_ids

class TestLiPDTimeseries():
    
    @pytest.mark.parametrize('dataframe',['True', 'False'])
    def test_get_timeseries_t0(self, dataframe):
        url = 'https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd'
        
        lipd = LiPD()
        lipd.load(url)
        ts_list=lipd.get_timeseries(lipd.get_all_dataset_names(), to_dataframe = dataframe)
    
        
class TestLiPDquery():

    def test_query_t0(self):
        
        
        url = ['https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd',
               'https://lipdverse.org/data/LCd0404b13039620e9ec2b82dbdcf87861/1_0_1//LedovyiObryvExposureNorthernSection.Anderson.2002.lpd']
        
        query = """PREFIX le: <http://linked.earth/ontology#>
               select (count(distinct ?ds) as ?count) where {
                   ?ds a le:Dataset .
                   ?ds le:hasUrl ?url
               }"""
       
        
        
        lipd = LiPD()
        lipd.load(url)
        result, result_df = lipd.query(query)
             
class TestLiPDbibtex():

    def test_bibtex_t0(self):
        
        
        url = ['https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd',
               'https://lipdverse.org/data/LCd0404b13039620e9ec2b82dbdcf87861/1_0_1//LedovyiObryvExposureNorthernSection.Anderson.2002.lpd']
        
        
        lipd = LiPD()
        lipd.load(url)
        bibs = lipd.get_bibtex(save=False)
      
class TestLiPDremove():
    
    def test_remove_t0(self):
        
        url = ['https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd',
               'https://lipdverse.org/data/LCd0404b13039620e9ec2b82dbdcf87861/1_0_1//LedovyiObryvExposureNorthernSection.Anderson.2002.lpd',
               'https://lipdverse.org/data/ch2kTA18TAS01/1_0_2//TA18TAS01.lpd']
        
        D=LiPD()
        D.load(url)
        names = D.get_all_dataset_names()
        names_compare = names[1:]
        D_test = D.copy()
        D_test.remove(names[0])
        assert D_test.get_all_dataset_names() == names_compare

class TestLiPDpop():
    
    def test_pop_t0(self):
        
        url = ['https://lipdverse.org/data/RRh3T4NCsf4MgrxhXbJq/1_0_0//Ocn-Philippines.Stott.2007.lpd',
               'https://lipdverse.org/data/LCd0404b13039620e9ec2b82dbdcf87861/1_0_1//LedovyiObryvExposureNorthernSection.Anderson.2002.lpd',
               'https://lipdverse.org/data/ch2kTA18TAS01/1_0_2//TA18TAS01.lpd']
        
        D=LiPD()
        D.load(url)
        names = D.get_all_dataset_names()
        D_test = D.copy()
        D_popped = D_test.pop(names[0])
        assert D_test.get_all_dataset_names() == names[1:]
        assert D_popped.get_all_dataset_names()[0] == names[0]
    
class TestLiPDensemble():

    def test_ens_t0(self):

        path = './examples/data/ODP846.Lawrence.2006.lpd'
        D=LiPD()
        D.load(path)
        
        ens_df = D.get_ensemble_tables()
        assert len(ens_df.index) == 1
    
    @pytest.mark.parametrize('ensname',['year','age'])
    def test_ens_t1(self,ensname):
        path = './examples/data/ODP846.Lawrence.2006.lpd'
        D=LiPD()
        D.load(path)
        
        ens_df = D.get_ensemble_tables(ensembleVarName=ensname)
        if ensname == 'year':
            assert len(ens_df.index) == 0
        else:
            assert len(ens_df.index) == 1
    
    def test_ens_t2(self):

        path = './examples/data/ODP846.Lawrence.2006.lpd'
        D=LiPD()
        D.load(path)
        
        names = D.get_all_dataset_names()
        
        ens_df = D.get_ensemble_tables(dsname=names[0])
        assert len(ens_df.index) == 1
        
                
        