#!/usr/bin/python3

# requirements
from tornado import websocket, web, ioloop
import datetime
import logging
import json
import os


class StatsManager:

    # general attributes
    bootTime = None

    # attributes for requests
    requests = {}
    requests["total"] = 0
    requests["failed"] = 0
    requests["successful"] = 0
    requests["avg_time"] = 0
    requests["paths"] = {}

    
    def __init__(self, conf):
        self.bootTime = datetime.datetime.now()
        self.conf = conf

    def getStats(self):
        return {"bootTime": str(self.bootTime),
                "upTime": str(datetime.datetime.now() - self.bootTime),
                "requests": self.requests,
                "config": self.conf.tools
        }
    
    def reset(self):
        self.total_requests = 0
        self.failed_requests = 0
        self.successful_requests = 0
    

class StatsProcessor():
    
    def __init__(self, stats):
        self.stats = stats
        self.logger = logging.getLogger("mediatorLogger")
        self.template = os.path.join(os.path.dirname(__file__), "templates/stats.html")

    def getStats(self):

        # get stats
        return self.stats.getStats()

    
    def get(self):

        if self.request.path == "/stats":
            
            # debug print
            self.logger.debug("Stats request")
            
            # get stats
            res = self.stats.getStats()
            
            # json or html?
            key = self.get_argument('format', None)
            if key == "json":
                
                # return a json dict
                self.set_header("Content-Type", "application/json")
                self.write(json.dumps(res))
                
            else:
                
                # render a web page
                self.render(self.template, stats=res)
                
        elif self.request.path == "/clearStats":

            # reset stats
            self.stats.reset()

            # return the stats
            res = self.stats.getStats()
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(res))


