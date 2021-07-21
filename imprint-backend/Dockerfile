FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# RUN apt-get update 
    # apt-get install -y binutils libproj-dev gdal-bin

RUN apt-get -y install sudo

RUN pip install -r requirements.txt
# COPY  main/libgeos.py /usr/local/lib/python3.8/site-packages/django/contrib/gis/geos/libgeos.py
# RUN apt-get install npm -y
# RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
# USER docker
CMD /bin/bash
