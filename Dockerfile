FROM halotools/python-sdk:ubuntu-16.04_sdk-1.0.4_2018-01-22
MAINTAINER jgibbons-cp

RUN apt-get update && apt-get install -y \
    python=2.7.11-1

RUN mkdir /app

COPY app/ /app/

WORKDIR /app/

CMD ["/usr/bin/python", "runner.py"]