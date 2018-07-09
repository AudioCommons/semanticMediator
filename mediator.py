#!/usr/bin/python3

# system-wide requirements
from tornado import websocket, web, ioloop
import threading
import logging
import getopt
import yaml
import sys

# local requirements
from lib.ConfigManager import *
from lib.TrackProcessor import *
from lib.StatsProcessor import *
from lib.CollectionProcessor import *

# initialize app
app = None

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
        
    # define routes
    app = web.Application([
        ("/tracks/search", TrackProcessor, dict(conf=conf, stats=sm)),
        ("/tracks/analyse", TrackProcessor, dict(conf=conf, stats=sm)),
        ("/collections/search", CollectionProcessor, dict(conf=conf, stats=sm)),
        ("/stats", StatsProcessor, dict(stats=sm))
    ])
    
    # start the server
    try:
        logging.debug("Starting semantic mediator...")
        app.listen(9027)
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.debug("Bye!")
        sys.exit(0)
