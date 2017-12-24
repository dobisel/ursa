
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

#### Configuration

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
 

Setting up development Environment on Windows (Tested for Windows 10)
----------------------------------

### Setup Python environment
- Install Python on Windows (https://www.python.org/downloads/) and make sure the Scripts subdirectory of Python is in your PATH.
   For example, if python is installed in C:\Python35-32\,
   you should make sure C:\Python35-32\Scripts is in your PATH in addition to C:\Python35-32\.

- Install related Microsoft Visual C++ Build Tools according to your python version mentioned on [WindowsCompilers](https://wiki.python.org/moin/WindowsCompilers)
- Run the following command on a Command Prompt to install Virtual Environment Wrapper for Windows:

```
    > pip install virtualenvwrapper-win
```


- Add WORKON_HOME variable as an Environment Variable and set the value %USERPROFILE%\Envs by default.

- Run the following command to make a Virtual Environment for "ursa" :

```
    > mkvirtualenv ursa
```

#### Activating virtual environment

    > workon ursa

#### Upgrade pip, setuptools and wheel to the latest version

    (ursa) > pip install -U pip setuptools wheel

### Installing Project in Virtual Environment(edit mode)

So, your changes will affect instantly on the installed version

#### restfulpy

    (ursa) > cd path/to/ursa/..
    (ursa) > git clone git@github.com:pylover/restfulpy.git
    (ursa) > cd restfulpy
    (ursa) > pip install -e .

    (ursa) > cd path/to/ursa/..
    (ursa) > git clone git@github.com:pylover/nanohttp.git
    (ursa) > cd nanohttp
    (ursa) > pip install -e .

    (ursa) > cd /path/to/ursa
    (ursa) > pip install -e .

### Setup PostgreSQL
You can find the windows installer on https://www.postgresql.org/download/windows/

### Setup Database

- Create the ursa.yml file in %USERPROFILE%\AppData\Local
- Add the following lines to this file
```
    db:
      uri: postgresql://postgres:postgres@localhost/ursa_dev
      administrative_uri: postgresql://postgres:postgres@localhost/postgres
      test_uri: postgresql://postgres:postgres@localhost/ursa_test
      echo: true
```

#### create database **TAKE CARE ABOUT USING THAT**

    (ursa) /path/to/ursa > ursa admin create-db --drop --basedata

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    (ursa) /path/to/ursa > ursa -c path/to/ursa.yml admin drop-db

#### Create database

    (ursa) /path/to/ursa > -c path/to/ursa.yml admin create-db

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    (ursa) /path/to/ursa > ursa -c path/to/ursa.yml admin create-db --drop

#### Create database object

    (ursa) /path/to/ursa > ursa -c path/to/ursa.yml admin setup-db

#### Database migration

    (ursa) /path/to/ursa > ursa migrate upgrade head

#### Insert Base data

    (ursa) /path/to/ursa > ursa -c path/to/ursa.yml admin base-data

#### Insert Mockup data

    (ursa) /path/to/ursa > ursa -c path/to/ursa.yml dev mockup-data

### Unittests
This command will generate the Mark-Down documents which are needed for Front-end developers :

    (ursa) /path/to/ursa > nosetests

### Serving

- Using nanohttp server

```
    (ursa) /path/to/ursa > ursa serve
```

