# Before running the mediator

Ensure you have a running instance of Blazegraph and SEPA. They can be downloaded from [GitHub](https://github.com/desmovalvo/FFSEPABins.git).
To run blazegraph, enter in folder `Endpoints` and run:

```
$ java -jar blazegraph.jar 
```

To run SEPA, enter in folder `Engine`, rename `endpoint-blazegraph.jpar` to `endpoint.jpar` and run:

```
$ java -jar SEPAEngine_0.8.4.jar
```

# Configuring the mediator

Edit the YAML configuration file to add your API keys for Freesound, Jamendo and Europeana as well as the URIs of the underlying services (SEPA, SPARQL-Generate).

# Running the mediator

```
$ python3 mediator.py -c <CONFIG_FILE.yaml>
```

# Tests

The project contains a few unit tests in folder `tests`. To run them, type:

```
$ MEDIATORTEST=testconf.yaml python3 -m unittest tests.MediatorTests
```