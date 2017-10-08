===============
Barrenero Miner
===============

Tools and scripts for mining crypto currencies.

:Version: 1.0.0
:Status: Production/Stable
:Author: José Antonio Perdiguero López

This projects aims to create a platform that provides an easy way of adding miners for different cryptocurrencies,
isolating each miner into a docker container, easy to build, update and independent of the system.

Miners are supported:

* Ether (`ethminer <https://github.com/ethereum-mining/ethminer>`_).
* Storj (`storj <https://storj.io/>`_).


Help us Donating
----------------

This project is free and open sourced, you can use it, spread the word, contribute to the codebase and help us donating:

:Ether: 0x566d41b925ed1d9f643748d652f4e66593cba9c9
:Bitcoin: 1Jtj2m65DN2UsUzxXhr355x38T6pPGhqiA

Requirements
------------

* Python 3.5 or newer. Download `here <https://www.python.org/>`_.
* Docker. `Official docs <https://docs.docker.com/engine/installation/>`_.
* Nvidia Docker. Follow instructions `here <https://github.com/NVIDIA/nvidia-docker>`_.

Quick start
-----------

1. Install services:

.. code:: bash

    ./make install /path/to/storj/storage/volume 4000-4004

1. (Optional) Install with Nvidia overclocking:

.. code:: bash

    ./make install --nvidia /path/to/storj/storage/volume 4000-4004

2. Move to installation folder:

.. code:: bash

    cd /usr/local/lib/barrenero/barrenero-miner/

3. Configure Ether miner parameters in *setup.cfg* file.

3. (Optional) Configure Nvidia overclock parameters in *setup.cfg* file.

4. Configure Storj miner using defined format by Storj service in *storj.json* file.

5. Build all services:

.. code:: bash

    ./make build ether
    ./make build storj

6. Reboot or restart Systemd unit:

.. code:: bash

    sudo service barrenero_miner_ether restart
    sudo service barrenero_miner_storj restart

Systemd
-------

The project provides a service file for Systemd that will be installed. These service files gives a reliable way to run
each miner, as well as overclocking scripts.

To check a miner service status:

.. code:: bash

    service barrenero_miner_<miner> status
    service barrenero_miner_ether status

To check a overclock service status:

.. code:: bash

    service barrenero_nvidia status

Run manually
------------

As well as using systemd services you can run miners manually using:

.. code:: bash
    ./make run <miner>

TODO
----

* Add ZCash miner.
* Add Monero miner.
