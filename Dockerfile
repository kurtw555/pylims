FROM python:3.8

RUN apt update -y && apt install -y --fix-missing --no-install-recommends \
    python3-pip software-properties-common build-essential \
    cmake sqlite3 gfortran python-dev

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN python --version

WORKDIR /src
COPY . /src/
COPY pylims/uwsgi.ini /etc/uwsgi/

RUN chmod 755 /src/django_start.sh
ENV PYTHONPATH="/src"