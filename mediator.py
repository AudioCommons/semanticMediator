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
from lib.TrackProcessor import *
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
    # routes for the tracks
    #
    ###########################################
    
    @app.route("/tracks/search")
    def trackSearch():

        # read arguments
        pattern = request.args.get("pattern")

        # invoke the TrackProcessor
        tp = TrackProcessor(conf, sm)
        return tp.search(request.path, pattern)

    
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
        print(cm.entries)
        if cm.getEntry(request.path, pattern) and not request.args.get("nocache"):
            
            logging.debug("Entry found in cache")        

        # invoke the TrackProcessor
        tp = CollectionProcessor(conf, sm)
        results, req_id = tp.search(request.path, pattern, cm.getEntry(request.path,pattern))

        # store entry in cache
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
        
