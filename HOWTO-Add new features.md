# Adding the Internet Archive to the AudioCommons Mediator

This report aims to discuss how to extend the AudioCommons Mediator with new media research features. In this case, the research of contents will be made within the [Internet Archive](https://archive.org/advancedsearch.php).

The report will refer to the two following repositories:
1. [The Mediator repository](https://github.com/AudioCommons/semanticMediator) - `sepy-upgrade` branch;
- [The IArchive extension repository](https://github.com/AudioCommons/InternetArchive4Mediator);

### The Mediator

The core of the integration of new services in the AC Mediator is its configuration file. Such YAML file is located at the path `semanticMediator/src/services/mediator/mediaconf.yaml` within its repository. All the information needed to get the media content from services is stored there, and in particular can be found
- Paths to JSON-LD frames to compact the appearance of the Mediator’s output;
- Access keys, if authentication is required by service providers;
- The `mappings>audioclips>search` content, that stores the references to the code that queries the service;

To extend the Mediator’s capabilities, it is needed to include new items in this file. For the Internet Archive we can achieve that by adding in the mappings section the following entry:
```[yaml]
iarchive:
   file: "lib/mappings/semantic-mappings-iarchive/data-adapters/audio-search-by-text.rq"
   args: ["pattern"]
```
As it can be seen, a simple reference is made to the fact that a _pattern_ request is expected. This means that we will be able to search for ‘dog’, ‘cat’, ‘violin’, and so on. Other providers may require also a _token_, which is the grant to access. This is the case of Jamendo, for instance.

The path reported as content of the `file` item, on the other hand, refers to a path that ends in a remote repository. In this case, we switch from the `semanticMediator` repository (1) to the `InternetArchive4Mediator` (2), which is renamed here into `semantic-mappings-iarchive`. This is what is called a [Git Submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

In addition to this, however, it is required for this repository to contain a folder named “data-adapters”, where the request file `audio-search-by-text.rq` should be stored. Such request file embeds a [SPARQL-Generate](https://ci.mines-stetienne.fr/sparql-generate/get-started.html) query. 

In fact, the AudioCommons Mediator’s request procedure is the following:
1. The _pattern_ (and the _token_, if necessary) is received as a direct user interaction. Some other parameters can be also given, like the timestamp of the request, or whatever information is considered useful;
- A first SPARQL-Generate builds the url to which issue the request;
- A second SPARQL-Generate retrieves the triples from the output obtained as a result of the request;
- JSON-LD is generated, containing all the results in a graph form.

### The Internet Archive Submodule
The submodule ([this](https://github.com/AudioCommons/InternetArchive4Mediator) Git repository) contains a set of tools useful to perform a research into the Internet Archive media storage.

The first problem that we must face to include it in the AudioCommons Mediator is to understand how the research can be done. From a plain browser, the Internet Archive offers two different research tools on [this](https://archive.org/advancedsearch.php) webpage. 

The first tool, called _Advanced Search_, allows to make a compound of rules, which may be related to the Title, the Creator, the Mediatype, and other basic metadata. For our purposes, a research should be as general as possible, but limited to audio content, and therefore a first-tentative request may be
```
Title contains PATTERN 
AND
Mediatype is AUDIO
```
Once the query is issued, it is transformed into the following URL:
```
https://archive.org/search.php?query=title%3A%28Violin%29%20AND%20mediatype%3A%28audio%29
```
where we can observe that the actual request has been converted into a url-compatible `title:(Violin) AND mediatype:(audio)`.

Knowing now how to format the query, it is possible to proceed towards the second research tool, the _Advanced Search returning JSON, XML, and more_. There, with the same approach, we get the Query field as `title:(Violin) AND mediatype:(audio)`, while we choose as output the JSON format. The query form also requires to choose at least one of the suggested metadata fields, from which for example we can hereby try “identifier”. The paging is left as 50 results per 1 page. Then, the URL will be
```
https://archive.org/advancedsearch.php?q=title%3A%28Violin%29+AND+mediatype%3A%28audio%29&fl%5B%5D=identifier&sort%5B%5D=&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&output=json&callback=callback&save=yes
```
Where the first thing to observe is that the output is not a JSON file, but a callback call. The first thing to do, then, is to remove `&callback=callback` from the URL, to receive as output a clean and well formatted JSON, useful for any following elaborations.The sorting is also unnecessary for now and can be omitted.

Adding the remaining metadata fields seems to be quite a simple task: if `&fl%5B%5D=identifier` is the URL parameter for the “identifier”, it is reasonable to consider that simply adding `&fl%5B%5D=title` will include also the “title” parameter in the research. However, needing to add all parameter, a shortcut available is to omit directly the `field` item. 

Eventually, we will have globally the following URL:
```
https://archive.org/advancedsearch.php?q=title%3A%28Violin%29+AND+mediatype%3A%28audio%29&rows=50&page=1&output=json&save=yes
```
That can be used as a template for the generic request. A simple URL generator written in Python3 is available in the repository, called `iarchive-urlgen.py`.

Formatting the URL in this fashion, we can proceed to its transformation into a JSON-LD.

### The Interned Archive SPARQL-Generate
SPARQL-Generate is an essential tool for the AudioCommons Mediator. The basic pattern to be used is the following:
```[sparql]
PREFIX iarchive-api: <https://archive.org/advancedsearch.php>
GENERATE {
	[…]
}
WHERE {
    BIND(IRI(CONCAT(
        STR(iarchive-api:),
        "?q=title",
        ENCODE_FOR_URI(":("),
        $pattern,
        ENCODE_FOR_URI(") AND mediatype:(audio)"),
        "&output=json",
        IF(BOUND($limit),CONCAT("&rows=", ENCODE_FOR_URI(STR($limit))),""),
        IF(BOUND($page),CONCAT("&page=", ENCODE_FOR_URI(STR($page))),"")
    )) AS ?ia_url)
}
```
In which the `$pattern` variable is automatically bound externally with the user researched pattern. Clearly, what is stored in the end within the variable `?ia_url` is exactly what has been defined in the previous section as the query URL for the Internet Archive.

For this reason, the contents of the omitted `GENERATE` should look like as 
```
[PREFIXES …]
GENERATE {
	[…]
}
SOURCE ?ia_url AS ?source
WHERE {
	BIND(fn:JSONPath(?source, "$.response.docs") AS ?resultSet)
	[…]
}
```
which is again a nested `GENERATE` that in this case gets the source from the result of a call to `?ia_url`. The remaining content, eventually, is all it is needed to create a set of triples according to the AudioCommons ontology.

Once the Sparql-Generate is ready, the setup for the extended Mediator is complete. It will be possible to start it and use it
1. Start the Sparql-Generate Server;
- Start Blazegraph
- (Start the [SEPA](https://github.com/arces-wot/SEPA))
- Start the Mediator

And eventually perform the request as explained in the Mediator's [documentation](https://m2.audiocommons.org/).

### The SPARQL-Generate in detail
In this subsection a short description of the detail of the SPARQL-Generate will be given. The parts that have already been reported won't be analyzed.

First of all, let's consider this main Generate section:
```[sparql]
GENERATE {
   <https://archive.org/>
      rdf:type foaf:Organization ;
      foaf:name "Internet Archive" .
 # Generate search action description
   ?searchAction
      a schema:SearchAction ;
      schema:object <https://archive.org/> ;
      schema:query $pattern;
      schema:startTime $startTime ;
      schema:endTime ?endTime ;
      schema:actionStatus ?actionStatus ;
      schema:result ?audioCollection ;
      schema:error ?error .
   [...]  
   ?audioCollection
      rdf:type ac:AudioCollection.
      #ac:nodeCount ?nodeCount.
}
SOURCE ?ia_url AS ?source
WHERE {
   BIND(fn:JSONPath(?source, "$.response.docs") AS ?resultSet)
   BIND(BNODE() AS ?searchAction)
   BIND(NOW() as ?endTime)
   BIND(IF(BOUND(?resultSet), schema:CompletedActionStatus, schema:FailedActionStatus) AS ?actionStatus)
   OPTIONAL {
      BIND(BNODE() AS ?audioCollection).
      FILTER(BOUND(?resultSet))
   }
   OPTIONAL {
      BIND(BNODE() AS ?error)
      FILTER(!BOUND(?resultSet))
   }
}.
```
As discussed, the data source in this case is the result of the call to the URL contained in `?ia_url`. Some checks are performed over the JSON, and if successful, the result is stored in variable `?resultSet`. In the `GENERATE` section, some triples are designed to describe the current research task: the _pattern_, the timestamps, the status, and so on.

The omitted part is another `GENERATE` that iterates over the results.
```
GENERATE {
   ?audioCollection ac:memberNode ?audioCollectionNode .
   ?audioCollectionNode
      a ac:AudioCollectionNode ;
      ac:nodeIndex ?index ;
      ac:nodeContent ?audioClip .
   ?audioClip
      a ac:AudioClip;
      dc:title ?title ;
      dc:description ?description;
      ac:author ?creator;
      cc:license ?license;
      ac:originalFile _:originalAudioFile.
   _:originalAudioFile a ac:AudioFile.
   ?publisher 
      ac:published ?audioClip;
      a foaf:Agent.
            
   GENERATE {
      ?audioClip ac:audioCategory ?category
   }
   ITERATOR iter:JSONPath(?res, "$.subject[*]") as ?tag
   WHERE {
      BIND(STR(?tag) AS ?tagStr)
      BIND(IRI(CONCAT(STR(iarchive-tags:),?tagStr)) AS ?category)
   }.
   ?audioPublication
      a ac:AudioPublication;
      ac:publishedAudioManifestation ?audioClip;
      event:time [
         a time:TemporalEntity, time:Instant;
         time:inXSDDateTime ?creationDateTime
      ].
}
ITERATOR iter:JSONElement(?resultSet, "$.[*]") AS ?results
WHERE {
   BIND(BNODE() AS ?audioCollectionNode)
   BIND(fn:JSONPath(?results, "element") AS ?res)
   BIND(fn:JSONPath(?results, "position")+1 AS ?index)
   BIND(STR(fn:JSONPath(?res,"$.title")) AS ?title)
   BIND(STR(fn:JSONPath(?res,"$.description")) AS ?description)
   BIND(IRI(fn:JSONPath(?res,"$.licenseurl")) AS ?license)
   BIND(IRI(CONCAT(STR(iarchive-users:),
      ENCODE_FOR_URI(fn:JSONPath(?res, "$.creator")))) AS ?creator)
   BIND(IRI(CONCAT(STR(iarchive-users:),
      ENCODE_FOR_URI(fn:JSONPath(?res, "$.publisher")))) AS ?publisher)
   BIND(IRI(CONCAT(STR(iarchive-tags:), STR(fn:JSONPath(?res,"$.identifier")))) AS ?audioClip)
   BIND(BNODE() AS ?audioPublication)
   BIND(xsd:dateTime(fn:JSONPath(?res, "$.publicdate")) AS ?creationDateTime)
}.
```
Here is the core of the setup. We here apply the AudioCommons ontology to the results obtained from the Internet Archive. The iterator `ITERATOR iter:JSONElement(?resultSet, "$.[*]") AS ?results` examines each of the results, and associates a _creator_ resource, a _publisher_ resource, and so on.

There is also an inner additional `GENERATE`, that explores the subjects that tag the results.

Have a look the the Jamendo's and FreeSound's SPARQL-Generates to check other examples of that same procedure.