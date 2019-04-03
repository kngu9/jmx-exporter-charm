all: jar charm

lint:
	flake8 --ignore=E121,E123,E126,E226,E24,E704,E265 ./reactive ./lib

.PHONY: jar
charm: builds/jmx-exporter

builds/jmx-exporter: files/exporter.jar
	charm build ./charm/ -o ./

.PHONY: files/exporter.jar
files/exporter.jar: jmx_exporter/collector/target

jmx_exporter/collector/target:
	mvn -f jmx_exporter package
	cp jmx_exporter/collector/target/collector-0.11.1-SNAPSHOT.jar charm/files/exporter.jar

.PHONY: clean
clean: clean-charm clean-jar

.PHONY: clean-charm
clean-charm:
	$(RM) -r ./builds ./deps

.PHONY: clean-jar
clean-jar:
	$(RM) -r jmx_exporter/collector/target
	$(RM) charm/files/exporter.jar

.PHONY: deps
deps: submodules

submodules:
	git submodule update --init --recursive
