# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:18:34 2016

@author: okada

"""


import unittest
import os
import glob
import subprocess

class TestSet(unittest.TestCase):

    WDIR = "/tmp/ecsub"
    
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
        
    def test1_01_version(self):
        subprocess.check_call(['python3', 'elsu', '--version'])

    def test2_01_submit(self):
        options = [
            "--type", "dashboard"
        ]
        subprocess.check_call(['python3', 'elsu', 'kibana', 'find'] + options)
        
    def test3_01_report(self):
        options = [
            "--type", "db"
        ]
        subprocess.check_call(['python', 'elsu', 'es', 'find'] + options)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSet))
    return suite

