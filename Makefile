TARGETS = charm/files/exporter.deb \
		  builds/jmx-exporter		  

.PHONY: all
all: $(TARGETS)

.PHONY: lint
check: lint

.PHONY: lint
lint:
	flake8 --ignore=E121,E123,E126,E226,E24,E704,E265 ./reactive ./lib

.PHONY: charm-jar
charm-jar: charm/files/exporter.deb

.PHONY: charm
charm: builds/jmx-exporter

builds/jmx-exporter: charm/files/exporter.deb
	charm build ./charm/ -o ./

charm/files/exporter.deb: jmx_exporter/jmx_prometheus_httpserver/target/*.deb
	cp $? charm/files/exporter.deb

jmx_exporter/jmx_prometheus_httpserver/target/*.deb: jmx_exporter/pom.xml
	mvn -f jmx_exporter package

jmx_exporter/pom.xml:
	git submodule update --init --recursive

.PHONY: clean
clean: clean-charm clean-deb

.PHONY: clean-charm
clean-charm:
	$(RM) -r ./builds ./deps

.PHONY: clean-deb
clean-deb:
	$(RM) -r charm/files/jmx_prometheus_httpserver*.deb

.PHONY: deps
deps: submodules

submodules:
	git submodule update --init --recursive
