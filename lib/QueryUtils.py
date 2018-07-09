#!/usr/bin/python

# system-wide requirements
import rdflib
import json


class QueryUtils:

    @staticmethod
    def getTriplesFromTurtle(turtle):
        
        # # parse turtle file
        # jturtle = json.loads(turtle)

        # initialize an empty graph, then fill it with the turtle content
        g = rdflib.Graph()
        g.parse(data=turtle, format="n3")

        # iterate over the graph to get triples
        triples = []
        for triple in g:
            triple_string = " "
            for field in triple:
                if isinstance(field, rdflib.term.URIRef):
                    triple_string += " <%s> " % field
                elif isinstance(field, rdflib.term.BNode):
                    triple_string += " _:%s " % field
                else:
                    triple_string += " '%s' " % field.replace("'", "\\'")
            triples.append(triple_string)
        
        # return
        return triples


    @staticmethod
    def getInsertDataFromTriples(triples, graph=None):

        # build the bgp
        bgp = ".".join(triples)
        
        # skeleton
        insertData = """INSERT DATA { GRAPH <%s> { %s }}""" % (graph, bgp)

        # return
        return insertData
