from subprocess import check_call

from charms.reactive import when, when_not, set_flag, hook

from charms.layer.jmxexporter import JMXExporter


@when_any('host-system.available', 'host-system.connected')
def install():
    JMXExporter().install()
