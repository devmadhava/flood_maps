#!/bin/bash

echo "Starting GIS Dev Environment..."

# Install Python + pip if not present
apt-get update -y
apt-get install -y python3 python3-pip wget unzip

# Install WhiteboxTools if missing
if [ ! -f /usr/local/whitebox/whitebox_tools ]; then
    echo "Installing WhiteboxTools..."
    mkdir -p /usr/local/whitebox
    cd /usr/local/whitebox
    wget https://www.whiteboxgeo.com/WBT_Linux.zip -O wbt.zip
    unzip wbt.zip
    chmod +x whitebox_tools
    rm wbt.zip
    cd /
fi

# Install Python libs ONCE
if [ ! -f /venv_done ]; then
    echo "Installing Python packages from requirements.txt..."
    pip3 install -r /workspace/requirements.txt
    touch /venv_done
fi

echo "Environment Ready!"
exec bash  # drop into shell
