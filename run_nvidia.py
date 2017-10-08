#!/usr/bin/env python3.6
import sys

try:
    from clinner.command import command, Type as CommandType
    from clinner.run import Main
except (ImportError, ModuleNotFoundError):
    import pip

    print('Installing Clinner')
    pip.main(['install', '--user', '-qq', 'clinner'])

    from clinner.command import command, Type as CommandType
    from clinner.run import Main

from miner.nvidia import NvidiaTuning


@command(command_type=CommandType.PYTHON,
         args=((('-c', '--config-file'), {'help': 'Config file', 'default': 'setup.cfg'}),),
         parser_opts={'help': 'Run Nvidia tuning'})
def nvidia_tuning(*args, **kwargs):
    NvidiaTuning(config=kwargs['config_file']).run()


if __name__ == '__main__':
    sys.exit(Main().run())
