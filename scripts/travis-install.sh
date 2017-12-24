#!/usr/bin/env bash

# Preparing the config file
CONFIG_FILE="${HOME}/.config/ursa.yml"
CONFIG_DIRECTORY=$(readlink -f ` dirname ${CONFIG_FILE}`)
sudo mkdir -p ${CONFIG_DIRECTORY}
sudo chown -R ${USER}:${USER} ${CONFIG_DIRECTORY}

echo "
db:
  uri: postgresql://postgres:postgres@localhost/ursa_dev
  test_uri: postgresql://postgres:postgres@localhost/ursa_test
  administrative_uri: postgresql://postgres:postgres@localhost/postgres
  echo: false
" > ${CONFIG_FILE}


# Installing Dependencies
sudo apt-get -qq update
sudo apt-get -qq purge -y --force-yes postgresql-*
sudo apt-get -qq install -y --force-yes libpq-dev build-essential postgresql

# Setting up the PostgreSql
sudo -u postgres psql -c "ALTER USER postgres WITH password 'postgres';"

pip3 install -U pip setuptools wheel coverage coveralls
pip3 install "git+https://github.com/pylover/nanohttp@develop"
pip3 install "git+https://github.com/pylover/restfulpy@develop"
pip3 install --no-cache -e .
pip3 install -r requirement.txt
