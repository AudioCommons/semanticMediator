#!/usr/bin/python3

# system-wide requirements
from flask import Flask, render_template, request
import threading
import logging
import getopt
import yaml
import sys

# local requirements
from lib.CacheManager import *
from lib.ConfigManager import *
from lib.AudioClipProcessor import *
from lib.StatsProcessor import *
from lib.CollectionProcessor import *

# initialize app
app = Flask(__name__, static_url_path='')

# main
if __name__ == "__main__":

    # basic initialization
    configFileName = None
    logLevel = None
    conf = None

    # initialize logging
    logging.basicConfig(level=logging.DEBUG)

    # load configuration
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:l:", ["help", "conf=", "loglevel="])
        for name,value in opts:
            if name in ("-h", "--help"):
                print("Parameters")
                print("\t-c (--conf)  configuration file")
                print("\t-l (--loglevel)  setting up the logging level (optional")
                print("\t-h (--help)  provides this help")
                print("Example:")
                print("\tpython3 mediator.py -c mediaconf.yaml")
                sys.exit()
            elif name in ("-c", "--conf"):
                configFileName = value
            elif name in ("-l", "--loglevel"):
                logLevel = value
            else:
                logging.error("Unknown option %s!" % name)
                sys.exit()
    except getopt.GetoptError as err:
        print("Error: %s" %(err))
        sys.exit()

    # open configuration file
    if configFileName:
        conf = ConfigManager(configFileName)
    else:
        logging.error("You MUST specify a configuration file!")
        sys.exit()

    # initialize a StatsManager
    sm = StatsManager(conf)

    # initialize a CacheManager
    cm = CacheManager(conf)

    # word_forms service
    # rpyc client
    import sys
    import rpyc

    searchExtensionConfig = conf.getExtensionConfig("space.colabo.search_extension")
    if conf.isExtensionActive("space.colabo.search_extension"):
        rpcConn = rpyc.connect(searchExtensionConfig['host'], searchExtensionConfig['port'])
        rpcService = rpcConn.root

    colaboFlowAuditConfig = conf.getExtensionConfig("space.colabo.flow.audit")
    if conf.isExtensionActive("space.colabo.flow.audit"):
        import uuid
        # from colabo.flow.audit import ColaboFlowAudit, audit_pb2
        from colabo.flow.audit import audit_pb2
        from colabo.flow.audit import ColaboFlowAudit

        gRpcUrl = colaboFlowAuditConfig['host']+':'+str(colaboFlowAuditConfig['port'])
        # https://docs.python.org/2/library/uuid.html
        flowInstanceId = str(uuid.uuid1())
        cfAuditRequestDefualt = audit_pb2.SubmitAuditRequest(
            bpmn_type='activity',
            bpmn_subtype='task',
            bpmn_subsubtype='sub-task',

            flowId='searchForSounds',

            userId=colaboFlowAuditConfig['userId'],
            sessionId=colaboFlowAuditConfig['sessionId'],
            flowInstanceId=flowInstanceId,

            implementationId=colaboFlowAuditConfig['implementationId'],
            implementerId=colaboFlowAuditConfig['implementerId']
        )
        colaboFlowAudit = ColaboFlowAudit(socketUrl=gRpcUrl, defaultAuditRequest=cfAuditRequestDefualt)

    # @app.route('/')
    # def root():
    #     return app.send_static_file('index.html')

    ###########################################
    #
    # routes for the audioclips
    # curl -v -H "Content-Type: application/ld+json" -X GET http://localhost:9027/audioclips/search?pattern=whale
    # curl -v -H "Content-Type: application/json" -X GET http://localhost:9027/audioclips/search?pattern=whale
    # curl -v -H "Content-Type: application/ld+json" -X GET http://m2.audiocommons.org/api/audioclips/search?pattern=whale
    #
    ###########################################

    @app.route("/audioclips/search")
    def audioclipSearch():
        """
        Performs search for audioclips

        Arguments:
        pattern - what we are searching for
        limit - max number of results from each provider
        page - page of results (for all the providers)
        source - what sources from
        nocache - avoid cache
        """

        # read arguments
        pattern = request.args.get("pattern")
        limit = request.args.get("limit")
        page = request.args.get("page")
        
        if conf.isExtensionActive("space.colabo.flow.audit"):
            cfAuditRequestDefault = colaboFlowAudit.getDefaultRequest()
            cfAuditRequestDefault.flowInstanceId = str(uuid.uuid1())+":"+pattern
            cfAReqStart = audit_pb2.SubmitAuditRequest(name='start')
            cfAResStart = colaboFlowAudit.audit_create_and_finish(cfAReqStart)

        if conf.isExtensionActive("space.colabo.search_extension"):
            flow = request.args.get("flow")
            print("[/audioclips/search]parameters pattern: %s" %(pattern));
            print("[/audioclips/search]parameters flow: %s" %(flow));
            print("[/audioclips/search]parameters source: %s" %(request.args.get("source")));
            if(flow == 'extended'):
                if conf.isExtensionActive("space.colabo.flow.audit"):
                    cfAReqExtSyn = audit_pb2.SubmitAuditRequest(name='extended.synonyms')
                    cfAResExtSyn = colaboFlowAudit.audit_create(cfAReqExtSyn)
    

                # r = ['dog', 'cat']
                r = rpcService.get_synonyms(pattern)
                pattern = (',').join(r)
                print("[/audioclips/search] extended pattern: %s" %(pattern));
                if conf.isExtensionActive("space.colabo.flow.audit"):
                    cfAResExtSyn = colaboFlowAudit.audit_finish(cfAReqExtSyn)
    

        sources = request.args.get("source").split(",") if request.args.get("source") else None

        queryParams = {
            "pattern": pattern,
            "limit": limit,
            "page": page
        }

        if conf.isExtensionActive("space.colabo.flow.audit"):
            cfAReqChkCache = audit_pb2.SubmitAuditRequest(name='checkCache')
            cfAResChkCache = colaboFlowAudit.audit_create_and_finish(cfAReqChkCache)

        # see if the request is present in cache
        # "cheating" a bit, as this is rather "checking for cache" time
        if conf.isExtensionActive("space.colabo.flow.audit"):
            cfAReqSWCache = audit_pb2.SubmitAuditRequest(name='searchSoundsWithCache')
            cfAResSWCache = colaboFlowAudit.audit_create(cfAReqSWCache)

        cacheEntryUuid = cm.getEntryUuid(request.path, queryParams, sources)
        if cacheEntryUuid and not request.args.get("nocache"):
            logging.debug("Entry found in cache")
        
            if conf.isExtensionActive("space.colabo.flow.audit"):
                cfAResSWCache = colaboFlowAudit.audit_finish(cfAReqSWCache)

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.search(request.path, queryParams, cacheEntryUuid, sources)

        # store entry in cache
        if not cacheEntryUuid:
            if conf.isExtensionActive("space.colabo.flow.audit"):
                cfAReqSvCache = audit_pb2.SubmitAuditRequest(name='saveCache')
                cfAResSvCache = colaboFlowAudit.audit_create(cfAReqSvCache)


            cm.setEntry(request.path, queryParams, sources, req_id)

            if conf.isExtensionActive("space.colabo.flow.audit"):
                cfAResSvCache = colaboFlowAudit.audit_finish(cfAReqSvCache)


        if conf.isExtensionActive("space.colabo.flow.audit"):
            cfAuditRequest = audit_pb2.SubmitAuditRequest(name='end',       flowInstanceId=cfAuditRequestDefualt.flowInstanceId+":"+pattern
            )
            cfAuditResult = colaboFlowAudit.audit_create_and_finish(cfAuditRequest)
            print("cfAuditResult = %s" % (cfAuditResult))

        # return
        return results


    @app.route("/audioclips/<audioclip_id>/analyse")
    def audioclipAnalyse(audioclip_id):

        # read arguments
        source = request.args.get("source")
        descriptor = request.args.get("plugin")

        # see if the request is present in cache
        cacheEntryUuid = cm.getEntryUuid(request.path, audioclip_id, source)
        if cacheEntryUuid and not request.args.get("nocache"):
            logging.debug("Entry found in cache")

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.analyse(request.path, audioclip_id, source, descriptor, cacheEntryUuid)

        # store entry in cache
        if not cacheEntryUuid:
            cm.setEntry(request.path, audioclip_id, source, req_id)

        # return
        return results


    @app.route("/audioclips/<audioclip_id>")
    def audioclipShow(audioclip_id):

        # read arguments
        source = request.args.get("source")

        # see if the request is present in cache
        cacheEntryUuid = cm.getEntryUuid(request.path, audioclip_id, source)
        if cacheEntryUuid and not request.args.get("nocache"):
            logging.debug("Entry found in cache")

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.show(request.path, audioclip_id, source, cacheEntryUuid)

        # store entry in cache
        if not cacheEntryUuid:
            cm.setEntry(request.path, audioclip_id, source, req_id)

        # return
        return results


    ###########################################
    #
    # routes for the collections
    #
    ###########################################


    @app.route("/collections/search")
    def collectionSearch():

        # read pattern
        pattern = request.args.get("pattern")
        sources = request.args.get("source").split(",") if request.args.get("source") else None

        # see if the request is present in cache
        cacheEntryUuid = cm.getEntryUuid(request.path, pattern, sources)
        if cacheEntryUuid and not request.args.get("nocache"):
            logging.debug("Entry found in cache")

        # invoke the AudioClipProcessor
        tp = CollectionProcessor(conf, sm)
        results, req_id = tp.search(request.path, pattern, cacheEntryUuid, sources)

        # store entry in cache
        if not cacheEntryUuid:
            cm.setEntry(request.path, pattern, sources, req_id)

        # return
        return results


    ###########################################
    #
    # routes for the stats
    #
    ###########################################

    @app.route("/stats")
    def stats():
        sp = StatsProcessor(sm)
        res = sp.getStats()
        return render_template("stats.html", stats=res)

    @app.after_request
    def apply_global_headers(response):
        response.headers["Content-Type"] = "application/json"
        response.headers["Link"] = "<https://json-ld.org/contexts/person.jsonld>; rel=\"http://www.w3.org/ns/json-ld#context\"; type=\"application/ld+json\""
        response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


    ###########################################
    #
    # start the app!
    #
    ###########################################

    app.run(port=conf.server["port"], threaded=True)
