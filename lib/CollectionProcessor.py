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

class CollectionProcessor:

    def __init__(self, conf, stats):

        # save the parameters
        self.stats = stats
        self.conf = conf        

        # create a KP
        self.kp = SEPAClient()

        
    def search(self, path, pattern, cacheEntry, sources):

        # debug print
        logging.debug("New collection search request")

        # initialize
        if cacheEntry:
            graphURI = "http://ns#%s" % cacheEntry
        else:
            graphURI = None
        
        if not cacheEntry:
        
            # generate an UUID for the request
            req_id = str(uuid4())
            graphURI = "http://ns#%s" % req_id
    
            # update stats
            if not path in self.stats.requests["paths"]:
                self.stats.requests["paths"][path] = {"total":0, "failed":0, "successful":0}
            self.stats.requests["total"] += 1
            self.stats.requests["paths"][path]["total"] += 1
            
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
            for cp in self.conf.mappings["collections"]["search"]:

                if (sources and cp in sources) or (not sources):
                
                    logging.debug("Searching for %s on %s" % (pattern, cp))
        
                    # build the SPARQL-generate query
                    sg_query = self.conf.mappings["collections"]["search"][cp].replace("$pattern", pattern)
        
                    # for every mapping spawn a thread
                    t = threading.Thread(target=worker, args=(self.conf, sg_query, cp))
                    threads.append(t)
                    t.start()
        
            # wait for results
            for t in threads:
                t.join()
            logging.debug("Ready to query SEPA")
            
        # assembly results
        query = None
        if not sources:
            query = """PREFIX prov: <http://www.w3.org/ns/prov#>
            CONSTRUCT { ?s ?p ?o } WHERE { GRAPH <%s> { ?s ?p ?o } }"""
        else:            
            filters = []            
            for s in sources:
                filters.append(" ?pp = <%s> " % self.conf.cps[s])
            query = """PREFIX prov: <http://www.w3.org/ns/prov#>
            CONSTRUCT { ?s ?p ?o } WHERE { GRAPH <%s> { ?s ?p ?o . ?s prov:wasAttributedTo ?pp . FILTER( %s ) } }"""  % (graphURI, " || ".join(filters))
            print(query)
        
        try:
            status, results = self.kp.query(self.conf.tools["sepa"]["query"], query % graphURI)
            jres = QueryUtils.getJsonLD(results)
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
            return json.dumps({"status":"ok", "results":json.loads(jres)}), cacheEntry
        else:
            return json.dumps({"status":"ok", "results":json.loads(jres)}), req_id
