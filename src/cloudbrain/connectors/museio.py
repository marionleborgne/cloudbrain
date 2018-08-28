import logging
import os
import subprocess
import sys
import time

_LOGGER = logging.getLogger(__name__)
_LOGGER.level = logging.DEBUG
_LOGGER.addHandler(logging.StreamHandler())

_MUSE_IO_INSTALL_TIP = ("Unable to start muse-io. Muse-io might not be "
                        "installed. "
                        "Go to http://choosemuse.com for more info.")



class _UnableToStartMuseIO(Exception):
    """Error starting muse-io"""
    pass



def _start_muse_io(port):
    """
    Start muse-io to pair with a muse.
    :param port: (int) Port used to pair the Muse.
    """
    cmd = ["muse-io", "--osc", "osc.udp://localhost:%s" % port]

    _LOGGER.debug("Running command: %s" % " ".join(cmd))

    # On Mac you need to update the dynamic library path find muse-io
    env = os.environ.copy()
    if sys.platform == 'darwin':
        if 'DYLD_LIBRARY_PATH' in env:
            env['DYLD_LIBRARY_PATH'] += ':/Applications/Muse'
        else:
            env['DYLD_LIBRARY_PATH'] = '/Applications/Muse'

    _LOGGER.debug("About to start muse-io process ...")
    try:
        museio_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
        museio_process.communicate()
        _LOGGER.debug("Started muse-io process.")
    except OSError as e:
        _LOGGER.error(e)
        raise _UnableToStartMuseIO(_MUSE_IO_INSTALL_TIP)
    except KeyboardInterrupt:
        exit(0)

    while True:
        line = museio_process.stdout.readline()
        if line != '':  # look for museIO running keywords
            _LOGGER.debug(line)
            if "OSC messages will be emitted" in line:
                _LOGGER.info("SUCCESS: MuseIO connected to a device!")
                break
        else:
            raise _UnableToStartMuseIO(_MUSE_IO_INSTALL_TIP)
        time.sleep(0.1)
