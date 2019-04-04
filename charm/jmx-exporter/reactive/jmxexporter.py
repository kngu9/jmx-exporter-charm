from charms.reactive import (when_any, when_not, set_flag,
                             clear_flag, hook, when_file_changed)
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


@when_file_changed(hookenv.config()['config'])
@when_any('host-system.available', 'host-system.connected')
def config_added():
    refresh()
