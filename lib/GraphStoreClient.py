#!/usr/bin/python3

import requests
import logging

class GraphStoreClient:

    def __init__(self, conf):

        # save the parameters
        self.conf = conf

    def sparqlQuery(self, queryStr, defaultGraphURI=None, contentType='text/turtle'):
        params = {'query': queryStr}
        if defaultGraphURI is not None:
            params['default-graph-uri'] = defaultGraphURI
        response = requests.get(self.conf['sparql-endpoint'], params, headers={'Accept': contentType})
        response.raise_for_status()
        return response.json() if contentType == 'application/ld+json' else response.text

    def sparqlUpdate(self, updateStr, defaultGraphURI=None):
        logging.debug("Update query: " + updateStr)
        params = {'update': updateStr}
        if defaultGraphURI is not None:
            params['default-graph-uri'] = defaultGraphURI
        response = requests.post(self.conf['sparql-endpoint'], params)
        response.raise_for_status()

    def getGraph(self, graphURI=None, contentType='text/turtle'):
        return self.sparqlQuery('CONSTRUCT WHERE {?s ?p ?o}', graphURI, contentType)

    def insertRDF(self, rdfTxt, graph=None, contentType='text/turtle'):
        parameters = {self.conf['insert-rdf-graphParam']: graph} if graph is not None else {}
        response = requests.post(self.conf['insert-rdf-url'], params=parameters, headers={'Content-Type': contentType}, data=rdfTxt)
        response.raise_for_status()
