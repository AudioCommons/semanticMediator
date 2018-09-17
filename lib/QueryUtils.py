#!/usr/bin/python

# system-wide requirements
from rdflib import Graph, plugin, URIRef, Literal, BNode
import rdflib
import json
import traceback
import logging
from pyld import jsonld

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
                    languageStr = ('@' + field.language) if field.language else ''
                    datatypeStr = ('^^<' + field.datatype + '>') if field.datatype else ''
                    valueStr = "'%s'" % field.replace("'", "\\'")
                    triple_string += " " + valueStr + languageStr + datatypeStr + " "
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
    def getOrderFromFrame(frame):
        if not isinstance(frame, dict):
            return None
        newDict = {}
        if "@order" in frame:
            newDict["@order"] = frame["@order"]
            del frame["@order"]
        for key,value in frame.items():
            subframe = QueryUtils.getOrderFromFrame(value)
            if subframe is not None:
                newDict[key] = subframe
        return newDict if len(newDict) > 0 else None

    @staticmethod
    def executeOrderList(input, order):
        input.sort(key=lambda item: item[order] if order in item else None)

    @staticmethod
    def executeOrder(input, order):
        if not isinstance(order, dict):
            return
        if isinstance(input, dict):
            for key, value in input.items():
                if key in order:
                    QueryUtils.executeOrder(value, order[key])
        elif isinstance(input, list):
            if "@order" in order:
                QueryUtils.executeOrderList(input, order["@order"])
            for item in input:
                QueryUtils.executeOrder(item, order)

    @staticmethod
    def frameAndCompact(input, frame, context):
        orderStruct = QueryUtils.getOrderFromFrame(frame)
        framedResults = jsonld.frame(json.loads(input), frame)
        compactedResults = jsonld.compact(framedResults, context)
        if "@graph" in compactedResults:
            results = compactedResults["@graph"]
        else:
            if "@context" in compactedResults:
                del compactedResults["@context"]
            results = compactedResults
        QueryUtils.executeOrder(results, orderStruct)
        return results

    @staticmethod
    def getJsonLD(queryResults, frame, context):

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
                    elif triple[field]["type"] == "literal":
                        if "xml:lang" in triple[field]:
                            t.append(Literal(triple[field]["value"], lang=triple[field]["lang"]))
                        elif "datatype" in triple[field]:
                            type = URIRef(triple[field]["datatype"])
                            t.append(Literal(triple[field]["value"], datatype=type))
                        else:
                            t.append(Literal(triple[field]["value"]))
                g.add(t)

            # return
            jld = g.serialize(format="json-ld")
            return QueryUtils.frameAndCompact(jld, frame, context)
        except:
            print(traceback.print_exc())
