#!/usr/bin/python

# system-wide requirements
from rdflib import Graph, plugin, URIRef, Literal, BNode
import rdflib
import json
import traceback

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


    @staticmethod
    def getJsonLD(queryResults):

        try:
            res = queryResults
            g = Graph()
            for triple in res["results"]["bindings"]:
                t = []
                for field in ["subject", "predicate", "object"]:
                    if triple[field]["type"] == "uri":
                        t.append(URIRef(triple[field]["value"]))                
                    elif triple[field]["type"] == "bnode":
                        t.append(BNode(triple[field]["value"]))
                    else:
                        t.append(Literal(triple[field]["value"]))
                g.add(t)
                    
            # return
            jld = g.serialize(format="json-ld")
            return jld.decode()
        except:
            print(traceback.print_exc())
