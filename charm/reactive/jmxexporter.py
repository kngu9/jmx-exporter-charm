from os import path

from subprocess import check_call

from charms.reactive import (when, when_any, when_not, set_flag,
                             clear_flag, hook, when_file_changed)

from charmhelpers.core import hookenv

from charms.layer.jmxexporter import JMXExporter


def refresh():
    hookenv.status_set('maintenance', 'refreshing service')
    clear_flag('jmxexporter.available')

    jmx = JMXExporter()
    jmx.install(service=True)
    check_call(['systemctl', 'daemon-reload'])

    set_flag('jmxexporter.available')


@when_not('jmxexporter.installed')
def install():
    JMXExporter().install()
    set_flag('jmxexporter.installed')


@when_any('host-system.available', 'host-system.connected')
@when_not('jmxexporter.available')
def waiting():
    hookenv.status_set('waiting', 'waiting for config')


@hook('upgrade-charm')
def upgrade():
    refresh()


@when('config.changed')
def config_changed():
    refresh()


@when_file_changed(hookenv.config()['config'])
@when_any('host-system.available', 'host-system.connected')
def config_added():
    # Prevent charm from firing initially
    if path.isfile(hookenv.config()['config']):
        refresh()
