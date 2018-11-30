# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:18:34 2016

@author: okada

"""


import unittest
import subprocess

class TestSet(unittest.TestCase):

    # init class
    @classmethod
    def setUpClass(cls):
        pass
        
    # terminated class
    @classmethod
    def tearDownClass(cls):
        pass

    # init method
    def setUp(self):
        pass

    # terminated method
    def tearDown(self):
        pass
    
    # ES
    def test_es_version(self):
        subprocess.check_call(['python3', 'elsu-es', '--version'])

    def test_es_post_01(self):
        cmd = ['python3', 'elsu-es', 'post'] 
        options = ["tests/testdata.json"]
        print(cmd + options)
        subprocess.check_call(cmd + options)

    def test_es_get_01(self):
        options = ["db"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)

    def test_es_get_02(self):
        options = ["db", "--detail"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)

    def test_es_get_03(self):
        options = ["table", "--name", "annual_precipitation"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)
        
    def test_es_get_04(self):
        options = ["record", "--name", "annual_precipitation"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)

    # kibana
    def test_kibana_post_01(self):
        options = ["index-pattern", "--index", "annual_precipitation"]
        subprocess.check_call(['python3', 'elsu-kibana', 'post'] + options)

    """
    def test_kibana_version(self):
        subprocess.check_call(['python3', 'elsu-kibana', '--version'])
    
    def test_kibana_get_01(self):
        options = ["all", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_get_02(self):
        options = ["all", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
        
    def test_kibana_get_03(self):
        options = ["dashboard", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_get_04(self):
        options = ["dashboard", "--title", "lassie01", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_get_05(self):
        options = ["dashboard", "--id", "lassie01-hmp-2012-dashboard", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_get_06(self):
        options = ["visualization", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
        
    def test_kibana_get_07(self):
        options = ["visualization", "--title", "bamsort-20181107-visualization-title", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_get_08(self):
        options = ["visualization", "--id", "bamsort-20181107-visualization-title", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
    """
    def test_kibana_get_09(self):
        options = ["index-pattern", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
        
    def test_kibana_get_10(self):
        options = ["index-pattern", "--title", "annual_precipitation", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_get_11(self):
        options = ["index-pattern", "--id", "annual_precipitation", "--max", "3"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
    
    # delete objects
    def test_kibana_delete_01(self):
        options = ["index-pattern", "--index", "annual_precipitation"]
        subprocess.check_call(['python3', 'elsu-kibana', 'delete'] + options)

    def test_es_delete_01(self):
        options = ["annual_precipitation"]
        subprocess.check_call(['python3', 'elsu-es', 'delete'] + options)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSet))
    return suite

