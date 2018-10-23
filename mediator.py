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
app = Flask(__name__)

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

    rpcConn = rpyc.connect("158.37.63.127", 12374)
    rpcService = rpcConn.root


    ###########################################
    #
    # routes for the audioclips
    # curl -v -H "Content-Type: application/ld+json" -X GET http://localhost:9027/audioclips/search?pattern=whale
    # curl -v -H "Content-Type: application/json" -X GET http://localhost:9027/audioclips/search?pattern=whale
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
        cacheEntry = cm.getEntry(request.path, pattern)
        if cacheEntry and not request.args.get("nocache"):            
            logging.debug("Entry found in cache")  

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.search(request.path, pattern, cacheEntry, sources)
        
        # store entry in cache
        if not cacheEntry:
            cm.setEntry(request.path, pattern, req_id)

        # return
        return results
    

    @app.route("/audioclips/<audioclip_id>/analyse")
    def audioclipAnalyse(audioclip_id):

        # read arguments
        source = request.args.get("source")
        descriptor = request.args.get("plugin")
        
        # see if the request is present in cache
        cacheEntry = cm.getEntry(request.path, audioclip_id)
        if cacheEntry and not request.args.get("nocache"):            
            logging.debug("Entry found in cache")        

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.analyse(request.path, audioclip_id, source, descriptor, cacheEntry)

        # store entry in cache
        if not cacheEntry:
            cm.setEntry(request.path, audioclip_id, req_id)

        # return
        return results


    @app.route("/audioclips/<audioclip_id>")
    def audioclipShow(audioclip_id):

        # read arguments
        source = request.args.get("source")
        
        # see if the request is present in cache
        cacheEntry = cm.getEntry(request.path, audioclip_id)
        if cacheEntry and not request.args.get("nocache"):            
            logging.debug("Entry found in cache")        

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.show(request.path, audioclip_id, source, cacheEntry)

        # store entry in cache
        if not cacheEntry:
            cm.setEntry(request.path, audioclip_id, req_id)

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
        cacheEntry = cm.getEntry(request.path, pattern)
        if cacheEntry and not request.args.get("nocache"):            
            logging.debug("Entry found in cache")        

        # invoke the AudioClipProcessor
        tp = CollectionProcessor(conf, sm)
        results, req_id = tp.search(request.path, pattern, cacheEntry, sources)

        # store entry in cache
        if not cacheEntry:
            cm.setEntry(request.path, pattern, req_id)

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

    
    ###########################################
    #
    # start the app!
    #
    ###########################################
    
    app.run(port=conf.server["port"], threaded=True)