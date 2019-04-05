from os import path, chmod

from charmhelpers.core import hookenv, host

EXPORTER_PORT = 4081
EXPORTER_SNAP = 'jmx-exporter'
EXPORTER_SERVICE = 'snap.{}.jmx.service'.format(EXPORTER_SNAP)
EXPORTER_COMMON = '/var/snap/{}/common'.format(EXPORTER_SNAP)


class JMXExporter():
    def install(self):
        '''
        Attempts to install configuration files from the config option.
        '''
        cfg_path = path.join(EXPORTER_COMMON, 'config.yaml')

        with open(cfg_path, 'w+') as f:
            f.write(hookenv.config()['config'])

        chmod(cfg_path, 0o440)

    def open_ports(self):
        '''
        Attempts to open the jmx-exporter port.
        '''
        hookenv.open_port(EXPORTER_PORT)

    def close_ports(self):
        '''
        Attempts to close the jmx-exporter port.
        '''
        hookenv.close_port(EXPORTER_PORT)

    def restart(self):
        '''
        Restarts the jmx-exporter service.
        '''
        host.service_restart(EXPORTER_SERVICE)

    def start(self):
        '''
        Starts the jmx-exporter service.
        '''
        host.service_reload(EXPORTER_SERVICE)

    def stop(self):
        '''
        Stops the jmx-exporter service.
        '''
        host.service_stop(EXPORTER_SERVICE)

    def is_running(self):
        '''
        Restarts the jmx-exporter service.
        '''
        return host.service_running(EXPORTER_SERVICE)
