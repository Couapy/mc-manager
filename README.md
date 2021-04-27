# mc-manager

[![Django Units tests](https://github.com/Couapy/mc-manager/actions/workflows/unit-test.yml/badge.svg)](https://github.com/Couapy/mc-manager/actions/workflows/unit-test.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-red.svg)](https://github.com/5kyc0d3r/upnpy/blob/master/LICENSE)

This is a web manager for Minecraft servers. The instances of Minecraft Servers are executed on the same device.

## Why this project ?

This project solves an issue I had with friends during gaming evenings :
I own a personal server that runs minecraft servers to play with friends, but when they needed to
create or started a server, I had to connect myself by ssh and run commands.

So I wanted to code a web manager that allow my friends and myself to administrate Minecraft servers easily.

## Install

Follow this instructions to install the project :

```bash
# Clone repository
git clone https://github.com/Couapy/mc-manager.git

# Execute
docker-compose up --build

# Download servers
docker exec daphne python manage.py updatemclist
```

## Configuration

All configuration is available in the `config.cfg` file.

**Please generate a secret for django before send application in production !**

The config file provide settings for :

* Django
* Minecraft server instances (RAM & versions availables)
* Mails
* OAuth providers
