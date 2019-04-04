JMX_EXPORTER_VERSION := $(shell awk '/version:/ {print $$2}' snap/snapcraft.yaml | head -1 | sed "s/'//g")

TARGETS = jmx-exporter_$(JMX_EXPORTER_VERSION)_amd64.snap \
		  charm/builds/jmx-exporter		  

.PHONY: all
all: $(TARGETS)

.PHONY: charm
charm: charm/builds/jmx-exporter

charm/builds/jmx-exporter:
	$(MAKE) -C charm/jmx-exporter

.PHONY: snap
snap: jmx-exporter_$(JMX_EXPORTER_VERSION)_amd64.snap

jmx-exporter_$(JMX_EXPORTER_VERSION)_amd64.snap:
	SNAPCRAFT_BUILD_ENVIRONMENT_MEMORY=6G snapcraft

.PHONY: clean
clean: clean-charm clean-snap

.PHONY: clean-charm
clean-charm:
	$(RM) -r charm/builds charm/deps

.PHONY: clean-snap
clean-snap:
	$(RM) -r jmx-exporter_*.snap
	snapcraft clean

.PHONY: check
check: lint

.PHONY: lint
lint:
	flake8 --ignore=E121,E123,E126,E226,E24,E704,E265 charm/
