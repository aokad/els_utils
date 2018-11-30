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
    
    # kibana
    def test_kibana_01_version(self):
        subprocess.check_call(['python3', 'elsu-kibana', '--version'])

    def test_kibana_02_get_01(self):
        options = ["all"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_02_get_02(self):
        options = ["all"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
        
    def test_kibana_02_get_03(self):
        options = ["dashboard"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_02_get_04(self):
        options = ["dashboard", "--title", "lassie01"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_02_get_05(self):
        options = ["dashboard", "--id", "lassie01-hmp-2012-dashboard"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_02_get_06(self):
        options = ["visualization"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
        
    def test_kibana_02_get_07(self):
        options = ["visualization", "--title", "bamsort-20181107-visualization-title"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_02_get_08(self):
        options = ["visualization", "--id", "bamsort-20181107-visualization-title"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_02_get_09(self):
        options = ["index-pattern"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)
        
    def test_kibana_02_get_10(self):
        options = ["index-pattern", "--title", "c-cat-mutation-20181107-*-metrics-cpu"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    def test_kibana_02_get_11(self):
        options = ["index-pattern", "--id", "c-cat-mutation-20181107-*-metrics-cpu"]
        subprocess.check_call(['python3', 'elsu-kibana', 'get'] + options)

    # ES
    def test_es_01_version(self):
        subprocess.check_call(['python3', 'elsu-es', '--version'])

    def test_es_02_get_01(self):
        options = ["db"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)

    def test_es_02_get_02(self):
        options = ["db", "--detail"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)

    def test_es_02_get_03(self):
        options = ["table", "--name", "loman-20181121"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)
        
    def test_es_02_get_04(self):
        options = ["record", "--name", "loman-20181121"]
        subprocess.check_call(['python3', 'elsu-es', 'get'] + options)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSet))
    return suite

