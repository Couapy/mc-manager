#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: properties.sh id_server properties_temp_path"
    exit 1
elif [ "$USER" != "minecraft" ]; then
    echo "err. You must be minecraft user."
    exit 1
fi

# Ajouter les lignes au fichier
# Supprimer les doublons
