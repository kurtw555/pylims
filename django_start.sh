#!/bin/bash
django-admin.py migrate auth --noinput          # used for login
django-admin.py migrate sessions --noinput      # used for login
exec uwsgi /etc/uwsgi/uwsgi.ini                 # Start uWSGI (HTTP router that binds Python WSGI to a web server, e.g. NGINX)