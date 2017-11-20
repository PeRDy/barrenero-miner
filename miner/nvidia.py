import logging
import logging.config
import os
import shlex
import subprocess
import time
from configparser import ConfigParser


class NvidiaTuning:
    NVIDIA_SMI = {
        'compute_mode': '-c',
        'persistent_mode': '-pm',
        'max_power': '-pl',
        'gpu_operation_mode': '--gom'
    }
    NVIDIA_SETTINGS = {
        'gpu': {
            'powermizer_mode': 'GPUPowerMizerMode',
            'fan_control': 'GPUFanControlState',
            'graphics_clock_offset': 'GPUGraphicsClockOffset[3]',
            'memory_transfer_rate_offset': 'GPUMemoryTransferRateOffset[3]',
        },
        'fan': {
            'fan_speed': 'GPUTargetFanSpeed',
        }
    }

    def __init__(self, config='miner.cfg'):
        self.config = ConfigParser()
        self.config.read(config)

        if not self.config.has_section('nvidia'):
            raise ValueError('Cannot found nvidia section in config file')

        if not self.config.get('nvidia', 'graphic_cards'):
            raise ValueError('Cannot found graphic_cards value defined in nvidia section')

        self.logger = logging.getLogger('miner')

    def _run_command(self, command, background=False, **kwargs):
        self.logger.info('Run command: %s', command)

        stdout = None if background else subprocess.PIPE
        process = subprocess.Popen(shlex.split(command), stdout=stdout, bufsize=1, universal_newlines=True, **kwargs)

        if not background:
            for line in (m.rstrip() for m in process.stdout):
                self.logger.info(line)

            process.stdout.close()
            return_code = process.poll()
        else:
            return_code = 0

        return return_code

    def run(self):
        self._run_command('sudo service xdm start')

        # Wait before OC
        time.sleep(10)

        # nvidia-settings config
        os.environ['DISPLAY'] = ':0'
        os.environ['XAUTHORITY'] = '/var/run/xdm/root/:0'

        # nvidia-smi config
        for setting, flag in self.NVIDIA_SMI.items():
            value = self.config.get('nvidia', setting, fallback=None)
            if value:
                self._run_command(f'nvidia-smi {flag} {value}')

        settings = [(tag, s, f) for tag, subs in self.NVIDIA_SETTINGS.items() for s, f in subs.items()]
        for tag, setting, flag in settings:
            for i in [int(x) for x in self.config.get('nvidia', 'graphic_cards').split(',')]:
                value = self.config.get(f'nvidia:{i}', setting, fallback=None)
                if value:
                    self._run_command(f'nvidia-settings -c :0 -a "[{tag}:{i}]/{flag}={value}"')

        time.sleep(5)
        self._run_command('sudo service xdm stop')
