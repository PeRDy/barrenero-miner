#!/usr/bin/env python3
import logging
import os
import shlex
import shutil
import subprocess
import sys

try:
    import docker
    import jinja2
    from clinner.command import command, Type as CommandType
    from clinner.run import Main
except ImportError:
    import importlib
    import pip
    import site

    print('Installing dependencies')
    pip.main(['install', '--user', '-qq', 'clinner', 'docker', 'jinja2'])

    importlib.reload(site)

    import docker
    import jinja2
    from clinner.command import command, Type as CommandType
    from clinner.run import Main

logger = logging.getLogger('cli')

docker_cli = docker.from_env()

APP_CHOICES = (
    'ether',
    'storj',
)


def _docker_flags(name, code, ports, network, storage):
    flags = []
    # App volumes
    if storage:
        flags.append('-v {}:/srv/apps/barrenero-miner-{}/storage/'.format(storage, name))

    if code:
        flags.append('-v {}:/srv/apps/barrenero-miner-{}'.format(os.getcwd(), name))

    flags.append('-v {}:/srv/apps/barrenero-miner-{}/logs'.format(os.path.join("/var/log/barrenero/miner", name), name))

    # Flags
    flags.append('--rm --name=barrenero-miner-{}'.format(name))
    flags.append('--network={}'.format(network))
    flags.append(' '.join(['-p {}'.format(port) for port in ports]))

    return ' '.join(flags)


def _create_network(name):
    if not docker_cli.networks.list(names=name):
        docker_cli.networks.create(name)


@command(command_type=CommandType.SHELL_WITH_HELP,
         args=((('app',), {'help': 'App name', 'choices': APP_CHOICES}),
               (('-f', '--dockerfile'), {'help': 'Dockerfile'})),
         parser_opts={'help': 'Docker build for local environment'})
def build(*args, **kwargs):
    cmd = shlex.split(
        'docker build -t barrenero-miner-{0}:latest -f dockerfiles/{0}/Dockerfile .'.format(kwargs["app"]))
    cmd += list(args)
    return [cmd]


@command(command_type=CommandType.SHELL,
         args=((('app',), {'help': 'App name', 'choices': APP_CHOICES}),
               (('--network',), {'help': 'Docker network', 'default': 'barrenero'}),
               (('-c', '--code',), {'help': 'Add code folder as volume', 'action': 'store_true'}),
               (('-i', '--interactive'), {'help': 'Docker image tag', 'action': 'store_true'}),
               (('-p', '--ports'), {'help': 'Ports to bind', 'nargs': '*', 'default': []}),
               (('--storage',), {'help': 'Storage folder for Storj'}),
               (('--no-nvidia',), {'help': 'Run with docker', 'action': 'store_true'})),
         parser_opts={'help': 'Run application'})
def run(*args, **kwargs):
    _create_network(kwargs['network'])

    # Select docker binary
    docker_bin = 'docker' if kwargs['no_nvidia'] else 'nvidia-docker'

    flags = _docker_flags(kwargs['app'], kwargs['code'], kwargs['ports'], kwargs['network'], kwargs['storage'])
    interactive_flag = '-it' if kwargs['interactive'] else '-d'

    cmd = shlex.split('{} run {} {} barrenero-miner-{}:latest -q --skip-check'.format(
        docker_bin, flags, interactive_flag, kwargs['app']))
    cmd += list(args)
    return [cmd]


@command(command_type=CommandType.SHELL,
         args=((('app',), {'help': 'App name', 'choices': APP_CHOICES}),
               (('--network',), {'help': 'Docker network', 'default': 'barrenero'}),
               (('-c', '--code',), {'help': 'Add code folder as volume', 'action': 'store_true'}),
               (('--ports',), {'help': 'Ports to bind', 'nargs': '*', 'default': []}),
               (('--storage',), {'help': 'Storage folder for Storj'}),
               (('--no-nvidia',), {'help': 'Run with docker', 'action': 'store_true'})),
         parser_opts={'help': 'Run application'})
def create(*args, **kwargs):
    _create_network(kwargs['network'])

    # Select docker binary
    docker_bin = 'docker' if kwargs['no_nvidia'] else 'nvidia-docker'

    flags = _docker_flags(kwargs['app'], kwargs['code'], kwargs['ports'], kwargs['network'], kwargs['storage'])

    cmd = shlex.split('{} create {} barrenero-miner-{}:latest'.format(docker_bin, flags, kwargs['app']))
    cmd += list(args)
    return [cmd]


@command(command_type=CommandType.PYTHON,
         args=((('storj_path',), {'help': 'Path to storj storage volume', 'default': '/storage/storj'}),
               (('storj_ports',), {'help': 'Range of storj ports to bind', 'default': '4000-4010'}),
               (('--path',), {'help': 'Barrenero full path', 'default': '/usr/local/lib/barrenero'}),
               (('-n', '--nvidia'), {'help': 'Adds nvidia overclock service', 'action': 'store_true'}),),
         parser_opts={'help': 'Install the application in the system'})
def install(*args, **kwargs):
    if not os.geteuid() == 0:
        logger.error('Script must be run as root')
        return -1

    path = os.path.abspath(os.path.join(kwargs['path'], 'barrenero-miner'))

    # Jinja2 builder
    j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(path, 'templates')))
    systemd_j2_context = {
        'app': {
            'name': 'barrenero-miner',
            'path': path,
        },
        'ether': {},
        'storj': {
            'ports': kwargs['storj_ports'],
            'volume': kwargs['storj_path'],
        },
        'nvidia': kwargs['nvidia']
    }

    # Create app directory
    logger.info("[Barrenero Miner] Install app under %s", path)
    shutil.rmtree(path, ignore_errors=True)
    shutil.copytree('.', path)

    # Create setup file
    logger.info("[Barrenero Miner] Defining config file")
    with open(os.path.join(path, 'setup.cfg'), 'w') as f:
        f.write(j2_env.get_template('setup.cfg.jinja2').render(systemd_j2_context))

    # Create Ether Systemd unit
    logger.info("[Barrenero Miner] Create Ether Miner's Systemd unit and enable it")
    with open('/etc/systemd/system/barrenero_miner_ether.service', 'w') as f:
        f.write(j2_env.get_template('barrenero_miner_ether.service.jinja2').render(systemd_j2_context))
    subprocess.run(shlex.split('systemctl enable barrenero_miner_ether.service'))

    # Create Storj Systemd unit
    logger.info("[Barrenero Miner] Create Storj Miner's Systemd unit and enable it")
    with open('/etc/systemd/system/barrenero_miner_storj.service', 'w') as f:
        f.write(j2_env.get_template('barrenero_miner_storj.service.jinja2').render(systemd_j2_context))
    subprocess.run(shlex.split('systemctl enable barrenero_miner_storj.service'))

    # Create Nvidia OC Systemd unit
    if kwargs['nvidia']:
        logger.info("[Barrenero Miner] Create Nvidia Overclock's Systemd unit and enable it")
        with open('/etc/systemd/system/barrenero_nvidia.service', 'w') as f:
            f.write(j2_env.get_template('barrenero_nvidia.service.jinja2').render(systemd_j2_context))
        subprocess.run(shlex.split('systemctl enable barrenero_nvidia.service'))

    subprocess.run(shlex.split('systemctl daemon-reload'))

    logger.info("[Barrenero Miner] Installation completed")


if __name__ == '__main__':
    sys.exit(Main().run())