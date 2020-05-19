#!/bin/bash

if [ $# -ne 4 ]; then
    echo "Usage: config.sh id_new_server min_ram max_ram server_port"
    exit 1
elif [ "$USER" != "minecraft" ]; then
    echo "err. You must be minecraft user."
    exit 1
fi

echo "MCMINMEM=$2" > /opt/minecraft/$1/server.conf
echo "MCMAXMEM=$3" >> /opt/minecraft/$1/server.conf
echo "PORT=$4" >> /opt/minecraft/$1/server.conf
