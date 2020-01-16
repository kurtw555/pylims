FROM python:3.8

RUN apt update -y && apt install -y --fix-missing --no-install-recommends \
    python3-pip software-properties-common build-essential \
    cmake sqlite3 gfortran python-dev

RUN cd /tmp && curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh && \
    bash Anaconda3-2019.10-Linux-x86_64.sh -b && \
    rm Anaconda3-2019.10-Linux-x86_64.sh
ENV PATH /root/anaconda3/bin:$PATH

RUN activate base
RUN conda update conda -y && \
    conda update anaconda -y

RUN conda info
COPY environment.yml ./environment.yml
RUN conda create -f environment.yml
RUN activate pylims

WORKDIR /src
COPY . /src/
COPY pylims/uwsgi.ini /etc/uwsgi/

RUN chmod 755 /src/django_start.sh
ENV PYTHONPATH="/src"