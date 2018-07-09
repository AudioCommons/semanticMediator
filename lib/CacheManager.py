#!/usr/bin/python3

# debug requirements
import traceback
import pdb

class CacheManager:

    entries = {}
        
    def __init__(self):
        pass

    def setEntry(self, path, pattern, uuid):

        # add the key if missing
        if not path in self.entries:
            self.entries[path] = {}

        # store the uuid
        self.entries[path][pattern] = uuid

    
    def getEntry(self, path, pattern):

        # if a request to that path, with that pattern is found
        # in the cache, then return the results
        if path in self.entries:
            if pattern in self.entries[path]:
                return self.entries[path][pattern]
        return None
