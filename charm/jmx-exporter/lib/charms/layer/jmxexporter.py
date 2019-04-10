from os import path

from charmhelpers.core import hookenv, host, templating

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

        unit_name = hookenv.principal_unit() or 'unknown'
        if unit_name == 'unknown':
            app_name = 'unknown'
        else:
            app_name = unit_name.split('/')[0]

        # Render configuration from config option
        templating.render(
            None,
            cfg_path,
            config_template=hookenv.config()['config'],
            context={
                'juju_unit_name': unit_name,
                'juju_application_name': app_name,
            },
            perms=0o644
        )

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
