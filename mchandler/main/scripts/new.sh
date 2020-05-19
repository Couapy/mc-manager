#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: new.sh id_new_server version_server"
    exit 1
elif [ "$USER" != "minecraft" ]; then
    echo "err. You must be minecraft user."
    exit 1
fi

if [ ! -e $1 ]; then
    if [ -f /opt/minecraft/servers/$2 ]; then
        mkdir /opt/minecraft/$1
        cp /opt/minecraft/servers/$2 /opt/minecraft/$1/minecraft_server.jar
        echo "eula=true" > /opt/minecraft/$1/eula.txt
    else
        echo "err. The server *$2* version doesn't exists."
    fi
else
    echo "err. Directory $1 already exists."
fi