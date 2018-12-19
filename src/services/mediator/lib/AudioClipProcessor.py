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

VERSION = "2.4.1"
DEFAULT_RESULTS_LIMIT = 12

class AudioClipProcessor:

    def __init__(self, conf, stats):
        # save the parameters
        self.stats = stats
        self.conf = conf # configuration

        self.gs = None # Graphstore

        # create a KP
        self.kp = SEPAClient()

        if 'graphstore' in self.conf.tools:
            self.gs = GraphStoreClient(self.conf.tools['graphstore'])

        colaboFlowAuditConfig = self.conf.getExtensionConfig("space.colabo.flow.audit")
        if self.conf.isExtensionActive("space.colabo.flow.audit"):
            import uuid
            # from colabo.flow.audit import ColaboFlowAudit, audit_pb2
            from colabo.flow.audit import audit_pb2
            from colabo.flow.audit import ColaboFlowAudit
            self.audit_pb2 = audit_pb2
            self.colaboFlowAudit = ColaboFlowAudit()

        colaboFlowGoConfig = self.conf.getExtensionConfig("space.colabo.flow.go")
        if self.conf.isExtensionActive("space.colabo.flow.go"):
            import uuid
            from colabo.flow.go import go_pb2
            from colabo.flow.go import ColaboFlowGo

            gRpcUrl = colaboFlowGoConfig['host']+':'+str(colaboFlowGoConfig['port'])
            # https://docs.python.org/2/library/uuid.html
            # flowInstanceId = str(uuid.uuid1())
            self.go_pb2 = go_pb2
            self.colaboFlowGo = ColaboFlowGo(socketUrl=gRpcUrl)


    def error(params, msg):
        return {
            "@type": "schema:SearchAction",
            "query": params["pattern"] ,
            # "schema:startTime": startTime ,
            # "schema:endTime": endTime ,
            "actionStatus": "schema:FailedActionStatus" ,
            "error": msg,
            "object": {
                "@type": "doap:Version",
                "revision": VERSION,
                "releaseOf": "https://m2.audiocommons.org/"
            }
        }

    def search(self, path, params, cacheEntryUuid, sources):
        """
        Performs search for audioclips
        :param path:
        :param params: dictionary of query parameteres (pattern: what we are searching against)
        :param cacheEntryUuid: a string reference to a cache entry stored in a graphstore (it forms: `graphURI = "http://ns#%s" % cacheEntryUuid`)
        :param sources: sources we should search against, can be None (=all)
        :return results: a JSON response of metadata and results
        :return req_id: UUID of the request
        """

        # debug print
        logging.debug("New audioclip search request")

        # update stats
        if not path in self.stats.requests["paths"]:
            self.stats.requests["paths"][path] = {"total":0, "failed":0, "successful":0}
        self.stats.requests["total"] += 1
        self.stats.requests["paths"][path]["total"] += 1

        # if the cache missed
        if not cacheEntryUuid:
            
            if self.conf.isExtensionActive("space.colabo.flow.audit"):
                cfAReqSWoCache = self.audit_pb2.SubmitAuditRequest(name='searchSoundsNoCache')
                cfAResSWoCache = self.colaboFlowAudit.audit_create(cfAReqSWoCache)
                print("cfAResSWoCache = %s" % (cfAResSWoCache))

            # generate an UUID for the request
            newCacheEntryUuid = str(uuid4())
            graphURI = "http://m2.audiocommons.org/graphs/%s" % newCacheEntryUuid
            mainActionURI = "http://m2.audiocommons.org/actions/%s" % newCacheEntryUuid

            # init a thread list
            threads = []

            # define the thread-worker function
            def worker(conf, sg_query, cp):
                """
                1. calls sparql-generate to access the search provider and generate RDF as a result
                2. stores results in either
                    a) graphstore (self.gs) if exists or
                    b) SEPA otherwise

                Arguments:
                conf - configuration
                sg_query - sparql-generate query
                cp - sound provider name (`jamendo`, `freesound`, `europeana`, ...)
                """


                logging.debug("Sending query to SPARQL Generate")
                # logging.debug(sg_query)

                # do the request to SPARQL-Generate
                try:
                    data = {"query":sg_query}
                    logging.debug("Request sent to the SPARQL Generate:")
                    logging.debug(data)

                    st = time.time()
                    
                    if self.conf.isExtensionActive("space.colabo.flow.go"):
                        actionName = 'sparql-gen'
                        flowId = 'search-sounds'
                        logging.debug("Calling Sparql-gen through ColaboFlow.Go action: '%s' in flow: '%s' " % (actionName, flowId))
                        sg_requestDataStr = json.dumps(data)
                        sg_request = self.go_pb2.ActionExecuteRequest(
                            flowId=flowId, name=actionName, flowInstanceId='fa23', dataIn=sg_requestDataStr)
                        sg_response = self.colaboFlowGo.executeActionSync(sg_request)
                        sg_respones_text = sg_response.dataOut
                    else:
                        logging.debug("Calling Sparql-gen directly")
                        # NOTE: self.conf.tools["sparqlgen"] == self.config["sparql-generate"]["URI"]
                        sg_req = requests.post(self.conf.tools["sparqlgen"], data=data)
                        sg_respones_text = sg_req.text
                    et = time.time()
                    print(et - st)
                except Exception as e:
                    logging.error("Exception during request to SPARQL-Generate server: %s" % (e))
                    self.stats.requests["failed"] += 1
                    self.stats.requests["paths"][path]["failed"] += 1
                    print(traceback.print_exc())
                    return

                logging.debug("Result from the SPARQL Generate:")
                logging.debug(sg_respones_text)

                if self.gs is not None: # if self.gs exists use it
                    try:
                        logging.debug("Posting data to graphstore for newCacheEntryUuid: %s" % (newCacheEntryUuid))
                        self.gs.insertRDF(sg_respones_text, graphURI)
                    except Exception as e:
                        msg = "Error while posting RDF data on graphstore"
                        logging.error(msg)
                        print(traceback.print_exc())
                    logging.debug("Process %s completed!" % cp)

                else: # otherwise use SEPA
                    # from the turtle output create a SPARQL INSERT DATA
                    logging.debug("Creating INSERT DATA query")
                    triples = QueryUtils.getTriplesFromTurtle(sg_respones_text)
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
            # cp are search engines (`jamendo`, `freesound`, `europeana`, ...) 
            for cp in self.conf.mappings["audioclips"]["search"]:

                if (sources and cp in sources) or (not sources):

                    logging.debug("Searching for %s on %s" % (params["pattern"], cp))

                    datetimeNow = "\"" + datetime.datetime.now().isoformat() + "\"" + "^^<http://www.w3.org/2001/XMLSchema#dateTime>"

                    # build the SPARQL-generate query
                    # baseQuery i.e. is a content of the file: `infrastructure-2/semanticMediator/src/services/mediator/lib/mappings/freesound-to-audiocommons/data-adapters/audio-search-by-text.rq`
                    baseQuery = self.conf.mappings["audioclips"]["search"][cp]
                    sg_query = QueryUtils.bindInGenerateQuery(baseQuery, {
                        "pattern": "\"" + params["pattern"] + "\"",
                        "startTime": datetimeNow,
                        "limit": str(params["limit"] or DEFAULT_RESULTS_LIMIT),
                        "page": str(params["page"] or 1)
                    })
                    # sg_query = baseQuery.replace("$pattern", "\"" + pattern + "\"").replace("$startTime", datetimeNow)
                    logging.debug('Modified query')
                    logging.debug(sg_query)

                    # for every mapping spawn a thread
                    t = threading.Thread(target=worker, args=(self.conf, sg_query, cp))
                    threads.append(t)
                    t.start()

            # wait for results
            for t in threads:
                t.join()
            logging.debug("Ready to query SEPA")

            if self.conf.isExtensionActive("space.colabo.flow.audit"):
                cfAResSWoCache = self.colaboFlowAudit.audit_finish(cfAReqSWoCache)

        else: # is cached
            # graphURI = "http://ns#%s" % cacheEntryUuid
            graphURI = "http://m2.audiocommons.org/graphs/%s" % cacheEntryUuid
            mainActionURI = "http://m2.audiocommons.org/actions/%s" % cacheEntryUuid

        # get results from graphstore or ...
        if self.gs is not None: # if self.gs exists, use it
            try:
                msg = "Collating results ..."
                logging.debug(msg)

                self.gs.sparqlUpdate("""
                    PREFIX schema: <http://schema.org/>
                    PREFIX doap: <http://usefulinc.com/ns/doap#>
                    INSERT {
                        GRAPH <%s> {
                            <%s>
                                a schema:SearchAction ;
                                schema:query "%s" ;
                                schema:actionStatus schema:CompletedActionStatus ;
                                schema:object <https://m2.audiocommons.org/api/v%s> ;
                                schema:result ?result ;
                                schema:error ?error .
                            <https://m2.audiocommons.org/api/v%s>
                                a doap:Version;
                                doap:revision "%s".
                            <https://m2.audiocommons.org/api/> doap:release <https://m2.audiocommons.org/api/v%s>.
                        }
                    }
                    WHERE {
                        BIND(BNODE() AS ?searchAction)
                        GRAPH <%s> {
                            {?action schema:result ?result}
                            UNION
                            {?action schema:error ?error}
                        }
                    }""" % (graphURI, mainActionURI, params["pattern"], VERSION, VERSION, VERSION, VERSION, graphURI))
            except Exception as e:
                msg = "Error while collating results: " + e.text
                logging.error(msg)
                self.stats.requests["failed"] += 1
                self.stats.requests["paths"][path]["failed"] += 1
                print(traceback.print_exc())
                return json.dumps(error(params, msg)), -1

            try:
                msg = "Getting RDF data as JSON-LD ..."
                logging.debug(msg)

                resultsTurtle = self.gs.getGraph(graphURI)
                g = rdflib.Graph()
                g.parse(data=resultsTurtle, format="n3")
                resultsJsonLd = g.serialize(format="json-ld")
                logging.debug(json.loads(resultsJsonLd))
                frameTemplate = self.conf.resources["jsonld-frames"]["audioclips"]["search"]
                frame = json.loads(frameTemplate.replace("$mainAction", mainActionURI))
                context = json.loads(self.conf.resources["jsonld-context"])
                jres = QueryUtils.frameAndCompact(json.loads(resultsJsonLd), frame, context)
                logging.debug(jres)
            except Exception as e:
                msg = "Error while getting RDF data as JSON-LD: " + e.text
                logging.error(msg)
                self.stats.requests["failed"] += 1
                self.stats.requests["paths"][path]["failed"] += 1
                print(traceback.print_exc())
                return json.dumps(error(params, msg)), -1

        # ... or from SEPA
        else: # no self.gs, use SEPA
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
                msg = "Querying SEPA ..."
                logging.debug(msg)

                status, results = self.kp.query(self.conf.tools["sepa"]["query"], query)
                frame = json.loads(self.conf.resources["jsonld-frames"]["audioclips"]["search"])
                context = json.loads(self.conf.resources["jsonld-context"])
                jres = QueryUtils.getJsonLD(results, frame, context)
            except:
                msg = "Error while connecting to SEPA"
                logging.error(msg)
                self.stats.requests["failed"] += 1
                self.stats.requests["paths"][path]["failed"] += 1
                return json.dumps(error(params, msg)), -1

        # return results and cache id
        self.stats.requests["successful"] += 1
        self.stats.requests["paths"][path]["successful"] += 1

        if cacheEntryUuid: # previousely cached
            return json.dumps(jres), cacheEntryUuid
        else: # not cached already
            return json.dumps(jres), newCacheEntryUuid


    def show(self, path, audioclipId, source, cacheEntryUuid):

        # debug print
        logging.debug("New audioclip show request")

        # update stats
        if not path in self.stats.requests["paths"]:
            self.stats.requests["paths"][path] = {"total":0, "failed":0, "successful":0}
        self.stats.requests["total"] += 1
        self.stats.requests["paths"][path]["total"] += 1

        # verify if cache exists
        if not cacheEntryUuid:

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
            graphURI = "http://ns#%s" % cacheEntryUuid

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
        if cacheEntryUuid:
            return json.dumps({"status":"ok", "results":results}), cacheEntryUuid
        else:
            return json.dumps({"status":"ok", "results":results}), req_id


    def analyse(self, path, audioclipId, cp, descriptor, cacheEntryUuid):

        # update stats
        if not path in self.stats.requests["paths"]:
            self.stats.requests["paths"][path] = {"total":0, "failed":0, "successful":0}
        self.stats.requests["total"] += 1
        self.stats.requests["paths"][path]["total"] += 1

        # verify if cache exists
        # if not cacheEntryUuid:

        # generate an UUID for the request
        req_id = str(uuid4())
        headers = {"Content-Type":"application/json"}
        graphURI = "http://ns#%s" % req_id

        # invoke the tool
        fullURI = self.conf.tools["ac-analysis"]["baseURI"] + "?provider=%s&id=%s&descriptor=%s" % (cp, audioclipId, descriptor)
        print(fullURI)
        req = requests.get(fullURI, headers=headers)

        # else:
        #     graphURI = "http://ns#%s" % cacheEntryUuid

        # TODO -- parse and "semanticize" results
        results = req.text
        logging.info(req.text)

        # return
        self.stats.requests["successful"] += 1
        self.stats.requests["paths"][path]["successful"] += 1
        if cacheEntryUuid:
            return json.dumps({"status":"ok", "results":results}), cacheEntryUuid
        else:
            return json.dumps({"status":"ok", "results":results}), req_id
