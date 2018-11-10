#!/usr/bin/python3

# requirements
import datetime
from sepy.SEPAClient import *

# debug requirements
import traceback
import pdb

class CacheManager:

    entries = {}

    def __init__(self, conf):

        # store the conf
        self.conf = conf

        # create a KP
        self.kp = SEPAClient()


    def setEntry(self, path, pattern, sources, uuid):

        # add the key if missing
        if not path in self.entries:
            self.entries[path] = {}
        pathEntries = self.entries[path]

        if not pattern in pathEntries:
            pathEntries[pattern] = {}
        patternEntries = pathEntries[pattern]

        # store the uuid
        patternEntries[str(sources)] = {"id": uuid, "timestamp": datetime.datetime.now()}


    def getEntryUiid(self, path, pattern, sources):

        # if a request to that path, with that pattern is found
        # in the cache, then return the results
        if path in self.entries:
            if pattern in self.entries[path]:
                sourcesStr = str(sources)
                if sourcesStr in self.entries[path][pattern]:
                    if (datetime.datetime.now() - self.entries[path][pattern][sourcesStr]["timestamp"]).total_seconds() < 30:
                        return self.entries[path][pattern][sourcesStr]["id"]
                    else:

                        # SPARQL update to delete the subgraph
                        graphURI = "http://ns#%s" % self.entries[path][pattern][sourcesStr]["id"]
                        update = """DELETE { ?s ?p ?o } WHERE { GRAPH <%s> { ?s ?p ?o } }""" % graphURI
                        self.kp.update(self.conf.tools["sepa"]["update"], update)

                        # delete cache entry
                        del self.entries[path][pattern][sourcesStr]
                        if len(self.entries[path][pattern]) == 0:
                            del self.entries[path][pattern]
                        if len(self.entries[path]) == 0:
                            del self.entries[path]

        # return
        return None
