from charms.reactive import (when, when_any, when_not, when_none,
                             set_flag, clear_flag, hook)
from charms.reactive.helpers import data_changed

from charmhelpers.core import hookenv

from charms.layer.jmxexporter import JMXExporter


def refresh():
    hookenv.status_set('maintenance', 'refreshing service')
    clear_flag('jmxexporter.service-installed')

    jmx = JMXExporter()
    jmx.install()
    jmx.restart()

    set_flag('jmxexporter.service-installed')


@when_not('jmxexporter.service-installed')
def waiting():
    refresh()


@hook('config-changed')
def config_changed():
    if not data_changed('jmx_exporter.config', hookenv.config()['config']):
        return

    refresh()


@when_any('host-system.available', 'host-system.connected')
@when_not('jmx.connected')
def host_added():
    refresh()
    set_flag('jmx.connected')


@when_none('host-system.available', 'host-system.connected')
@when('jmx.connected')
def host_removed():
    refresh()
    clear_flag('jmx.connected')
