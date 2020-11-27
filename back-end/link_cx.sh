#!/bin/bash
# Author: Alex Gomes
# Description: The purpose is to link instantclient library files for cx_oracle to communicate.

sudo mkdir -p /opt/oracle
sudo cp -r instantclient_19_9 /opt/oracle/

sudo sh -c "echo /opt/oracle/instantclient_19_9 > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig

export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_9:$LD_LIBRARY_PATH