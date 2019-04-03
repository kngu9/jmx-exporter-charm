from subprocess import check_call

from charms.reactive import when_any, when_not, set_flag, hook

from charmhelpers.core import hookenv

from charms.layer.jmxexporter import JMXExporter


@when_not('jmxexporter.configured')
def waiting():
    hookenv.status_set('waiting', 'waiting for host-system relation')

@when_any('host-system.available', 'host-system.connected')
def install():
    jmx = JMXExporter()
    jmx.configure()
    jmx.install(service=True)
    jmx.open_ports()
    set_flag('jmxexporter.configured')


@hook('upgrade-charm')
def upgrade():
    jmx = JMXExporter()
    JMXExporter().install()
    jmx.restart()


@hook('config-changed')
def config_changed():
    jmx = JMXExporter()
    jmx.configure()
    jmx.restart()
    set_flag('jmxexporter.configured')
