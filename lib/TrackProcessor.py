#!/usr/bin/python3

# system-wide requirements
from sepy.SEPAClient import *
from tornado import web
from uuid import uuid4
import threading
import requests
import logging
import json
import pdb

# local requirements
from .QueryUtils import *


class TrackProcessor(web.RequestHandler):

    def initialize(self, conf, stats):

        # save the parameters
        self.stats = stats
        self.conf = conf        

        # create a KP
        self.kp = SEPAClient()

        
    def get(self):

        # determine the requested action
        action = self.request.path.split("/")[-1]

        # invoke the proper handler
        if action == "search":
            self.search()
        if action == "analyse":
            self.analyse()
            
            
    def search(self):

        # debug print
        logging.debug("New track search request")
        
        # generate an UUID for the request
        req_id = str(uuid4())
        
        # read the search pattern
        # NOTE: the user may specify multiple patterns and this must be handled somehow
        if not "pattern" in self.request.arguments:
            msg = "You MUST specify a pattern if you want to search for something!"
            logging.error(msg)
            self.write(json.dumps({"status":"failure", "cause":msg}))            
            return            
        patternList = [t.decode("utf-8") for t in self.request.arguments["pattern"]]
        patternString = "+".join(patternList)
        
        # initialization
        threads = []

        # define the worker function
        def worker(conf, sg_query, cp):

            # do the request to SPARQL-Generate
            try:
                data = {"query":sg_query}
                sg_req = requests.post(self.conf.tools["sparqlgen"], data=data)
            except Exception as e:
                logging.error("Exception during request to SPARQL-Generate server")
                print(traceback.print_exc())
                return

            # from the turtle output create a SPARQL INSERT DATA
            triples = QueryUtils.getTriplesFromTurtle(sg_req.text)
            update = QueryUtils.getInsertDataFromTriples(triples)

            # put data in SEPA
            try:
                self.kp.update(self.conf.tools["sepa"]["update"], update)
            except:
                logging.error("Error while connecting to SEPA")
            logging.debug("Process %s completed!" % cp)
            
                    
        # read the mappings
        results = {}
        for cp in self.conf.mappings["tracks"]["search"]:
            logging.debug("Searching for %s on %s" % (patternString, cp))

            # build the SPARQL-generate query
            sg_query = self.conf.mappings["tracks"]["search"][cp].replace("$pattern", patternString)

            # for every mapping spawn a thread
            t = threading.Thread(target=worker, args=(self.conf, sg_query, cp))
            threads.append(t)
            t.start()

        # wait for results
        for t in threads:
            t.join()
        logging.debug("Ready to query SEPA")
        
        # assembly results
        query = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX dc: <http://purl.org/dc/elements/1.1/> 
        PREFIX ac: <http://audiocommons.org/ns/audiocommons#> 
        SELECT ?audioClip ?title
        WHERE {?audioClip rdf:type ac:AudioClip .
        ?audioClip dc:title ?title }"""
        try:
            status, results = self.kp.query(self.conf.tools["sepa"]["query"], query)
        except:
            msg = "Error while connecting to SEPA"
            logging.error(msg)
            self.write(json.dumps({"status":"failure", "cause":msg}))
            return
        
        # return
        self.write(json.dumps({"status":"ok", "results":results}))


    def analyse(self):
       
        # debug print
        logging.debug("New track analysis request")
        
        # generate an UUID for the request
        req_id = str(uuid4())

        # read parameters
        in_id = self.request.arguments["id"]
        in_provider = self.request.arguments["provider"]
        in_transform = self.request.arguments["transform"]

        # invoke johan's service
        logging.error("Not implemented")
        
