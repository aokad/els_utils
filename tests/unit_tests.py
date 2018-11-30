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
        subprocess.check_call(['python3 elsu-es --version'])

    def test_es_post_01(self):
        cmd = 'python3 elsu-es post tests/testdata.json'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_es_get_01(self):
        cmd = 'python3 elsu-es get db | head'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_es_get_02(self):
        cmd = 'python3 elsu-es get db --detail | head'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_es_get_03(self):
        cmd = 'python3 elsu-es get table --name annual_precipitation'
        print(cmd)
        subprocess.check_call(cmd, shell = True)
        
    def test_es_get_04(self):
        cmd = 'python3 elsu-es get record --name annual_precipitation'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    # kibana
    def test_kibana_version(self):
        cmd = 'python3 elsu-kibana --version'
        print(cmd)
        subprocess.check_call(cmd, shell = True)
        
    def test_kibana_post_01(self):
        cmd = 'python3 elsu-kibana post index-pattern --index annual_precipitation'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_kibana_get_01(self):
        cmd = 'python3 elsu-kibana get all --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_kibana_get_02(self):
        cmd = 'python3 elsu-kibana get all --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)
        
    def test_kibana_get_03(self):
        cmd = 'python3 elsu-kibana get dashboard --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_kibana_get_04(self):
        cmd = 'python3 elsu-kibana get dashboard --title lassie01'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_kibana_get_05(self):
        cmd = 'python3 elsu-kibana get dashboard --id lassie01-hmp-2012-dashboard --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_kibana_get_06(self):
        cmd = 'python3 elsu-kibana get visualization --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)
        
    def test_kibana_get_07(self):
        cmd = 'python3 elsu-kibana get visualization --title bamsort-20181107-visualization-title --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_kibana_get_08(self):
        cmd = 'python3 elsu-kibana get visualization --id bamsort-20181107-visualization-title --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)
    
    def test_kibana_get_09(self):
        cmd = 'python3 elsu-kibana get "index-pattern" --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)
        
    def test_kibana_get_10(self):
        cmd = 'python3 elsu-kibana get "index-pattern" --title annual_precipitation'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_kibana_get_11(self):
        cmd = 'python3 elsu-kibana get "index-pattern" --id annual_precipitation --max 3'
        print(cmd)
        subprocess.check_call(cmd, shell = True)
    
    # delete objects
    def test_kibana_delete_01(self):
        cmd = 'python3 elsu-kibana delete annual_precipitation'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

    def test_es_delete_01(self):
        cmd = 'python3 elsu-es delete annual_precipitation'
        print(cmd)
        subprocess.check_call(cmd, shell = True)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSet))
    return suite

