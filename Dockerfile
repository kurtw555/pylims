FROM python:3.8.1-buster

RUN apt update -y && apt install -y --fix-missing --no-install-recommends \
    python3-pip software-properties-common build-essential \
    cmake sqlite3 gfortran python-dev python3-dev

RUN cd /tmp && curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh && \
    bash Anaconda3-2019.10-Linux-x86_64.sh -b && \
    rm Anaconda3-2019.10-Linux-x86_64.sh
ENV PATH /root/anaconda3/bin:$PATH

ADD environment.yml ./environment.yml
RUN conda config --set channel_priority false
RUN conda config --add channels conda-forge && conda config --add channels anaconda
RUN conda env create -f ./environment.yml

WORKDIR /src
COPY . /src/
COPY pylims/uwsgi.ini /etc/uwsgi/

RUN chmod 755 /src/django_start.sh
ENV PATH /root/anaconda3/envs/pylims:/root/anaconda3/envs/pylims/bin:/root/anaconda3/envs/pylims/lib:/etc:/src:$PATH
ENV PYTHONPATH /src:$PYTHONPATH