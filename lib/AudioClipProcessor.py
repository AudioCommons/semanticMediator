#!/usr/bin/python3

# system-wide requirements
from sepy.SEPAClient import *
from uuid import uuid4
import threading
import requests
import logging
import json
import datetime
import rdflib
from .GraphStoreClient import GraphStoreClient

# debug requirements
import traceback
import pdb

# local requirements
from .QueryUtils import *

class AudioClipProcessor:

    def __init__(self, conf, stats):
        # save the parameters
        self.stats = stats
        self.conf = conf # configuration

        self.gs = None # Graphstore

        # create a KP
        self.kp = SEPAClient()

        if self.conf.tools['graphstore'] is not None:
            self.gs = GraphStoreClient(self.conf.tools['graphstore'])

    def search(self, path, pattern, cacheEntry, sources):
        """
        Performs search for audioclips
        :param path: 
        :param pattern: what we are searching against
        :param cacheEntry: a string reference to a cache entry stored in a graphstore (it forms: `graphURI = "http://ns#%s" % cacheEntry`)
        :param sources: sources we should search against, can be None (=all)
        :return: value of ac_field_name for the given result
        """

        # debug print
        logging.debug("New audioclip search request")

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

                logging.debug("Sending query to SPARQL Generate")
                logging.debug(sg_query)

                # do the request to SPARQL-Generate
                try:
                    data = {"query":sg_query}
                    st = time.time()
                    sg_req = requests.post(self.conf.tools["sparqlgen"], data=data)
                    et = time.time()
                    print(et - st)
                except Exception as e:
                    logging.error("Exception during request to SPARQL-Generate server")
                    self.stats.requests["failed"] += 1
                    self.stats.requests["paths"][path]["failed"] += 1
                    print(traceback.print_exc())
                    return

                logging.debug("Result from SPARQL Generate")
                logging.debug(sg_req.text)

                if self.gs is not None:
                    try:
                        logging.debug("Posting data to graphstore for req_id: %s" % (req_id))
                        self.gs.insertRDF(sg_req.text, graphURI)
                    except Exception as e:
                        msg = "Error while posting RDF data on graphstore"
                        logging.error(msg)
                        print(traceback.print_exc())
                        logging.debug("Process %s completed!" % cp)
                else:
                    # from the turtle output create a SPARQL INSERT DATA
                    logging.debug("Creating INSERT DATA query")
                    triples = QueryUtils.getTriplesFromTurtle(sg_req.text)
                    update = QueryUtils.getInsertDataFromTriples(triples, graphURI)

                    # put data in SEPA
                    try:
                        logging.debug("Sending INSERT DATA query to SEPA")
                        self.kp.update(self.conf.tools["sepa"]["update"], update)
                    except:
                        logging.error("Error while connecting to SEPA")
                        logging.debug("Process %s completed!" % cp)

            # read the mappings
            results = {}
            for cp in self.conf.mappings["audioclips"]["search"]:

                if (sources and cp in sources) or (not sources):

                    logging.debug("Searching for %s on %s" % (pattern, cp))

                    datetimeNow = "\"" + datetime.datetime.now().isoformat() + "\"" + "^^<http://www.w3.org/2001/XMLSchema#dateTime>"

                    # build the SPARQL-generate query
                    sg_query = self.conf.mappings["audioclips"]["search"][cp].replace("$pattern", pattern).replace("$startTime", datetimeNow)

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

        if self.gs is not None:
            try:
                resultsTurtle = self.gs.getGraph(graphURI)
                g = rdflib.Graph()
                g.parse(data=resultsTurtle, format="n3")
                resultsJsonLd = g.serialize(format="json-ld")
                logging.debug(resultsJsonLd)
                frame = json.loads(self.conf.resources["jsonld-frames"]["audioclips"]["search"])
                context = json.loads(self.conf.resources["jsonld-context"])
                jres = QueryUtils.frameAndCompact(json.loads(resultsJsonLd), frame, context)
            except Exception as e:
                msg = "Error while getting RDF data as JSON-LD: " + e.text
                logging.error(msg)
                self.stats.requests["failed"] += 1
                self.stats.requests["paths"][path]["failed"] += 1
                print(traceback.print_exc())
                return json.dumps({"status": "failure", "cause": msg}), -1

        else:
            # assembly results
            query = None
            # if not sources:
            query = """PREFIX prov: <http://www.w3.org/ns/prov#>
                CONSTRUCT { ?s ?p ?o } WHERE { GRAPH <%s> { ?s ?p ?o } }""" % graphURI
            # else:
            #     filters = []
            #     for s in sources:
            #         filters.append(" ?pp = <%s> " % self.conf.cps[s])
            #     query = """PREFIX prov: <http://www.w3.org/ns/prov#>
            #     CONSTRUCT { ?s ?p ?o } WHERE { GRAPH <%s> { ?s ?p ?o . ?s prov:wasAttributedTo ?pp . FILTER( %s ) } }"""  % (graphURI, " || ".join(filters))
            #     print(query)

            try:
                status, results = self.kp.query(self.conf.tools["sepa"]["query"], query)
                frame = json.loads(self.conf.resources["jsonld-frames"]["audioclips"]["search"])
                context = json.loads(self.conf.resources["jsonld-context"])
                jres = QueryUtils.getJsonLD(results, frame, context)
            except:
                msg = "Error while connecting to SEPA"
                logging.error(msg)
                self.stats.requests["failed"] += 1
                self.stats.requests["paths"][path]["failed"] += 1
                return json.dumps({"status": "failure", "cause": msg}), -1

        # return
        self.stats.requests["successful"] += 1
        self.stats.requests["paths"][path]["successful"] += 1

        if cacheEntry:
            return json.dumps({"status": "ok", "results": jres}), cacheEntry
        else:
            return json.dumps({"status": "ok", "results": jres}), req_id


    def show(self, path, audioclipId, source, cacheEntry):

        # debug print
        logging.debug("New audioclip show request")

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
            if source in self.conf.mappings["audioclips"]["show"]:

                logging.debug("Showing audioclip %s from %s" % (audioclipId, source))

                # get the query
                sg_query = self.conf.mappings["audioclips"]["show"][source].replace("$trackId", audioclipId)

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

        logging.debug("Ready to query SEPA")

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
            msg = "Error while getting RDF data as JSON-LD: " + exception.text
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


    def analyse(self, path, audioclipId, cp, descriptor, cacheEntry):

        # update stats
        if not path in self.stats.requests["paths"]:
            self.stats.requests["paths"][path] = {"total":0, "failed":0, "successful":0}
        self.stats.requests["total"] += 1
        self.stats.requests["paths"][path]["total"] += 1

        # verify if cache exists
        # if not cacheEntry:

        # generate an UUID for the request
        req_id = str(uuid4())
        headers = {"Content-Type":"application/json"}
        graphURI = "http://ns#%s" % req_id

        # invoke the tool
        fullURI = self.conf.tools["ac-analysis"]["baseURI"] + "?provider=%s&id=%s&descriptor=%s" % (cp, audioclipId, descriptor)
        print(fullURI)
        req = requests.get(fullURI, headers=headers)

        # else:
        #     graphURI = "http://ns#%s" % cacheEntry

        # TODO -- parse and "semanticize" results
        results = req.text
        logging.info(req.text)

        # return
        self.stats.requests["successful"] += 1
        self.stats.requests["paths"][path]["successful"] += 1
        if cacheEntry:
            return json.dumps({"status":"ok", "results":results}), cacheEntry
        else:
            return json.dumps({"status":"ok", "results":results}), req_id
