import os
import shutil
import filecmp

from subprocess import check_call, check_output

from charmhelpers.core import hookenv, templating, host


EXPORTER_PORT = 4081
EXPORTER_UNIT = 'jmx_exporter'
EXPORTER_SERVICE = '{}.service'.format(
    EXPORTER_UNIT
)
EXPORTER_APT_NAME = 'jmx_prometheus_httpserver'
EXPORTER_SERVICE_PATH = '/etc/systemd/system/{}'.format(
    EXPORTER_SERVICE
)
EXPORTER_CONFIG_PATH = '/etc/jmx_exporter/{}.yaml'.format(
    EXPORTER_UNIT
)

class JMXExporter():
    def install(self, service=False):
        '''
        Attempts to install jar to path if checksum if different or
        does not exists.
        '''

        # Install debian file
        check_call([
            'apt', 'install', '-y',
            '{}/files/exporter.deb'.format(hookenv.charm_dir())
        ])

        if service:
            # Install as a service
            ex = ' '.join([
                shutil.which(EXPORTER_UNIT),
                '{addr}:{port}'.format(
                    addr=hookenv.unit_private_ip(),
                    port=EXPORTER_PORT
                ),
                EXPORTER_CONFIG_PATH
            ])
            
            templating.render(
                source='{}'.format(EXPORTER_SERVICE),
                target=EXPORTER_SERVICE_PATH,
                owner='root',
                perms=0o400,
                context={
                    'exporter_path': ex
                }
            )

            check_call(['systemctl', 'enable', EXPORTER_SERVICE])

            check_call(['journalctl', '--unit={}'.format(EXPORTER_SERVICE)])

    def configure(self):
        templating.render(
            source='jmx_exporter.yaml',
            target=EXPORTER_CONFIG_PATH,
            owner='root',
            perms=0o644,
            context={}
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

    def enable(self):
        if not self.is_enabled():
            check_call(['systemctl', 'enable', EXPORTER_SERVICE])
            check_call(['journalctl', '--unit={}'.format(EXPORTER_SERVICE)])

    def disable(self):
        check_call([
            'systemctl', 'disable', EXPORTER_SERVICE
        ])

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
    
    def is_enabled(self):
        '''
        Returns true if service is enabled
        '''
        return check_output([
            'systemctl', 'is-enabled', EXPORTER_SERVICE
        ]).decode('utf-8') == 'enabled'

    def is_running(self):
        '''
        Restarts the jmx-exporter service.
        '''
        return host.service_running(EXPORTER_SERVICE)