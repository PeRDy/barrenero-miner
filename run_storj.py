#!/usr/bin/env python3
import sys

try:
    from clinner.command import command, Type as CommandType
    from clinner.run import Main
except (ImportError, ModuleNotFoundError):
    import pip
    import site
    import importlib

    print('Installing Clinner')
    pip.main(['install', '--user', '-qq', 'clinner'])

    importlib.reload(site)

    from clinner.command import command, Type as CommandType
    from clinner.run import Main

from miner.storj import Miner as StorjMiner


@command(command_type=CommandType.PYTHON,
         args=((('-c', '--config-file'), {'help': 'Config file', 'default': 'config/storj.cfg'}),),
         parser_opts={'help': 'Run Storj miner'})
def start(*args, **kwargs):
    StorjMiner(config=kwargs['config_file']).run()


if __name__ == '__main__':
    sys.exit(Main().run())
