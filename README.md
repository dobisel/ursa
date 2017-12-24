
Ursa
=====

## Branches

### master

[![Build Status](https://travis-ci.com/Carrene/ursa.svg?token=HWnTqWuJD5Ap9uCZHQqx&branch=master)](https://travis-ci.com/Carrene/ursa)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/ursa/badge.svg?branch=master&t=MDoOU3)](https://coveralls.io/github/Carrene/ursa?branch=master)


Setting up development Environment on Linux
----------------------------------

### Installing Dependencies

    $ sudo apt-get install libass-dev libpq-dev postgresql \
        build-essential redis-server redis-tools

### Setup Python environment

    $ sudo apt-get install python3-pip python3-dev
    $ sudo pip3 install virtualenvwrapper
    $ echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
    $ echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
    $ source ~/.bashrc
    $ v.activate
    $ mkvirtualenv --python=$(which python3.6) --no-site-packages ursa

#### Activating virtual environment
    
    $ workon ursa

#### Upgrade pip, setuptools and wheel to the latest version

    $ pip install -U pip setuptools wheel
  
### Installing Project (edit mode)

So, your changes will affect instantly on the installed version

#### nanohttp

    $ cd /path/to/workspace
    $ git clone git@github.com:pylover/nanohttp.git
    $ cd nanohttp
    $ pip install -e .
    
#### restfulpy
    
    $ cd /path/to/workspace
    $ git clone git@github.com:pylover/restfulpy.git
    $ cd restfulpy
    $ pip install -e .

#### ursa
    
    $ cd /path/to/workspace
    $ git clone git@github.com:Carrene/ursa.git
    $ cd ursa
    $ pip install -e .
    $ pip install -r requirement.txt 
    
#### Enabling the bash auto completion for ursa

    $ echo "eval \"\$(register-python-argcomplete ursa)\"" >> $VIRTUAL_ENV/bin/postactivate    
    $ deactivate && workon ursa
    
### Setup Database

#### Configuration(Optional)

Create a file named `~/.config/ursa.yml`

```yaml

db:
  url: postgresql://postgres:postgres@localhost/ursa_dev
  test_url: postgresql://postgres:postgres@localhost/ursa_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres
   
   
```

#### Remove old abd create a new database **TAKE CARE ABOUT USING THAT**

    $ ursa admin create-db --drop --basedata [or instead of --basedata, --mockup]

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ ursa [-c path/to/config.yml] admin drop-db

#### Create database

    $ ursa [-c path/to/config.yml] admin create-db

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ ursa [-c path/to/config.yml] admin create-db --drop
    
#### Create database object

    $ ursa [-c path/to/config.yml] admin setup-db

#### Database migration

    $ ursa migrate upgrade head

#### Insert Base data

    $ ursa [-c path/to/config.yml] admin base-data
    
#### Insert Mockup data

    $ ursa [-c path/to/config.yml] dev mockup-data
    
### Unittests

    $ nosetests
    
### Serving

- Using python builtin http server

```bash
$ ursa [-c path/to/config.yml] serve
```    

- Gunicorn

```bash
$ ./gunicorn
```

### Notification server

```bash
$ ursa serve-notifications
```


- Gunicorn

```bash
$ ./gunicorn-notifications
```
