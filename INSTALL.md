* install PostgreSQL 8.3+

* make sure you have virtualenv installed:
http://www.virtualenv.org/en/latest/

* download helios-server

* cd into the helios-server directory

* create a virtualenv:

```
virtualenv venv
```

* activate virtual environment

```
source venv/bin/activate
````

* install requirements

```
pip install -r requirements.txt
```

* reset database

```
./reset.sh
```

* start server

```
python manage.py runserver
```

* to start Helios as a service using systemd

add a service definition (e.g. helios.service) in /etc/systemd/system with the following content:

```
[Unit]
Description=Helios Voting
After=network.target

[Service]
Type=simple
Environment=EMAIL_USE_AWS=0
Environment=HELIOS_DIR=*TODO*
WorkingDir=${HELIOS_DIR}
ExecStart=/bin/bash -c '${HELIOS_DIR}/venv/bin/python ${HELIOS_DIR}/manage.py runserver'
User=*TODO*
Group=*TODO*

[Install]
WantedBy=multi-user.target
```

You also need to install rabbitmq:

```
sudo apt install rabbitmq-server
```
And add a celery message broker service (helios-celery.service):

```
[Unit]
Description=Helios Voting Celery Message Broker
After=network.target

[Service]
Type=simple
Environment=HELIOS_DIR=*TODO*
ExecStart=/bin/bash -c 'cd ${HELIOS_DIR} && source venv/bin/activate && celery worker --app helios --events --beat --concurrency 1 --logfile celeryw.log --pidfile celeryw.pid'
WorkingDir=${HELIOS_DIR}
User=*TODO*
Group=*TODO*

[Install]
WantedBy=multi-user.target
```

Then add, enable and start the services:
```
sudo systemctl daemon-reload
sudo systemctl enable helios
sudo systemctl start helios
sudo systemctl enable helios-celery
sudo systemctl start helios-celery
```

* to get Google Auth working:

** go to https://console.developers.google.com

** create an application

** set up oauth2 credentials as a web application, with your origin, e.g. https://myhelios.example.com, and your auth callback, which, based on our example, is https://myhelios.example.com/auth/after/

** still in the developer console, enable the Google+ API.

** set the GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET configuration variables accordingly.