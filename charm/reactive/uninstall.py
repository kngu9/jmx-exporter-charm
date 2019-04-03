import os

from subprocess import check_call

from charmhelpers.core import hookenv

from charms.reactive import hook, set_flag

from charms.layer.jmxexporter import JMXExporter, EXPORTER_SERVICE_PATH

@hook('stop')
def stop():
    try:
        jmx = JMXExporter()
        jmx.close_ports()
        jmx.stop()
        jmx.disable()

        os.remove(EXPORTER_SERVICE_PATH)

        check_call([
            'apt-get', 'auto-remove',
            '--purge', '-y',
            'jmx_prometheus_httpserver'
        ])
    except Exception as e:
        hookenv.log('failed to remove jmx_exporter: {}'.format(e), hookenv.ERROR)