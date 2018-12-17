#!/usr/bin/python3

# system-wide requirements
import yaml
import logging

class MediatorConfigManagerException(Exception):
    pass

class ConfigManager:

    cps = {}
    mappings = {}
    tools = {"sepa": {}, "sparql-generate": {}}
    extensions = {}
    server = {"port": None}

    def readResources(self, resDict):
        # read the resources
        try:

            for resource in resDict:

                if ("file" in resDict[resource]):

                    # open the file and store the content in memory
                    try:
                        with open(resDict[resource]["file"]) as fd:
                            resDict[resource] = fd.read()
                    except FileNotFoundError:
                        raise MediatorConfigManagerException("Mapping file %s not found!" % resDict[resource].file)

                else:
                    self.readResources(resDict[resource])

        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Error while reading engine URIs in configuration file!")


    def __init__(self, configFile):

        # open the configuration file
        try:
            self.config = yaml.load(open(configFile, "r"))
        except FileNotFoundError:
            raise MediatorConfigManagerException("Configuration file not found at: "+ configFile)

        # read server conf
        try:
            self.server["port"] = self.config["mediator"]["port"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong Port Configuration!")

        # read config
        try:
            self.caching = self.config["caching"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong Caching Configuration!")

        # read SEPA URIs
        try:
            self.tools["sepa"]["query"] = self.config["sepa"]["URIs"]["query"]
            self.tools["sepa"]["update"] = self.config["sepa"]["URIs"]["update"]
            self.tools["sepa"]["subscribe"] = self.config["sepa"]["URIs"]["subscribe"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong SEPA Configuration!")

        # read SPARQL-Generate URIs
        try:
            self.tools["sparqlgen"] = self.config["sparql-generate"]["URI"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong SPARQL-generate Configuration!")

        # read extensions
        try:
            if 'extensions' in self.config:
                for extensionName in self.config["extensions"]:
                    extensionConfig = self.config["extensions"][extensionName]
                    if 'general' not in extensionConfig:
                        raise MediatorConfigManagerException("Extension '%s' config should have 'general' key!" % (extensionName))
                    generalExtensionConfig = extensionConfig['general']
                    if 'exists' not in generalExtensionConfig:
                        raise MediatorConfigManagerException("Extension '%s' config should have 'general.exists' key!" % (extensionName))
                    if 'active' not in generalExtensionConfig:
                        raise MediatorConfigManagerException("Extension '%s' config should have 'general.active' key!" % (extensionName))

                    self.extensions[extensionName] = self.config["extensions"][extensionName];

        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Problem with loading mediator extensions configuration!")

        # read graphstore configuration
        if self.config["use-graphstore"]:
            try:
                self.tools["graphstore"] = {}
                self.tools["graphstore"]["sparql-endpoint"] = self.config["graphstore"]["sparql-endpoint"]
                self.tools["graphstore"]["insert-rdf-url"] = self.config["graphstore"]["insert-rdf-url"]
                self.tools["graphstore"]["insert-rdf-graphParam"] = self.config["graphstore"]["insert-rdf-graphParam"]
            except (KeyError, TypeError):
                raise MediatorConfigManagerException("Wrong ac-analysis Configuration!")

        # read Analysis tool configuration
        try:
            self.tools["ac-analysis"] = {}
            self.tools["ac-analysis"]["baseURI"] = self.config["analysisTools"]["baseURI"]
            self.tools["ac-analysis"]["plugins"] = self.config["analysisTools"]["plugins"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong ac-analysis Configuration!")

        # read CPs' URIS
        try:
            self.cps = self.config["contentProviders"]["uris"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong Content Providers URI Configuration!")

        # read the mappings
        try:

            # iterate over entities (e.g. tracks, collections..)
            for entity in self.config["contentProviders"]["mappings"]:

                # iterate over actions (e.g. search..)
                for action in self.config["contentProviders"]["mappings"][entity]:

                    # iterate over content providers (e.g. jamendo, freesound..)
                    for cp in self.config["contentProviders"]["mappings"][entity][action]:

                        # open the file and store the query in memory
                        try:
                            fn = self.config["contentProviders"]["mappings"][entity][action][cp]["file"]
                            with open(fn) as fd:

                                # check if dictionary already contains the needed keys
                                if not entity in self.mappings:
                                    self.mappings[entity] = {}
                                if not action in self.mappings[entity]:
                                    self.mappings[entity][action] = {}

                                # read the mapping
                                q = fd.read()

                                # if a key is given, put it into the mapping!
                                if cp in self.config["contentProviders"]["keys"]:
                                    q = q.replace("$token", "\"" + self.config["contentProviders"]["keys"][cp] + "\"")

                                # store the mapping
                                self.mappings[entity][action][cp] = q

                        except FileNotFoundError:
                            raise MediatorConfigManagerException("Mapping file %s not found!" % fn)

        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Error while reading engine URIs in configuration file!")

        self.resources = self.config["resources"]
        self.readResources(self.resources)

    def getExtensionConfig(self, extensionName):
        try:
            if extensionName in self.extensions:
                return self.extensions[extensionName]
            else:
                return None;
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Problem accessing '%s' extension in configuration file: " % extensionName)

    def isExtensionExisting(self, extensionName):
        try:
            if extensionName in self.extensions:
                return self.extensions[extensionName]['general']['exists']
            else:
                return False;
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Problem accessing '%s' extension in configuration file: " % extensionName)

    def isExtensionActive(self, extensionName):
        try:
            if extensionName in self.extensions:
                return self.extensions[extensionName]['general']['exists'] and self.extensions[extensionName]['general']['active']
            else:
                return False;
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Problem accessing '%s' extension in configuration file: " % extensionName)
