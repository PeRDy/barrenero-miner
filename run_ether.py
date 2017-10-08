#!/usr/bin/env python3.6
import logging
import logging.config
import sys
import time

try:
    from clinner.command import command, Type as CommandType
    from clinner.run import Main as ClinnerMain
except (ImportError, ModuleNotFoundError):
    import pip

    print('Installing Clinner')
    pip.main(['install', '--user', '-qq', 'clinner'])

    from clinner.command import command, Type as CommandType
    from clinner.run import Main as ClinnerMain

from miner.ether import Miner as EtherMiner


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


class Main(ClinnerMain):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'value_json': {
                '()': UTCFormatter,
                'format': '{'
                          '"timestamp":"%(asctime)s",'
                          '"value":%(message)s'
                          '}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'json': {
                '()': UTCFormatter,
                'format': '{'
                          '"timestamp":"%(asctime)s",'
                          '"level":"%(levelname)s",'
                          '"file":"%(filename)s",'
                          '"line":%(lineno)d,'
                          '"message":"%(message)s"'
                          '}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'plain': {
                '()': UTCFormatter,
                'format': '[%(asctime)s] (%(levelname)s:%(filename)s:%(lineno)d) %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'plain',
                'level': 'DEBUG',
            },
            'base_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/base.log',
                'formatter': 'json',
                'level': 'INFO',
                'maxBytes': 10 * (2 ** 20),
                'backupCount': 5
            },
            'values_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/values.log',
                'formatter': 'value_json',
                'level': 'INFO',
                'maxBytes': 1 * (2 ** 20),
                'backupCount': 100
            },
        },
        'loggers': {
            'values': {
                'handlers': ['values_file'],
                'level': 'INFO',
                'propagate': False
            },
            'ether': {
                'handlers': ['console', 'base_file'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }

    def __init__(self):
        super().__init__()

        logging.config.dictConfig(self.LOGGING)


@command(command_type=CommandType.PYTHON,
         args=((('-c', '--config-file'), {'help': 'Config file', 'default': 'setup.cfg'}),
               (('--nvidia-tuning',), {'help': 'Enable nvidia tuning', 'action': 'store_true', 'default': False}),),
         parser_opts={'help': 'Run Ether miner'})
def ether(*args, **kwargs):
    EtherMiner(config=kwargs['config_file']).run()


if __name__ == '__main__':
    sys.exit(Main().run())
