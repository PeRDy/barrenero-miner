import logging
import logging.config
import shlex
import subprocess
import time
from configparser import ConfigParser


class Miner:
    def __init__(self, config):
        self._daemon_command = None
        self._nodes_commands = None

        self.config = ConfigParser()
        self.config.read(config)

        if not self.config.has_section('storj'):
            raise ValueError("Cannot found storj section in config file")

        self.logger = logging.getLogger('ether')
        self.values_logger = logging.getLogger('values')

    @property
    def daemon_command(self):
        if not self._daemon_command:
            self._daemon_command = shlex.split('storjshare daemon -F')

        return self._daemon_command

    @property
    def nodes_commands(self):
        if not self._nodes_commands:
            self._nodes_commands = [shlex.split('storjshare start -c {}'.format(c.strip()))
                                    for c in self.config.get('storj', 'nodes').split(',')]

        return self._nodes_commands

    def run(self):
        try:
            self.logger.info('Run command: %s', self.daemon_command)
            daemon = subprocess.Popen(self.daemon_command)

            time.sleep(10)

            for c in self.nodes_commands:
                subprocess.run(c, check=True)
            daemon.wait()
        finally:
            daemon.terminate()

        return daemon.poll()
