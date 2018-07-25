#!/usr/bin/python3

# requirements
import unittest
import requests
import logging
import json
import yaml
import sys
import os

class MediatorTests(unittest.TestCase):

    config = None
    statsURI = None
    clearStatsURI = None
    
    @classmethod
    def setUpClass(self):

        # read config file
        try:        
            self.config = os.environ["MEDIATORTEST"]
        except KeyError:
            logging.error("You must specify a configuration file through the variable $MEDIATORTEST")
            sys.exit()            
        yf = open(self.config, "r")
        ym = yaml.load(yf)        
        self.mediatorBaseURI = ym["mediator"]["baseUri"]
        self.audioclipSearchPath = ym["mediator"]["routes"]["audioclipSearch"]["path"]
        self.audioclipSearchArgs = ym["mediator"]["routes"]["audioclipSearch"]["args"]
        self.audioclipShowPath = ym["mediator"]["routes"]["audioclipShow"]["path"]
        self.audioclipShowArgs = ym["mediator"]["routes"]["audioclipShow"]["args"]
        self.audioclipAnalysePath = ym["mediator"]["routes"]["audioclipAnalyse"]["path"]
        self.audioclipAnalyseArgs = ym["mediator"]["routes"]["audioclipAnalyse"]["args"]    
        self.collectionSearchPath = ym["mediator"]["routes"]["collectionSearch"]["path"]
        self.collectionSearchArgs = ym["mediator"]["routes"]["collectionSearch"]["args"]

        # close file
        yf.close()

        
    def test_00_successful_audioclip_search(self):

        # request configuration
        reqConf = {"pattern": "barking"}
        params = None

        # build URI
        for arg in self.audioclipSearchArgs:
            if not params:
                params = "?%s=%s" % (arg, reqConf[arg])
            else:
                params += "&%s=%s" % (arg, reqConf[arg])

        # make the request
        r = requests.get(self.mediatorBaseURI + self.audioclipSearchPath + params)
        msg = json.loads(r.text)
        
        # check that returns 200
        self.assertEqual(200, r.status_code)
        self.assertEqual("ok", msg["status"])

        
    def test_01_successful_audioclip_show(self):

        # request configuration
        reqConf = {"source": "freesound"}
        params = None

        # build URI
        for arg in self.audioclipShowArgs:
            if not params:
                params = "?%s=%s" % (arg, reqConf[arg])
            else:
                params += "&%s=%s" % (arg, reqConf[arg])

        # make the request
        uri = self.mediatorBaseURI + self.audioclipShowPath % "418106"
        r = requests.get(uri + params)
        msg = json.loads(r.text)
        
        # check that returns 200
        self.assertEqual(200, r.status_code)
        self.assertEqual("ok", msg["status"])


    def test_02_successful_collection_search(self):

        # request configuration
        reqConf = {"pattern": "barking"}
        params = None

        # build URI
        for arg in self.collectionSearchArgs:
            if not params:
                params = "?%s=%s" % (arg, reqConf[arg])
            else:
                params += "&%s=%s" % (arg, reqConf[arg])

        # make the request
        r = requests.get(self.mediatorBaseURI + self.collectionSearchPath + params)
        msg = json.loads(r.text)
        
        # check that returns 200
        self.assertEqual(200, r.status_code)
        self.assertEqual("ok", msg["status"])


    def test_03_successful_audioclip_analysis(self):

        # request configuration
        reqConf = {"source": "jamendo", "plugin": "chords"}
        params = None

        # build URI
        for arg in self.audioclipAnalyseArgs:
            if not params:
                params = "?%s=%s" % (arg, reqConf[arg])
            else:
                params += "&%s=%s" % (arg, reqConf[arg])

        # make the request
        mid = self.audioclipAnalysePath % "1498355"
        r = requests.get(self.mediatorBaseURI + mid + params)
        msg = json.loads(r.text)
        
        # check that returns 200
        self.assertEqual(200, r.status_code)
        self.assertEqual("ok", msg["status"])

        
                
if __name__ == "__main__":
    unittest.main(verbosity = 3)
