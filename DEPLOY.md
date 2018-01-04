
Ursa deployment guide
======================

Preparation
-----------

### Prerequicites:

```bash
sudo su -
apt-get install nginx build-essential python3-pip postgresql libpq-dev
```

### Python3.6

```bash
apt build-dep python3.5
cd /tmp
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
tar -xvf Python-3.6.*.tar.xz
cd Python-3.6.*
./configure
make -j4
make altinstall
```

### Virtual env

```bash
pip3.6 install -U pip setuptools wheel
``` 


##### Setup Database

```bash
echo 'CREATE USER root' | sudo -u postgres psql
echo 'CREATE DATABASE ursa WITH owner root' | sudo -u postgres psql
```

##### Config file

Create a file `/etc/ursa.yml` with this contents:

```yaml
db:
  url:  url: postgresql+psycopg2://ursa:@/ursa

  echo: false
application:
  welcome_url: http://localhost:8081/welcome
    
network:
  interfaces_dir:  /etc/network
  interfaces_file: /etc/network/interfaces
  default_interface: enp0s3
```

###Install
Go to your ursa repository on your workspace
```bash
cd path/to/ursa
git archive --format tar origin/master | ssh root@ursa-sandbox 'tar -xv -C /usr/local/ursa'
```

On server
```bash
cd /usr/local
v.activate && workon ursa
sudo pip install -e .
```

#### Install Network Interfaces
Go to your network-interfaces repository on your workspace

```bash
cd path/to/network-interfaces
git archive --format tar.gz origin/master | ssh root@ursa-sandbox 'cat - > /tmp/network-interfaces.tar.gz'
```
On server
```bash
pip3.6 install /tmp/network-interfaces.tar.gz 

```


#### Database objects

```bash
v.activate && workon ursa
ursa -c /etc/ursa.yml admin create-db --drop --basedata
```

##### Systemd

/etc/systemd/system/ursa.service:

```ini
[Unit]
Description=ursa API daemon
Requires=ursa.socket
After=network.target

[Service]
PIDFile=/run/ursa/pid
User=root
WorkingDirectory=/usr/local/ursa/
ExecStart=/usr/local/bin/gunicorn -w 1 --pid /run/ursa/pid -b unix:/run/ursa.socket wsgi_production:app
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

[Install]
WantedBy=sockets.target
```

/usr/lib/tmpfiles.d/ursa.conf:

```
d /run/ursa 0755 root root -
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

/etc/nginx/sites-available/ursa

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
      alias /usr/local/ursa/static/$1;
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
```
#### Restart Nginx

```bash
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/ursa /etc/nginx/sites-enabled/
service nginx restart
```

## Reboot the device!

```bash
reboot
```