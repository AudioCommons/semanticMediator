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
        self.expirationTime = self.conf.caching['expiration-time']

        # create a KP
        self.kp = SEPAClient()


    def setEntry(self, path, params, sources, uuid):
        """
        Sets UUID and timestap for the cache entry.
        Cache itself is stored in the triplestore.
        Cache itself is stored in the triplestore and addressed through the UUID which represents namespaced graph.

        Arguments:
        path - request.path
        params - search params (pattern, limit, page, ...)
        source - what sources to search from
        uuid - UUID of the cache (graph) entry
        """

        paramStr = json.dumps(params, sort_keys=True)

        # add the key if missing
        if not path in self.entries:
            self.entries[path] = {}
        pathEntries = self.entries[path]

        if not paramStr in pathEntries:
            pathEntries[paramStr] = {}
        paramEntries = pathEntries[paramStr]

        # store the uuid
        paramEntries[str(sources)] = {"id": uuid, "timestamp": datetime.datetime.now()}


    def getEntryUuid(self, path, params, sources):
        """
        Returns the UUID for the specific search parameters (if matched)
        Cache itself is stored in the triplestore and addressed through the UUID which represents namespaced graph.

        Arguments:
        path - request.path
        params - search params (pattern, limit, page, ...)
        source - what sources to search from
        """

        paramStr = json.dumps(params, sort_keys=True)

        # if a request to that path, with that paramStr is found
        # in the cache, then return the results
        if path in self.entries:
            if paramStr in self.entries[path]:
                sourcesStr = str(sources)
                if sourcesStr in self.entries[path][paramStr]:
                    uuidStr = self.entries[path][paramStr][sourcesStr]["id"]

                    if (datetime.datetime.now() - self.entries[path][paramStr][sourcesStr]["timestamp"]).total_seconds() < self.expirationTime: # if not expired
                        return uuidStr
                    else:

                        # SPARQL update to delete the subgraph
                        graphURI = "http://ns#%s" % uuidStr
                        update = """DELETE { ?s ?p ?o } WHERE { GRAPH <%s> { ?s ?p ?o } }""" % graphURI
                        self.kp.update(self.conf.tools["sepa"]["update"], update)

                        # delete cache entry
                        del self.entries[path][paramStr][sourcesStr]
                        if len(self.entries[path][paramStr]) == 0:
                            del self.entries[path][paramStr]
                        if len(self.entries[path]) == 0:
                            del self.entries[path]

        # return
        return None
