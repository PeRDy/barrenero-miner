===============
Barrenero Miner
===============

Tools and scripts for mining crypto currencies.

:Version: 1.0.0
:Status: Production/Stable
:Author: José Antonio Perdiguero López

This projects aims to create a platform that provides an easy way of adding miners for different cryptocurrencies,
isolating each miner into a docker container, easy to build, update and independent of the system.

Miners currently supported:

* Ether (`ethminer <https://github.com/ethereum-mining/ethminer>`_).
* Storj (`storj <https://storj.io/>`_).

Full `documentation <http://barrenero.readthedocs.io>`_ for Barrenero project.

Help us Donating
----------------

This project is free and open sourced, you can use it, spread the word, contribute to the codebase and help us donating:

:Ether: 0x566d41b925ed1d9f643748d652f4e66593cba9c9
:Bitcoin: 1Jtj2m65DN2UsUzxXhr355x38T6pPGhqiA
:PayPal: barrenerobot@gmail.com

Requirements
------------

* Python 3.5 or newer. Download `here <https://www.python.org/>`_.
* Docker. `Official docs <https://docs.docker.com/engine/installation/>`_.
* Nvidia Docker. Follow instructions `here <https://github.com/NVIDIA/nvidia-docker>`_.

Quick start
-----------

1. Install services:

    .. code:: console

        ./make install /path/to/storj/storage/volume 4000-4004

1. (Optional) Install with Nvidia overclocking:

    .. code:: console

        ./make install --nvidia /path/to/storj/storage/volume 4000-4004

2. Move to installation folder:

    .. code:: console

        cd /usr/local/lib/barrenero/barrenero-miner/

3. Configure Ether miner parameters in *setup.cfg* file.

4. (Optional) Configure Nvidia overclock parameters in *setup.cfg* file.

5. Configure Storj miner using defined format by Storj service in *storj.json* file.

6. Build all services:

    .. code:: console

        ./make build ether
        ./make build storj

7. Reboot or restart Systemd unit:

    .. code:: console

        sudo service barrenero_miner_ether restart
        sudo service barrenero_miner_storj restart

Systemd
-------

The project provides a service file for Systemd that will be installed. These service files gives a reliable way to run
each miner, as well as overclocking scripts.

To check a miner service status:

.. code:: console

    service barrenero_miner_<miner> status
    service barrenero_miner_ether status

To check a overclock service status:

.. code:: console

    service barrenero_nvidia status

Run manually
------------

As well as using systemd services you can run miners manually using:

.. code:: console
    
    ./make run <miner>

TODO
----

* Add ZCash miner.
* Add Monero miner.
