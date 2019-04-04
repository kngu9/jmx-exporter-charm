from charmhelpers.core import hookenv

from charms.reactive import hook, set_flag

from charms.layer import snap
from charms.layer.jmxexporter import EXPORTER_SNAP


@hook('stop')
def uninstall():
    try:
        snap.remove(EXPORTER_SNAP)
    except Exception as e:
        # log errors but do not fail stop hook
        hookenv.log('failed to remove snap: {}'.format(e), hookenv.ERROR)
