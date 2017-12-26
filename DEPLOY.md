
Ursa deployment guide
======================

Preparation
-----------

### Prerequicites:

```bash
sudo apt-get install build-essential python3-pip postgresql libpq-dev
```

### Python3.6

```bash
sudo apt build-dep python3.5
sudo cd /tmp
sudo wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
sudo tar -xvf Python-3.6.3.tar.xz
sudo cd Python-3.6.3
sudo ./configure
sudo make -j4
sudo make altinstall
```

### Virtual env

```bash
sudo pip3 install -U pip setuptools wheel
sudo pip3 install virtualenvwrapper
``` 

##### Create and login as `dev` user

```bash
sudo adduser dev
su - dev
mkdir ~/workspace
echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
source ~/.bashrc
v.activate
mkvirtualenv --python=$(which python3.6) --no-site-packages ursa
```

##### Setup Database

```bash
echo 'CREATE USER dev' | sudo -u postgres psql
echo 'CREATE DATABASE ursa' | sudo -u postgres psql
echo 'GRANT ALL PRIVILEGES ON DATABASE ursa TO dev' | sudo -u postgres psql
echo "ALTER USER dev WITH PASSWORD 'password'" | sudo -u postgres psql
```

##### Config file

Create a file `~/.config/ursa.yml` with this contents:

```yaml
      url: postgresql://postgres:postgres@localhost/ursa_dev
      test_url: postgresql://postgres:postgres@localhost/ursa_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres
      echo: false
    application:
      welcome_url: http://localhost:8081/welcome
    
    network:
      interfaces_file: /etc/network/interfaces
      default_interface: eth0
```

### Install

```bash
su - dev
mkdir ~/workspace/ursa
cd ~/workspace/ursa
v.activate && workon ursa
pip install -e .
```

##### Database objects

```bash
v.activate && workon ursa
ursa admin setup-db
ursa admin base-data
ursa admin mockup-data  #  if desirable
```

###### Systemd

/etc/systemd/system/ursa.service:

```ini
[Unit]
Description=ursa API daemon
Requires=ursa.socket
After=network.target

[Service]
PIDFile=/run/ursa/pid
User=dev
Group=dev
WorkingDirectory=/home/dev/workspace/ursa/
#ExecStartPre=/bin/mkdir /run/ursa && /bin/chown dev:dev /run/ursa
ExecStart=/home/dev/.virtualenvs/ursa/bin/gunicorn -w 1 --pid /run/ursa/pid -b unix:/run/ursa.socket wsgi_production:app
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target

```

/etc/systemd/system/ursa.socket:

```ini
[Unit]
Description=ursa socket

[Socket]
ListenStream=/run/ursa.socket
#ListenStream=0.0.0.0:9000
#ListenStream=[::]:8000

[Install]
WantedBy=sockets.target
```

/usr/lib/tmpfiles.d/ursa.conf:

```
d /run/ursa 0755 dev dev -
```

Next enable the services so they autostart at boot:

```bash
systemd-tmpfiles --create
systemctl daemon-reload
systemctl enable ursa.socket
service ursa start
```

Either reboot, or start the services manually:

```bash
systemctl start ursa.socket
```

### NGINX

```
upstream ursa_webapi {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response
    server unix:/run/ursa.socket fail_timeout=0;
}


server {
    listen 80;

    location / {
        try_files $uri $uri/ @rewrites;
    }
    
    location ~ /static/(.*) {
        include /etc/nginx/mime.types;
        alias /home/dev/workspace/ursa/static/$1;
    }

    location @rewrites {
      rewrite ^(.+)$ /index.html last;
    }


    location /apiv1/ {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_redirect off;
      proxy_pass http://ursa_webapi;
    }

    
}
