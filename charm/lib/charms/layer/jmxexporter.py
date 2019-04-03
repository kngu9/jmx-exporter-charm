import os
import shutil
import filecmp

from charmhelpers.core import hookenv


EXPORTER_PORT = 4081
EXPORTER_PATH = '/opt/jmx_exporter/exporter.jar'


class JMXExporter():
    def install():
        '''
        Attempts to install jar to path if checksum if different or
        does not exists.
        '''
        should_copy = False

        if not os.path.exists(EXPORTER_PATH):
            os.makedirs(os.path.dirname(EXPORTER_PATH))
            should_copy = True
        else:
            if not filecmp.cmp(
                '{}/files/exporter.jar'.format(hookenv.charm_dir()),
                EXPORTER_PATH,
                shallow=True
            ):
                should_copy = True

        if should_copy:
            shutil.copy(
                '{}/files/exporter.jar'.format(hookenv.charm_dir()),
                EXPORTER_PATH
            )
            os.chmod(EXPORTER_PATH, 0o755)