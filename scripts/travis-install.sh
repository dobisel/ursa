#!/usr/bin/env bash

# Installing Dependencies
sudo apt-get -qq update
sudo apt-get -qq purge -y --force-yes postgresql-*
sudo apt-get -qq install -y --force-yes libpq-dev build-essential postgresql

# Setting up the PostgreSql
sudo -u postgres psql -c "ALTER USER postgres WITH password 'postgres';"

pip3 install -U pip setuptools wheel coverage coveralls
pip3 install --no-cache -e .
pip3 install -r requirement.txt
