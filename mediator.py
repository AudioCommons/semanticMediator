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
        source - what sources from
        nocache - avoid cache
        """

        # read arguments
        pattern = request.args.get("pattern")

        if conf.isExtensionActive("space.colabo.search_extension"):
            flow = request.args.get("flow")
            print("[/audioclips/search]parameters pattern: %s" %(pattern));
            print("[/audioclips/search]parameters flow: %s" %(flow));
            print("[/audioclips/search]parameters source: %s" %(request.args.get("source")));
            if(flow == 'extended'):
                # r = ['dog', 'cat']
                r = rpcService.get_synonyms(pattern)
                pattern = (',').join(r)
                print("[/audioclips/search] extended pattern: %s" %(pattern));

        sources = request.args.get("source").split(",") if request.args.get("source") else None

        # see if the request is present in cache
        cacheEntryUuid = cm.getEntryUiid(request.path, pattern, sources)
        if cacheEntryUuid and not request.args.get("nocache"):
            logging.debug("Entry found in cache")

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.search(request.path, pattern, cacheEntryUuid, sources)

        # store entry in cache
        if not cacheEntryUuid:
            cm.setEntry(request.path, pattern, sources, req_id)

        # return
        return results


    @app.route("/audioclips/<audioclip_id>/analyse")
    def audioclipAnalyse(audioclip_id):

        # read arguments
        source = request.args.get("source")
        descriptor = request.args.get("plugin")

        # see if the request is present in cache
        cacheEntryUuid = cm.getEntryUiid(request.path, audioclip_id, source)
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
        cacheEntryUuid = cm.getEntryUiid(request.path, audioclip_id, source)
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
        cacheEntryUuid = cm.getEntryUiid(request.path, pattern, sources)
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
