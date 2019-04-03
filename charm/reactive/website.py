from charms.layer.jmxexporter import EXPORTER_PORT

from charms.reactive import when


@when('website.available')
def setup_website(website):
    website.configure(EXPORTER_PORT)
