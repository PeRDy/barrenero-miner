import json
import logging
import logging.config
import os
import re
import shlex
import subprocess
from configparser import ConfigParser


class Miner:
    def __init__(self, config='setup.cfg'):
        self._command = None
        self._account = None

        self.config = ConfigParser()
        self.config.read(config)

        if not self.config.has_section('ether'):
            raise ValueError("Cannot found miner section in config file")

        self.logger = logging.getLogger('ether')
        self.values_logger = logging.getLogger('values')

    @property
    def command(self):
        if not self._command:
            bin_path = os.path.expanduser(self.config.get('ether', 'bin'))
            args = self.config.get('ether', 'args', fallback='')
            pool_primary = self.config.get('ether', 'pool_primary')
            pool_secondary = self.config.get('ether', 'pool_secondary')
            worker_name = self.config.get('ether', 'worker', fallback='Worker')
            email = self.config.get('ether', 'email', fallback=None)
            worker = f'{self.account}.{worker_name}'
            if email:
                worker += f'/{email}'

            self._command = f'{bin_path} {args} -S {pool_primary} -FS {pool_secondary} -O {worker}'

        return self._command

    @property
    def account(self):
        if not self._account:
            try:
                self._account = self.config.get('ether', 'wallet')

                if self._account[:2] != '0x':
                    self._account = '0x' + self._account
            except PermissionError:
                raise PermissionError('Cannot access to wallet account')

        return self._account

    def run(self):
        os.environ['GPU_FORCE_64BIT_PTR'] = '0'
        os.environ['GPU_MAX_HEAP_SIZE'] = '100'
        os.environ['GPU_USE_SYNC_OBJECTS'] = '1'
        os.environ['GPU_MAX_ALLOC_PERCENT'] = '100'
        os.environ['GPU_SINGLE_ALLOC_PERCENT'] = '100'

        hashes_regex = re.compile(r'gpu/(\d+).+?(\d+\.\d+)')
        self.logger.info('Run command: %s', self.command)
        process = subprocess.Popen(shlex.split(self.command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   bufsize=1, universal_newlines=True)

        for message in (m.rstrip() for m in process.stdout):
            hashes = {int(gpu): float(value) for gpu, value in hashes_regex.findall(message)}

            if hashes:
                self.values_logger.info(json.dumps(hashes))
            else:
                self.logger.info(message)

        process.stdout.close()
        return process.poll()
