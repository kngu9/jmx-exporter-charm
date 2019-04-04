from charms.reactive import when

from charmhelpers.core import hookenv

from charms.layer.jmxexporter import JMXExporter


@when('jmxexporter.service-installed')
def autostart():
    jmx = JMXExporter()

    if jmx.is_running():
        hookenv.status_set('active', 'ready')
        jmx.open_ports()
        return

    for i in range(3):
        hookenv.status_set(
            'maintenance',
            'attempting to restart jmx_exporter, '
            'attempt: {}'.format(i+1)
        )
        jmx.restart()
        if jmx.is_running():
            hookenv.status_set('active', 'ready')
            jmx.open_ports()
            return

    hookenv.status_set('blocked', 'failed to start jmx_exporter; check syslog')
