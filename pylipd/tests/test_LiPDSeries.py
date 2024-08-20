#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 22:34:58 2023

@author: deborahkhider

Tests for pylipd.LiPDSeries

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
from pylipd.lipd_series import LiPDSeries

class TestLoad():
    
    def test_load_t0(self,odp846):
        D =odp846
        lipd_series = D.to_lipd_series()
        
class TestGetAll():
    
    def test_variables_t0(self,odp846):
        D =odp846
        S = D.to_lipd_series()
        df = S.get_all_variables()
    
    def test_variable_names_t0(self,pages2k):
        D=pages2k
        S = D.to_lipd_series()
        names = S.get_all_variable_names()
    
    def test_timeseries_essentials_t0(self, pages2k):
        D=pages2k
        S = D.to_lipd_series()
        names = S.get_timeseries_essentials()
    
    def test_proxy_t0(self, pages2k):
        D=pages2k
        S = D.to_lipd_series()
        names = S.get_all_proxy()
    
    def test_variable_t0(self,pages2k):
        D=pages2k
        S = D.to_lipd_series()
        l = S.get_variable_properties()
        
class TestFiler():
    
    def test_name_t0(self,pages2k):
        D=pages2k
        S = D.to_lipd_series()
        Sfiltered = S.filter_by_name('temperature')
        df=Sfiltered.get_timeseries_essentials()
        assert len(df.index)==11
    
    def test_proxy_t0(self,pages2k):
        D=pages2k
        S = D.to_lipd_series()
        Sfiltered = S.filter_by_proxy('ring width')
        v = Sfiltered.get_all_proxy()
        assert len(v)==1
    
    @pytest.mark.parametrize('stats',['Mean','Median','Min','Max'])
    def test_resolution_t0(self,stats,pages2k):
        D=pages2k
        S = D.to_lipd_series()
        Sfiltered = S.filter_by_resolution(threshold = 10,stats=stats)
        

        