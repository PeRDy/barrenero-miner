# Barrenero Miner
Tools and scripts for mining crypto currencies.

* **Version**: 1.0.0
* **Status**: Production/Stable
* **Author**: José Antonio Perdiguero López

This projects aims to create a platform that provides an easy way of adding miners for different cryptocurrencies,
isolating each miner into a docker container, easy to build, update and independent of the system.

Miners currently supported:

* Ether ([ethminer](https://github.com/ethereum-mining/ethminer)).
* Storj ([storj](https://storj.io/)).

Full [documentation](http://barrenero.readthedocs.io) for Barrenero project.

## Help us Donating
This project is free and open sourced, you can use it, spread the word, contribute to the codebase and help us donating:

* **Ether**: `0x566d41b925ed1d9f643748d652f4e66593cba9c9`
* **Bitcoin**: `1Jtj2m65DN2UsUzxXhr355x38T6pPGhqiA`
* **PayPal**: `barrenerobot@gmail.com`

## Requirements
* Docker. [Official docs](https://docs.docker.com/engine/installation/).
* Nvidia Docker. Follow instructions [here](https://github.com/NVIDIA/nvidia-docker).

## Quick start
* Run Ether miner: `docker run -v /etc/barrenero/miner/:/etc/barrenero/miner/ perdy/barrenero-miner-ether:latest`
* Run Storj miner: `docker run -p=4000-4003:4000-4003 -v /etc/barrenero/miner/:/etc/barrenero/miner/ perdy/barrenero-miner-storj:latest`
* Run Nvidia Overclock: `python /usr/local/lib/barrenero/nvidia_tuning.py`

## TODO
* Add ZCash miner.
* Add Monero miner.
