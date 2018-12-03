# Install

## Java

***NOTE***: It seems that BlazeGraph has problem with Java v10.0.0
+ https://github.com/blazegraph/database/issues/89
+ https://sourceforge.net/p/bigdata/discussion/676946/thread/771a036f/

Downgrading Java version will help:

[How can I see all versions of a package that are available in the archive?](https://askubuntu.com/questions/447/how-can-i-see-all-versions-of-a-package-that-are-available-in-the-archive)
[How To Install Java with `apt` on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-18-04)

```sh
java -version
sudo apt install openjdk-8-jre
sudo apt install openjdk-8-jdk
java -version
sudo update-alternatives --config java
# choose the version you want (1.8.0)
java -version
```

## Preparing virtual environment

```sh
sudo -H virtualenv qmul-infrastructure-2-env
sudo chown -R `whoami` qmul-infrastructure-2-env
source qmul-infrastructure-2-env/bin/activate
sudo -H python -m pip install -r requirements.txt
```

### Installing dependencies

```sh
pip3 install virtualenv
 /home/mprinc/.local/bin/virtualenv
# probably some better place later
cd /var/services
/home/mprinc/.local/bin/virtualenv qmul-infrastructure-2-env
source /var/services/qmul-infrastructure-2-env/bin/activate
cd /var/repos/semanticMediator-ng/
pip3 install -r requirements.txt
# pip3 install rpyc
```

## Blazegraph & SEPA

Ensure you have a running instance of Blazegraph and SEPA. They can be downloaded from [GitHub](https://github.com/desmovalvo/FFSEPABins.git).
To run blazegraph, enter in folder `Endpoints` and run:

```sh
cd SEPA
java -jar blazegraph.jar
```

To run SEPA, enter in folder `Engine`, rename `endpoint-blazegraph.jpar` to `endpoint.jpar` and run:

```sh
cd SEPA
# java -jar SEPAEngine_0.8.4.jar
java -jar engine-v0.9.1.jar
```

### Install sepy library

```sh
git clone https://github.com/arces-wot/SEPA-python3-APIs
cd SEPA-python3-APIs/
# cd /var/repos/SEPA-python3-APIs
source /var/services/qmul-infrastructure-2-env/bin/activate
cd /var/repos/semanticMediator-ng/
python3 setup.py build
# this you might to run as sudo if you do not use virtual environment
python3 setup.py install
```

## Installing sparqlGenerate

https://github.com/sparql-generate/sparql-generate/tree/master/sparql-generate-jena

```sh
git clone https://github.com/sparql-generate/sparql-generate
cd sparql-generate/sparql-generate-jena
# this craches on tests (and licences)
mvn package
# to disable tests and licencing issues
# https://stackoverflow.com/questions/7456006/maven-packaging-without-test-skip-tests
mvn package -Drat.numUnapprovedLicenses=100 -DskipTests
```

## Installing sparqlGenerate-ws

```sh
git clone https://github.com/miguel76/sparql-generate-ws
cd sparql-generate-ws/
java -jar target/sparql-generate-ws.jar 6060
# cd /var/services/sparqlGenerate-ws
# java -jar sparql-generate-ws.jar 6060
```

### Building Local repo

+ [using mvn deploy:deploy-file](https://sookocheff.com/post/java/local-maven-repository/)
    + [mvn deploy:deploy-file](http://maven.apache.org/plugins/maven-deploy-plugin/deploy-file-mojo.html)
+ [manually](https://gist.github.com/timmolderez/92bea7cc90201cd3273a07cf21d119eb)

```sh
cd sparql-generate-ws/
# migth be not necessary
mkdir repo
# Either explicitly described jar lib
mvn deploy:deploy-file \
    -Durl=file://repo \
    -Dfile=sparql-generate-jena-1.2.3-SNAPSHOT.jar \
    -DgroupId=com.github.thesmartenergy \
    -DartifactId=sparql-generate-jena \
    -Dpackaging=jar -Dversion=1.2.3-SNAPSHOT


# or implicitly described (in `pom.xml`) jar lib
mvn deploy:deploy-file \
    -Durl=file://repo \
    -Dfile=sparql-generate-jena-1.2.3-SNAPSHOT.jar \
    -DpomFile=../sparql-generate/sparql-generate-jena/pom.xml
```

Then update `pom.xml` by adding local repo and adding dependency (it will be searched in local repo):

```xml
<repositories>
  <repository>
    <id>project.local</id>
    <name>project</name>
    <url>file:${project.basedir}/repo</url>
  </repository>
</repositories>

<dependencies>
    <dependency>
        <groupId>com.github.thesmartenergy</groupId>
        <artifactId>sparql-generate-jena</artifactId>
        <version>1.2.3-SNAPSHOT</version>
    </dependency>
    <!-- ... -->
</dependencies>
<!-- ... -->
```

Build:

```sh
mvn package
```

You should be able to run it now:

```sh
cd sparql-generate-ws
java -jar target/sparql-generate-ws.jar 6060
```

## Installing Mediator

### Install external git mappings

```sh
git submodule init
git submodule update
```

## Configuring the mediator

There is a default version of the YAML configuration file `mediaconf.example.yaml` that you should copy into `mediaconf.yaml` and set properly.

Edit the YAML configuration file to add your API keys for Freesound, Jamendo and Europeana. Note: these are not the end-user keys for the providers, but rather Audio Commons global-level keys with higher lelvel privileges, since they need to serve N users, so for example number of daily search accesses should be much higher than for a regular single-user keys.

If needed, change the URIs of the underlying services (SEPA, SPARQL-Generate) as needed.

## Running the mediator

```sh
cd semanticMediator-ng
# cd /var/repos/semanticMediator-ng/
# source /var/services/qmul-infrastructure-2-env/bin/activate

python3 mediator.py -c <CONFIG_FILE.yaml>
# for example
# python3 mediator.py -c mediaconf.yaml
```

# Run

```sh
# cd /Users/sasha/Documents/data/development/QMUL/infrastructure-2
cd <mediator-repos>
```

1st terminal. Run blazegraph:

```sh
cd SEPA
java -jar blazegraph.jar
```

2nd terminal. Run SEPA:

```sh
cd SEPA
# java -jar SEPAEngine_0.8.4.jar
java -jar engine-v0.9.1.jar
```

```sh
cd sparql-generate-ws/
java -jar target/sparql-generate-ws.jar 6060
```

```sh
source qmul-infrastructure-2-env/bin/activate
```

# Tests

# from local machine
curl -v -H "Content-Type: application/json" -X GET http://localhost:9027/audioclips/search?pattern=dog

http://localhost:9027/audioclips/search?pattern=dog

The project contains a few unit tests in folder `tests`. To run them, enter in folder `tests` and type:

```
$ MEDIATORTEST=testconf.yaml python3 -m unittest tests.MediatorTests
```