#!/usr/bin/python3

# system-wide requirements
from sepy.SEPAClient import *
from uuid import uuid4
import threading
import requests
import logging
import json

# debug requirements
import traceback
import pdb

# local requirements
from .QueryUtils import *

class TrackProcessor:

    def __init__(self, conf, stats):

        # save the parameters
        self.stats = stats
        self.conf = conf        

        # create a KP
        self.kp = SEPAClient()


    def search(self, path, pattern, cacheEntry):
        
        # debug print
        logging.debug("New track search request")

        # update stats
        if not path in self.stats.requests["paths"]:
            self.stats.requests["paths"][path] = {"total":0, "failed":0, "successful":0}
        self.stats.requests["total"] += 1
        self.stats.requests["paths"][path]["total"] += 1

        # initialize
        if not cacheEntry:

            # generate an UUID for the request
            req_id = str(uuid4())
            graphURI = "http://ns#%s" % req_id
            
            # init a thread list
            threads = []
        
            # define the worker function
            def worker(conf, sg_query, cp):

                # do the request to SPARQL-Generate
                try:
                    data = {"query":sg_query}
                    sg_req = requests.post(self.conf.tools["sparqlgen"], data=data)
                except Exception as e:
                    logging.error("Exception during request to SPARQL-Generate server")
                    self.stats.requests["failed"] += 1
                    self.stats.requests["paths"][path]["failed"] += 1
                    print(traceback.print_exc())
                    return
                
                # from the turtle output create a SPARQL INSERT DATA
                triples = QueryUtils.getTriplesFromTurtle(sg_req.text)
                update = QueryUtils.getInsertDataFromTriples(triples, graphURI)

                # put data in SEPA
                try:
                    self.kp.update(self.conf.tools["sepa"]["update"], update)
                except:
                    logging.error("Error while connecting to SEPA")
                    logging.debug("Process %s completed!" % cp)            
                    
            # read the mappings
            results = {}
            for cp in self.conf.mappings["tracks"]["search"]:
                logging.debug("Searching for %s on %s" % (pattern, cp))
                    
                # build the SPARQL-generate query
                sg_query = self.conf.mappings["tracks"]["search"][cp].replace("$pattern", pattern)

                # for every mapping spawn a thread
                t = threading.Thread(target=worker, args=(self.conf, sg_query, cp))
                threads.append(t)
                t.start()

            # wait for results
            for t in threads:
                t.join()
            logging.debug("Ready to query SEPA")
            
        else:
            graphURI = "http://ns#%s" % cacheEntry
        
        # assembly results
        query = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX dc: <http://purl.org/dc/elements/1.1/> 
        PREFIX ac: <http://audiocommons.org/ns/audiocommons#> 
        SELECT ?audioClip ?title
        WHERE { GRAPH <%s> { ?audioClip rdf:type ac:AudioClip .
        ?audioClip dc:title ?title }}""" % graphURI
        try:
            status, results = self.kp.query(self.conf.tools["sepa"]["query"], query)
        except:
            msg = "Error while connecting to SEPA"
            logging.error(msg)
            self.stats.requests["failed"] += 1
            self.stats.requests["paths"][path]["failed"] += 1
            self.write(json.dumps({"status":"failure", "cause":msg}))
            return

        # return
        self.stats.requests["successful"] += 1
        self.stats.requests["paths"][path]["successful"] += 1
        if cacheEntry:
            return json.dumps({"status":"ok", "results":results}), cacheEntry
        else:
            return json.dumps({"status":"ok", "results":results}), req_id

        
    def show(self, path, trackId, source, cacheEntry):

        # update stats
        if not path in self.stats.requests["paths"]:
            self.stats.requests["paths"][path] = {"total":0, "failed":0, "successful":0}
        self.stats.requests["total"] += 1
        self.stats.requests["paths"][path]["total"] += 1

        # verify if cache exists
        if not cacheEntry:

            # generate an UUID for the request
            req_id = str(uuid4())
            graphURI = "http://ns#%s" % req_id
            
            # verify if source is one of the supported CPs
            if source in self.conf.mappings["tracks"]["show"]:
    
                # get the query
                sg_query = self.conf.mappings["tracks"]["show"][source].replace("$trackId", trackId)
            
                # do the request to SPARQL-Generate
                try:
                    data = {"query":sg_query}
                    sg_req = requests.post(self.conf.tools["sparqlgen"], data=data)
                except Exception as e:
                    logging.error("Exception during request to SPARQL-Generate server")
                    self.stats.requests["failed"] += 1
                    self.stats.requests["paths"][path]["failed"] += 1
                    print(traceback.print_exc())
                    return
                
                # from the turtle output create a SPARQL INSERT DATA
                triples = QueryUtils.getTriplesFromTurtle(sg_req.text)
                update = QueryUtils.getInsertDataFromTriples(triples, graphURI)
    
                # put data in SEPA
                try:
                    self.kp.update(self.conf.tools["sepa"]["update"], update)
                except:
                    logging.error("Error while connecting to SEPA")
                    logging.debug("Process %s completed!" % source)            

        else:
            graphURI = "http://ns#%s" % cacheEntry
                    
        # assembly results
        query = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX dc: <http://purl.org/dc/elements/1.1/> 
        PREFIX ac: <http://audiocommons.org/ns/audiocommons#> 
        SELECT ?audioClip ?title
        WHERE { GRAPH <%s> { ?audioClip rdf:type ac:AudioClip .
        ?audioClip dc:title ?title }}""" % graphURI
        try:
            status, results = self.kp.query(self.conf.tools["sepa"]["query"], query)
        except:
            msg = "Error while connecting to SEPA"
            logging.error(msg)
            self.stats.requests["failed"] += 1
            self.stats.requests["paths"][path]["failed"] += 1
            self.write(json.dumps({"status":"failure", "cause":msg}))
            return

        # return
        self.stats.requests["successful"] += 1
        self.stats.requests["paths"][path]["successful"] += 1
        if cacheEntry:
            return json.dumps({"status":"ok", "results":results}), cacheEntry
        else:
            return json.dumps({"status":"ok", "results":results}), req_id

        
    def analyse(self):
       
        # debug print
        logging.debug("New track analysis request")

        # update stats
        self.stats.requests["total"] += 1        
        
        # generate an UUID for the request
        req_id = str(uuid4())

        # read parameters
        in_id = self.request.arguments["id"]
        in_provider = self.request.arguments["provider"]
        in_transform = self.request.arguments["transform"]

        # invoke johan's service
        self.stats.requests["failure"] += 1
        logging.error("Not implemented")
        
