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
    configFile = None
    logLevel = None
    conf = None
    
    # initialize logging
    logging.basicConfig(level=logging.DEBUG)

    # load configuration
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:l:", ["help", "conf=", "loglevel="])
        for o,a in opts:
            if o in ("-h", "--help"):
                print("Help message")
                sys.exit()
            elif o in ("-c", "--conf"):
                configFile = a
            elif o in ("-l", "--loglevel"):
                logLevel = a
            else:
                logging.error("Unknown option %s!" % o)
                sys.exit()                            
    except getopt.GetoptError as err:
        sys.exit()

    # open configuration file
    if configFile:
        conf = ConfigManager(configFile)
    else:
        logging.error("You MUST specify a configuration file!")
        sys.exit()

    # initialize a StatsManager
    sm = StatsManager(conf)

    # initialize a CacheManager
    cm = CacheManager(conf)
    
    ###########################################
    #
    # routes for the audioclips
    #
    ###########################################
    
    @app.route("/audioclips/search")
    def audioclipSearch():

        # read arguments
        pattern = request.args.get("pattern")

        # see if the request is present in cache
        cacheEntry = cm.getEntry(request.path,pattern)
        if cacheEntry and not request.args.get("nocache"):            
            logging.debug("Entry found in cache")        

        # invoke the AudioClipProcessor
        tp = AudioClipProcessor(conf, sm)
        results, req_id = tp.search(request.path, pattern, cacheEntry)
        
        # store entry in cache
        if not cacheEntry:
            cm.setEntry(request.path, pattern, req_id)

        # return
        return results
    

    @app.route("/audioclips/<audioclip_id>/analyse")
    def audioclipAnalyse(audioclip_id):

        # read arguments
        source = request.args.get("source")
        descriptor = request.args.get("descriptor")
        
        # see if the request is present in cache
        cacheEntry = cm.getEntry(request.path, audioclip_id, descriptor)
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

        # see if the request is present in cache
        cacheEntry = cm.getEntry(request.path, pattern)
        if cacheEntry and not request.args.get("nocache"):            
            logging.debug("Entry found in cache")        

        # invoke the AudioClipProcessor
        tp = CollectionProcessor(conf, sm)
        results, req_id = tp.search(request.path, pattern, cacheEntry)

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
        
